from fastapi import HTTPException, Query, status


# PUBLIC_INTERFACE
def pagination_params(
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return."),
    offset: int = Query(0, ge=0, description="Number of records to skip."),
) -> tuple[int, int]:
    """Common pagination parameters dependency."""
    return limit, offset


def not_found(detail: str = "Item not found") -> HTTPException:
    """Return a standardized 404 exception."""
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
