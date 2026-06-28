from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from app.logger import logger

DATABASE_URL = "sqlite:///./address.db"
DATABASE_NAME = "address.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def initialize_database():
    check_database()
    check_tables()

def check_database():
    db_file = Path(DATABASE_NAME)

    if db_file.exists():
        logger.info("Database file already exists.")
        return
    
    logger.info("Database file not found.")
    logger.info("Creating SQLite database...")
    # SQLite creates the file when a connection/table is created
    Base.metadata.create_all(bind=engine)

    logger.info("Database created successfully.")

def check_tables():
    inspector = inspect(engine)

    if "addresses" in inspector.get_table_names():
        logger.info("Addresses table already exists.")
        return

    logger.info("Addresses table not found.")
    logger.info("Creating addresses table...")

    Base.metadata.create_all(bind=engine)

    logger.info("Addresses table created successfully.")