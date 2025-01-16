from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import app.config.config as config 

DATABASE_URL = config.get_database_url()

if not DATABASE_URL:
    raise RuntimeError("Failed to retrieve the database URL from SSM.")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"options": "-c statement_timeout=60000"} )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()