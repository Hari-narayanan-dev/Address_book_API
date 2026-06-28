from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with CRUD operations and nearby location search using FastAPI and SQLite.",
    version="1.0.0",
    contact={
        "name": "Harinarayanan",
        "email": "harinarayananpari@gmail.com"
    }
)

app.include_router(router)