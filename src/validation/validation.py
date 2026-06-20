import pandas as pd
from src.utils.logger import get_logger
from src.config.settings import VALIDATION_REPORT_PATH

logger = get_logger()


class DataValidator:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def generate_report(self):
        try:
            logger.info(
                "Starting validation process..."
            )

            report = {

                "total_rows":
                    len(self.df),

                "null_customer_id":
                    self.df["CustomerID"].isnull().sum(),

                "null_description":
                    self.df["Description"].isnull().sum(),

                "negative_quantity":
                    (self.df["Quantity"] <= 0).sum(),

                "negative_unit_price":
                    (self.df["UnitPrice"] <= 0).sum(),

                "duplicate_rows":
                    self.df.duplicated().sum(),

                "cancelled_orders":
                    self.df["InvoiceNo"]
                    .astype(str)
                    .str.startswith("C")
                    .sum()
            }

            logger.info(
                "Validation completed successfully"
            )

            return report
        except Exception as e:
            logger.error(f"Validation report generation failed: {e}")
            raise e

    def save_report(self, report):
        try:
            report_df = pd.DataFrame(report.items(), columns=["Metric","Count"])
            
            
            VALIDATION_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
            
            report_df.to_csv(VALIDATION_REPORT_PATH, index=False)
            logger.info("Validation report saved")
        except Exception as e:
            logger.error(f"Saving validation report failed: {e}")
            raise e