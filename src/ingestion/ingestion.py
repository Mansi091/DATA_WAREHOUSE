import pandas as pd
import boto3
import os
from dotenv import load_dotenv
from src.utils.logger import get_logger

load_dotenv()

logger = get_logger()

class DataIngestion:

    def __init__(self, file_path=None):
        self.file_path = file_path

    def load_data(self):

        try:
            logger.info("Starting data ingestion")

            # Read from S3
            if os.getenv("USE_S3", "False") == "True":

                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    region_name=os.getenv("AWS_REGION")
                )

                obj = s3.get_object(
                    Bucket=os.getenv("S3_BUCKET"),
                    Key=os.getenv("S3_KEY")
                )

                df = pd.read_csv(obj["Body"])

                logger.info("Loaded dataset from Amazon S3")

            else:

                df = pd.read_csv(self.file_path)

                logger.info("Loaded dataset from local file")

            logger.info(
                f"Successfully loaded {df.shape[0]} rows and {df.shape[1]} columns"
            )

            return df

        except Exception as e:

            logger.error(f"Ingestion Failed: {e}")
            raise