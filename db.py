from sqlalchemy import create_engine
import pandas as pd

def get_engine():
    return create_engine(
        "mysql+pymysql://root:marwaphpmyadminaq@localhost:3306/hotel_mysql"
    )

def query(sql):
    engine = get_engine()
    return pd.read_sql(sql, engine)