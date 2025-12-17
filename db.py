import os
from sqlalchemy import create_engine
import pandas as pd

# When running in Docker, the host is 'db'. When running locally, it's '127.0.0.1'
DB_HOST = os.getenv("DB_HOST", "db") 
DB_PORT = "3306" # Inside the docker network, use the internal port 3306
DB_USER = "marwaaq"
DB_PASSWORD = "marwaphpmyadminaq"
DB_NAME = "hotel_db"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

def query(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, engine)