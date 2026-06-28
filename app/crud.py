from app.models import Address
from app.schemas import AddressCreate
from sqlalchemy.orm import Session


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

