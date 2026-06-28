from fastapi import FastAPI
from app.routes import router
from app.logger import logger
from app.database import initialize_database
app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with CRUD operations and nearby location search using FastAPI and SQLite.",
    version="1.0.0",
    contact={
        "name": "Harinarayanan",
        "email": "harinarayananpari@gmail.com"
    }
)
initialize_database()
logger.info("Starting Address Book API")
app.include_router(router)