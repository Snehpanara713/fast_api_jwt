from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables for database connection
RDS_USERNAME: str = os.environ.get("RDS_USERNAME", "postgres")
RDS_PASSWORD: str = os.environ.get("RDS_PASSWORD", "123456")
RDS_HOSTNAME: str = os.environ.get("RDS_HOSTNAME", "localhost")
RDS_DB_NAME: str = os.environ.get("RDS_DB_NAME", "db_employeeapp")
RDS_PORT: int = int(os.environ.get("RDS_PORT", 5432))

# Construct the database URL for PostgreSQL
POSTGRESQL_DATABASE_URL = f"postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"

# Create a base class for declarative class definitions
Base = declarative_base()

# Create an engine to interact with the database
engine = create_engine(POSTGRESQL_DATABASE_URL)

# Create a session maker with autocommit and autoflush settings
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define a function to retrieve a database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
