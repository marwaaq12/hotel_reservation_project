from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# -----------------------------
# Database connection settings
# -----------------------------

DB_USER = "marwaaq"
DB_PASSWORD = "marwaphpmyadminaq"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "hotel_db"

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------
# Engine & session
# -----------------------------

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

# -----------------------------
# Helper functions
# -----------------------------

def get_db():
    """
    Create a database session and close it properly
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def fetch_all(query: str):
    """
    Execute a SELECT query and return all rows
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
