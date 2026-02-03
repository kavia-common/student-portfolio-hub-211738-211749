from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import Profile
from src.schemas import ProfileCreate, ProfileOut, ProfileUpdate

router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    "/",
    response_model=list[ProfileOut],
    summary="List profiles",
    description="Return a list of profile records (typically one).",
    operation_id="list_profiles",
)
async def list_profiles(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List profile records."""
    limit, offset = pagination
    result = await session.execute(select(Profile).order_by(Profile.id).limit(limit).offset(offset))
    return list(result.scalars().all())


@router.get(
    "/{profile_id}",
    response_model=ProfileOut,
    summary="Get a profile",
    description="Fetch a profile by id.",
    operation_id="get_profile",
)
async def get_profile(profile_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get a profile by its id."""
    obj = await session.get(Profile, profile_id)
    if not obj:
        raise not_found("Profile not found")
    return obj


@router.post(
    "/",
    response_model=ProfileOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a profile",
    description="Create a new profile record.",
    operation_id="create_profile",
)
async def create_profile(payload: ProfileCreate, session: AsyncSession = Depends(get_db_session)):
    """Create a profile record."""
    obj = Profile(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{profile_id}",
    response_model=ProfileOut,
    summary="Update a profile",
    description="Update an existing profile record by replacing provided fields.",
    operation_id="update_profile",
)
async def update_profile(
    profile_id: int, payload: ProfileUpdate, session: AsyncSession = Depends(get_db_session)
):
    """Update a profile record."""
    obj = await session.get(Profile, profile_id)
    if not obj:
        raise not_found("Profile not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a profile",
    description="Delete a profile by id.",
    operation_id="delete_profile",
)
async def delete_profile(profile_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete a profile record."""
    obj = await session.get(Profile, profile_id)
    if not obj:
        raise not_found("Profile not found")
    await session.delete(obj)
    await session.commit()
    return None
