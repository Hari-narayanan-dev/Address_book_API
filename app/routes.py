from fastapi import APIRouter, status, Depends
from app import crud, schemas
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(
    tags=["Address Management"]
)

@router.get("/health")
def health():
    return {
        "status": "The API is healthy"
    }


@router.post(
    "/addresses",
    response_model=schemas.AddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Address",
    description="Creates a new address and stores it in the SQLite database."
)
def create_address(
    address: schemas.AddressCreate,
    db: Session = Depends(get_db),
):
    return crud.create_address(db, address)