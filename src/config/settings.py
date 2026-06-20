import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path.cwd()

RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "Online Retail.csv"

REPORTS_DIR = BASE_DIR / "data" / "reports"
VALIDATION_REPORT_PATH = REPORTS_DIR / "validation_report.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
CLEANED_DATA_PATH = PROCESSED_DIR / "clean_retail_data.csv"

DB_TYPE = os.getenv("DB_TYPE", "postgresql").lower()
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "retail_warehouse")

