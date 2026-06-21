import boto3
import os

from io import StringIO
from dotenv import load_dotenv

load_dotenv()


class S3Storage:

    def __init__(self):

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv(
                "AWS_ACCESS_KEY_ID"
            ),
            aws_secret_access_key=os.getenv(
                "AWS_SECRET_ACCESS_KEY"
            ),
            region_name=os.getenv(
                "AWS_REGION"
            )
        )

        self.bucket = os.getenv(
            "S3_BUCKET"
        )

    def upload_dataframe(
        self,
        df,
        key
    ):

        csv_buffer = StringIO()

        df.to_csv(
            csv_buffer,
            index=False
        )

        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=csv_buffer.getvalue()
        )