# Address Book REST API

A RESTful Address Book API built using **FastAPI** and **SQLite**. The application supports complete CRUD operations, bulk address creation, duplicate validation, nearby address search using geographical coordinates, request validation, and structured logging.

---

# Technology Stack

* Python 3.10+
* FastAPI
* SQLite
* SQLAlchemy
* Pydantic
* Uvicorn

---

# Features

* Create a new address
* Bulk create multiple addresses
* Retrieve all addresses
* Retrieve address by ID
* Update an existing address
* Delete an address
* Nearby address search using Haversine Formula
* Duplicate address detection
* Request validation using Pydantic
* Structured application logging
* SQLite database integration
* RESTful API design
* Interactive Swagger Documentation

---

# Project Structure

```
address_book/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── crud.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── utils.py
│   └── logger.py
│
├── requirements.txt
├── README.md
└── address_book.db
```

---

# Prerequisites

* Python 3.10 or above
* Git
* Postman (Recommended)
* VS Code (Optional)

---

# Clone the Repository

```bash
git clone <repository-url>

cd address_book
```

---

# Create Virtual Environment

## Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## macOS / Linux

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

This project does not require any external environment variables.

The application automatically creates the SQLite database during the first execution if it does not already exist.

---

# Run the Application

```bash
uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Database Initialization

On application startup:

* Checks whether the SQLite database exists
* Creates the database if not present
* Verifies the Address table
* Creates the table if required
* Starts the FastAPI application

---

# API Endpoints

---

## Health Check

### GET

```
/health
```

Response

```json
{
    "status": "The API is healthy"
}
```

---

## Create Address

### POST

```
/addresses
```

Request

```json
{
    "name": "Anna Nagar",
    "street": "2nd Avenue",
    "city": "Chennai",
    "latitude": 13.084,
    "longitude": 80.210
}
```

Response

```json
{
    "success": true,
    "message": "Address created successfully."
}
```

---

## Bulk Create Addresses

### POST

```
/addresses/bulk
```

Request

```json
{
    "data": [
        {
            "name": "Indiranagar Office",
            "street": "100 Feet Road",
            "city": "Bangalore",
            "latitude": 12.9784,
            "longitude": 77.6408
        },
        {
            "name": "Koramangala Hub",
            "street": "80 Feet Road",
            "city": "Bangalore",
            "latitude": 12.9352,
            "longitude": 77.6245
        }
    ]
}
```

Response

```json
{
    "success": true,
    "message": "Bulk address creation completed.",
    "data": {
        "created_count": 2,
        "duplicate_count": 0
    }
}
```

---

## Get All Addresses

### GET

```
/addresses
```

Response

```json
{
    "success": true,
    "message": "Addresses retrieved successfully.",
    "data": [
        {
            "id": 1,
            "name": "Anna Nagar",
            "street": "2nd Avenue",
            "city": "Chennai",
            "latitude": 13.084,
            "longitude": 80.210
        }
    ]
}
```

---

## Get Address by ID

### GET

```
/addresses/{id}
```

Example

```
/addresses/1
```

---

## Update Address

### PUT

```
/addresses/{id}
```

Request

```json
{
    "name": "Anna Nagar Updated",
    "street": "2nd Avenue",
    "city": "Chennai",
    "latitude": 13.084,
    "longitude": 80.210
}
```

---

## Delete Address

### DELETE

```
/addresses/{id}
```

Example

```
/addresses/1
```

---

## Nearby Address Search

### GET

```
/addresses/nearby
```

Query Parameters

| Parameter | Description          |
| --------- | -------------------- |
| latitude  | Current Latitude     |
| longitude | Current Longitude    |
| distance  | Radius in Kilometers |

Example

```
/addresses/nearby?latitude=12.9784&longitude=77.6408&distance=10
```

Returns all addresses located within the specified radius.

---

# Logging

The application logs important events including:

* Application startup
* Database initialization
* Table validation
* Address creation
* Bulk creation
* Duplicate detection
* Retrieval operations
* Updates
* Deletions
* Nearby search operations
* Warnings and errors

---

# Request Validation

The API validates:

* Required fields
* Latitude range (-90 to 90)
* Longitude range (-180 to 180)
* Empty values
* Invalid request bodies

Validation is performed using Pydantic schemas before reaching the business logic.

---

# Duplicate Validation

Before inserting a new address, the application checks whether an address with the same:

* Name
* Street
* City
* Latitude
* Longitude

already exists.

If found, the request is skipped and an appropriate response is returned.

---

# Nearby Search

The Nearby Search API uses the **Haversine Formula** to calculate the geographical distance between two latitude and longitude coordinates.

Only addresses that fall within the specified search radius are returned.

---

# Testing the API

The APIs can be tested using:

* FastAPI Swagger UI
* Postman
* cURL

Suggested testing order:

1. Health Check
2. Create Address
3. Get All Addresses
4. Get Address by ID
5. Update Address
6. Delete Address
7. Bulk Create Addresses
8. Nearby Search

---

# Future Improvements

If this project were extended further, the following enhancements could be considered:

* PostgreSQL/MySQL support
* JWT Authentication & Authorization
* Alembic Database Migrations
* Docker Containerization
* Unit & Integration Testing using Pytest
* Spatial indexing for optimized nearby search
* CI/CD Pipeline
* Pagination and Filtering
* Rate Limiting
* Environment-based configuration

---

# Author

**Harinarayanan**

Software Engineer | Python Backend Developer

---

Thank you for reviewing this project.
