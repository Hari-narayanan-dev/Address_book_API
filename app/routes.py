from fastapi import APIRouter


router = APIRouter(
    tags=["Address Management"]
)

@router.get("/health")
def health():
    return {
        "status": "The API is healthy"
    }