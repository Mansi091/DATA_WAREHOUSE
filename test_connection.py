from src.database.connection import get_engine
from src.config.settings import DB_USER, DB_HOST, DB_PORT, DB_NAME

print("DEBUG: Connection Parameters")
print(f"  DB_USER: {DB_USER}")
print(f"  DB_HOST: {DB_HOST}")
print(f"  DB_PORT: {DB_PORT}")
print(f"  DB_NAME: {DB_NAME}")

try:
    engine = get_engine()
    connection = engine.connect()
    print("Database Connected Successfully!")
    connection.close()
except Exception as e:
    print("Connection Failed")
    print(e)