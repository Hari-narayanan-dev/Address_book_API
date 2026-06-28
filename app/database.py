from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

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
        return
    # SQLite creates the file when a connection/table is created
    Base.metadata.create_all(bind=engine)



def check_tables():
    inspector = inspect(engine)

    if "addresses" in inspector.get_table_names():
        return

    Base.metadata.create_all(bind=engine)