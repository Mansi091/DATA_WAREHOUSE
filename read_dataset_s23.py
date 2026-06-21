# read_s3.py

from dotenv import load_dotenv
import boto3
import pandas as pd
import os

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

obj = s3.get_object(
    Bucket=os.getenv("S3_BUCKET"),
    Key="raw/Online Retail.csv"
)

df = pd.read_csv(obj["Body"])

print(df.head())
print(df.shape)