from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# configure env variables for db
host = os.getenv("HOST_DB", "database")
port = os.getenv("POSTGRES_PORT", "5432")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
db = os.getenv("POSTGRES_DB", "book_inventory")
dbtype = os.getenv("DBTYPE", "postgresql")

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
