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


@router.get(
    "/addresses",
    response_model=schemas.AddressResponse,
    summary="Get All Addresses",
    description="Returns all addresses stored in the database."
)
def get_addresses(
    db: Session = Depends(get_db)
):
    return crud.get_addresses(db)

@router.get(
    "/addresses/{address_id}",
    response_model=schemas.AddressResponse,
    summary="Get Address by ID",
    description="Returns a single address using its unique ID."
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    address_data = crud.get_address(db, address_id)

    return address_data

@router.put(
    "/addresses/{address_id}",
    response_model=schemas.AddressResponse,
    summary="Update Address",
    description="Updates an existing address in the database."
)
def update_address(
    address_id: int,
    updated: schemas.AddressUpdate,
    db: Session = Depends(get_db)
):
    address_data = crud.update_address(db, address_id, updated)
    # if not address_data:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Address not found"
    #     )
    return address_data


@router.delete(
    "/addresses/{address_id}",
    summary="Delete Address",
    description="Deletes an address from the database."
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db)
):
    address_data = crud.delete_address(db, address_id)

    return address_data