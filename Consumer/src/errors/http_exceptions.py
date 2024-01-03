from fastapi import status
from fastapi import HTTPException


INTERNAL_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal error"
)

NOT_FOUND = HTTPException(
    status.HTTP_404_NOT_FOUND,
    "Entity not found"
)
