from app.models import Address
from app.schemas import AddressCreate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils import haversine


def create_address(db: Session, address: AddressCreate):

    existing_address = (
        db.query(Address)
        .filter(
            Address.name == address.name,
            Address.street == address.street,
            Address.city == address.city,
            Address.latitude == address.latitude,
            Address.longitude == address.longitude,
        )
        .first()
    )

    if existing_address:

        return {
            "success": False,
            "message": "Address already exists.",
            "data": None
        }

    db_address = Address(
        name=address.name,
        street=address.street,
        city=address.city,
        latitude=address.latitude,
        longitude=address.longitude,
    )

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return {
        "success": True,
        "message": "Address created successfully.",
    }

def get_addresses(db: Session):
    addresses = db.query(Address).all()
    if not addresses:
        return {
            "success": False,
            "message": "No addresses found.",
        }
    return {
        "success": True,
        "message": "Addresses retrieved successfully.",
        "data": [
        {
            "id": a.id,
            "name": a.name,
            "street": a.street,
            "city": a.city,
            "latitude": a.latitude,
            "longitude": a.longitude,
        }
        for a in addresses
    ]
    }

def get_address(db: Session, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"Address with ID {address_id} not found.",
        }
    )
    return {
        "success": True,
        "message": "Address fetched successfully.",
        "data": {
            "id": address.id,
            "name": address.name,
            "street": address.street,
            "city": address.city,
            "latitude": address.latitude,
            "longitude": address.longitude,
        }
    }


def update_address(db: Session, address_id: int, updated: AddressCreate):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"Address with ID {address_id} not found.",
        })

    address.name = updated.name
    address.street = updated.street
    address.city = updated.city
    address.latitude = updated.latitude
    address.longitude = updated.longitude

    db.commit()
    db.refresh(address)
    return {
        "success": True,
        "message": "Address updated successfully.",
        "data": {
            "id": address.id,
        }
    }


def delete_address(db: Session, address_id: int):
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": f"Address with ID {address_id} not found.",
            }
        )

    db.delete(address)
    db.commit()

    return {
        "success": True,
        "message": "Address deleted successfully.",
        "data":{
            "id": address.id,
        }
    }

def get_nearby_addresses(
    db: Session,
    latitude: float,
    longitude: float,
    distance: float,
):
    addresses = db.query(Address).all()

    nearby = []

    for address in addresses:

        d = haversine(
            latitude,
            longitude,
            address.latitude,
            address.longitude,
        )

        if d <= distance:

            nearby.append(
                {
                    "id": address.id,
                    "name": address.name,
                    "street": address.street,
                    "city": address.city,
                    "latitude": address.latitude,
                    "longitude": address.longitude,
                    "distance_km": round(d, 2),
                }
            )
        else:
            return {
                "success": False,
                "message": "No Nearby addresses Found.",
            }
    return {
        "success": True,
        "message": "Nearby addresses retrieved successfully.",
        "data": nearby
    }
