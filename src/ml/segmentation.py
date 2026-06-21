import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from src.database.connection import get_engine
from src.utils.logger import get_logger

logger = get_logger()


class CustomerSegmenter:

    def __init__(self):
        self.engine = get_engine()

    def load_data(self):
        logger.info("loading data for customer segmentation")
        query = """
        SELECT
            "CustomerID",
            "InvoiceDate",
            "InvoiceNo",
            "Revenue"
        FROM online_retail_clean
        """
        df = pd.read_sql(query, self.engine)
        logger.info(f"Loaded {df.shape[0]} rows for segmentation")
        return df

    def calculate_rfm(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("calculating RFM metrics")
        
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        
        max_date = df["InvoiceDate"].max()
        reference_date = max_date + pd.Timedelta(days=1)
        
        rfm = df.groupby("CustomerID").agg(
            LastPurchase=("InvoiceDate", "max"),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Revenue", "sum")
        ).reset_index()
        
        rfm["Recency"] = (reference_date - rfm["LastPurchase"]).dt.days
        rfm = rfm.drop(columns=["LastPurchase"])
        
        logger.info(f"Calculated RFM metrics for {len(rfm)} customers")
        return rfm

    def preprocess_and_segment(self, rfm: pd.DataFrame) -> pd.DataFrame:
        logger.info("preprocessing features and running K-Means clustering")
        
        rfm_features = rfm[["Recency", "Frequency", "Monetary"]].copy()
        rfm_features["Monetary"] = rfm_features["Monetary"].clip(lower=0.01)
        
        rfm_log = np.log1p(rfm_features)
        
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_log)
        
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)
        
        cluster_summary = rfm.groupby("Cluster").agg(
            Recency_mean=("Recency", "mean"),
            Frequency_mean=("Frequency", "mean"),
            Monetary_mean=("Monetary", "mean")
        ).reset_index()
        
        score_scaler = StandardScaler()
        summary_scaled = score_scaler.fit_transform(
            cluster_summary[["Recency_mean", "Frequency_mean", "Monetary_mean"]]
        )
        
        scores = -summary_scaled[:, 0] + summary_scaled[:, 1] + summary_scaled[:, 2]
        cluster_summary["Score"] = scores
        
        sorted_clusters = cluster_summary.sort_values(by="Score").reset_index(drop=True)
        
        labels = [
            "Hibernating / Lost",
            "At-Risk",
            "Loyal / Active",
            "VIP / Champions"
        ]
        
        cluster_mapping = {}
        for i, row in sorted_clusters.iterrows():
            cluster_mapping[int(row["Cluster"])] = labels[i]
            
        rfm["Segment"] = rfm["Cluster"].map(cluster_mapping)
        
        logger.info(f"Assigned segments: {rfm['Segment'].value_counts().to_dict()}")
        return rfm

    def save_to_db(self, rfm: pd.DataFrame):
        logger.info("saving segments back to dim_customer table")
        
        dim_customer = rfm[[
            "CustomerID", "Recency", "Frequency", "Monetary", "Segment"
        ]]
        
        dim_customer.to_sql(
            "dim_customer",
            self.engine,
            if_exists="replace",
            index=False
        )
        logger.info(f"Successfully saved {len(dim_customer)} records to dim_customer")

    def run_segmentation(self):
        try:
            logger.info("starting customer segmentation pipeline")
            df = self.load_data()
            rfm = self.calculate_rfm(df)
            segmented_rfm = self.preprocess_and_segment(rfm)
            self.save_to_db(segmented_rfm)
            print("Customer segmentation pipeline completed successfully!")
        except Exception as e:
            logger.error(f"Customer segmentation failed: {e}")
            raise e