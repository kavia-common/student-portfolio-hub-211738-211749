from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import Education
from src.schemas import EducationCreate, EducationOut, EducationUpdate

router = APIRouter(prefix="/education", tags=["Education"])


@router.get(
    "/",
    response_model=list[EducationOut],
    summary="List education records",
    description="Return a list of education records.",
    operation_id="list_education",
)
async def list_education(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List education records."""
    limit, offset = pagination
    result = await session.execute(select(Education).order_by(Education.id.desc()).limit(limit).offset(offset))
    return list(result.scalars().all())


@router.get(
    "/{education_id}",
    response_model=EducationOut,
    summary="Get an education record",
    description="Fetch an education record by id.",
    operation_id="get_education",
)
async def get_education(education_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get education record by id."""
    obj = await session.get(Education, education_id)
    if not obj:
        raise not_found("Education record not found")
    return obj


@router.post(
    "/",
    response_model=EducationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create an education record",
    description="Create a new education record.",
    operation_id="create_education",
)
async def create_education(payload: EducationCreate, session: AsyncSession = Depends(get_db_session)):
    """Create education record."""
    obj = Education(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{education_id}",
    response_model=EducationOut,
    summary="Update an education record",
    description="Update an existing education record.",
    operation_id="update_education",
)
async def update_education(
    education_id: int, payload: EducationUpdate, session: AsyncSession = Depends(get_db_session)
):
    """Update education record."""
    obj = await session.get(Education, education_id)
    if not obj:
        raise not_found("Education record not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{education_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an education record",
    description="Delete an education record by id.",
    operation_id="delete_education",
)
async def delete_education(education_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete education record."""
    obj = await session.get(Education, education_id)
    if not obj:
        raise not_found("Education record not found")
    await session.delete(obj)
    await session.commit()
    return None
