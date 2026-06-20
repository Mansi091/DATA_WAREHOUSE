import pandas as pd
from src.utils.logger import get_logger

logger = get_logger()

class DataIngestion:

    def __init__(self,file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            logger.info("Starting data ingestion")

            df = pd.read_csv(self.file_path)

            logger.info(f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns")

            return df

        except Exception as e:
            logger.error(f"Ingestion Failed : {e}")

