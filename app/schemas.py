from pydantic import BaseModel, Field
from typing import Optional
from typing import Any


class AddressData(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name of the address"
    )

    street: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Street address"
    )

    city: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="City name"
    )

    latitude: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude"
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude"
    )

class AddressResponse(BaseModel):
    success: bool
    message: str
    data: Any | None = None

class AddressCreate(AddressData):
    pass

class AddressUpdate(AddressData):
    pass