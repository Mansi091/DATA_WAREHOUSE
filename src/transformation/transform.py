import pandas as pd
from src.utils.logger import get_logger
from src.config.settings import CLEANED_DATA_PATH

logger = get_logger()



class DataTransformer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def clean_data(self):
        try:
            logger.info("Starting data transformation")

            initial_rows = len(self.df)

            self.df = self.df.dropna(
                subset=["CustomerID"]
            )

            self.df = self.df.dropna(
                subset=["Description"]
            )

            self.df = self.df[
                self.df["Quantity"] > 0
            ]

            self.df = self.df.drop_duplicates()

            self.df = self.df[
                ~self.df["InvoiceNo"]
                .astype(str)
                .str.startswith("C")
            ]

            final_rows = len(self.df)

            logger.info(
                f"Removed {initial_rows - final_rows} invalid rows"
            )

            return self.df

        except Exception as e:
            logger.error(
                f"Data cleaning failed: {e}"
            )
            raise e

    def create_features(self):
        try:
            logger.info(
                "Creating new features"
            )

            self.df["Revenue"] = (
                self.df["Quantity"]
                * self.df["UnitPrice"]
            )

            self.df["InvoiceDate"] = pd.to_datetime(
                self.df["InvoiceDate"]
            )

            self.df["Year"] = (
                self.df["InvoiceDate"].dt.year
            )

            self.df["Month"] = (
                self.df["InvoiceDate"].dt.month
            )

            self.df["Quarter"] = (
                self.df["InvoiceDate"].dt.quarter
            )

            self.df["Day"] = (
                self.df["InvoiceDate"].dt.day
            )

            self.df["Weekday"] = (
                self.df["InvoiceDate"].dt.day_name()
            )

            logger.info(
                "Feature engineering completed successfully"
            )

            return self.df

        except Exception as e:
            logger.error(
                f"Creation of new features failed: {e}"
            )
            raise e

    def save_data(self):
        try:
            CLEANED_DATA_PATH.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.df.to_csv(
                CLEANED_DATA_PATH,
                index=False
            )

            logger.info(
                f"Processed data saved locally at: {CLEANED_DATA_PATH}"
            )

        except Exception as e:

            logger.error(
                f"Saving processed data failed: {e}"
            )

            raise e