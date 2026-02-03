from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import Achievement
from src.schemas import AchievementCreate, AchievementOut, AchievementUpdate

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.get(
    "/",
    response_model=list[AchievementOut],
    summary="List achievements",
    description="Return a list of achievements.",
    operation_id="list_achievements",
)
async def list_achievements(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List achievements."""
    limit, offset = pagination
    result = await session.execute(select(Achievement).order_by(Achievement.id.desc()).limit(limit).offset(offset))
    return list(result.scalars().all())


@router.get(
    "/{achievement_id}",
    response_model=AchievementOut,
    summary="Get an achievement",
    description="Fetch an achievement by id.",
    operation_id="get_achievement",
)
async def get_achievement(achievement_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get achievement by id."""
    obj = await session.get(Achievement, achievement_id)
    if not obj:
        raise not_found("Achievement not found")
    return obj


@router.post(
    "/",
    response_model=AchievementOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create an achievement",
    description="Create a new achievement entry.",
    operation_id="create_achievement",
)
async def create_achievement(payload: AchievementCreate, session: AsyncSession = Depends(get_db_session)):
    """Create achievement."""
    obj = Achievement(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{achievement_id}",
    response_model=AchievementOut,
    summary="Update an achievement",
    description="Update an existing achievement entry.",
    operation_id="update_achievement",
)
async def update_achievement(
    achievement_id: int, payload: AchievementUpdate, session: AsyncSession = Depends(get_db_session)
):
    """Update achievement."""
    obj = await session.get(Achievement, achievement_id)
    if not obj:
        raise not_found("Achievement not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{achievement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an achievement",
    description="Delete an achievement entry by id.",
    operation_id="delete_achievement",
)
async def delete_achievement(achievement_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete achievement."""
    obj = await session.get(Achievement, achievement_id)
    if not obj:
        raise not_found("Achievement not found")
    await session.delete(obj)
    await session.commit()
    return None
