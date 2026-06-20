from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from src.config.settings import (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

def get_engine():
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT) if DB_PORT else 5432,
        database=DB_NAME
    )

    engine = create_engine(connection_url)
    return engine