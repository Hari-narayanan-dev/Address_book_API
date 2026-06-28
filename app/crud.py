from app.models import Address
from app.schemas import AddressCreate, BulkAddressItem
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.utils import haversine
from app.logger import logger


def create_address(db: Session, address: AddressCreate):
    logger.info(f"Creating address: {address.name}")
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
        logger.warning("Duplicate address found.")
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
    logger.info(f"Address created: {db_address.name}")
    return {
        "success": True,
        "message": "Address created successfully.",
    }

def create_bulk_addresses(
    db: Session,
    addresses: list[BulkAddressItem]
):
    logger.info(
        f"Bulk creation started. Total addresses: {len(addresses)}"
    )
    created = []
    duplicates = []

    for address in addresses:

        duplicate = (
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

        if duplicate:
            duplicates.append(address.name)
            continue

        db_address = Address(
            name=address.name,
            street=address.street,
            city=address.city,
            latitude=address.latitude,
            longitude=address.longitude,
        )

        db.add(db_address)
        created.append(db_address)

    db.commit()

    for address in created:
        db.refresh(address)
    logger.info(
        f"Bulk creation completed. "
        f"Created={len(created)}, "
        f"Duplicates={len(duplicates)}"
    )

    return {
        "success": True,
        "message": "Bulk address creation completed.",
        "data": {
            "total_received": len(addresses),
            "created_count": len(created),
            "duplicate_count": len(duplicates),
            "duplicates": duplicates
        }
    }

def get_addresses(db: Session):
    logger.info("Fetching all addresses")
    addresses = db.query(Address).all()
    if not addresses:
        logger.warning("No addresses found in the database")
        return {
            "success": False,
            "message": "No addresses found.",
        }
    logger.info(f"Found {len(addresses)} addresses")
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
    logger.info(f"Fetching address with ID: {address_id}")
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        logger.warning(f"Address not found | ID={address_id}")
        return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"Address with ID {address_id} not found.",
        }
    )
    logger.info(f"Address fetched: {address.name if address else 'Not found'}")
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
    logger.info(f"Updating address with ID: {address_id}")
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Update failed | Address ID={address_id}. Address with ID: {address_id} not found")
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
    logger.info(f"Address updated successfully | ID={address.id}")
    return {
        "success": True,
        "message": "Address updated successfully.",
        "data": {
            "id": address.id,
        }
    }


def delete_address(db: Session, address_id: int):
    logger.warning(f"Deleting Address with ID: {address_id}")
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Address with ID: {address_id} not found")
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": f"Address with ID {address_id} not found.",
            }
        )

    db.delete(address)
    db.commit()
    logger.info(f"Address deleted successfully | ID={address_id}")
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
    logger.info(f"Fetching nearby addresses within {distance} km")
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
    if not nearby:
        return {
            "success": False,
            "message": "No Nearby addresses Found.",
        }
    logger.info(f"Found {len(nearby)} nearby addresses")
    return {
        "success": True,
        "message": f"{len(nearby)} Nearby addresses retrieved successfully.",
        "data": nearby
    }
