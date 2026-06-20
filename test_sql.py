from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://postgres:Mansi091%40@localhost:5432/retail_dw"
)

query = """
SELECT COUNT(*)
FROM online_retail_clean
"""

result = pd.read_sql(query, engine)

print(result)