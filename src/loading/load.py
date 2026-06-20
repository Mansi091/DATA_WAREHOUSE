import pandas as pd
from src.database.connection import get_engine
from src.utils.logger import get_logger

logger = get_logger()


class DataLoader:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def load_to_db(self, table_name="online_retail_clean"):
        try:
            logger.info(f"Starting database load into table: {table_name}")
            engine = get_engine()

            #uplood using pandas to_sql
            self.df.to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False
            )

            logger.info(
                f"Loaded {len(self.df)} rows into '{table_name}'"
            )
            print(
                f"database Load Complete: Loaded {len(self.df)} rows into '{table_name}'"
            )
        except Exception as e:
            logger.error(f"database loading failed: {e}")
            raise e
