from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import Skill
from src.schemas import SkillCreate, SkillOut, SkillUpdate

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get(
    "/",
    response_model=list[SkillOut],
    summary="List skills",
    description="Return a list of skills.",
    operation_id="list_skills",
)
async def list_skills(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List skills."""
    limit, offset = pagination
    result = await session.execute(select(Skill).order_by(Skill.id.desc()).limit(limit).offset(offset))
    return list(result.scalars().all())


@router.get(
    "/{skill_id}",
    response_model=SkillOut,
    summary="Get a skill",
    description="Fetch a skill by id.",
    operation_id="get_skill",
)
async def get_skill(skill_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get skill by id."""
    obj = await session.get(Skill, skill_id)
    if not obj:
        raise not_found("Skill not found")
    return obj


@router.post(
    "/",
    response_model=SkillOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a skill",
    description="Create a new skill entry.",
    operation_id="create_skill",
)
async def create_skill(payload: SkillCreate, session: AsyncSession = Depends(get_db_session)):
    """Create skill."""
    obj = Skill(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{skill_id}",
    response_model=SkillOut,
    summary="Update a skill",
    description="Update an existing skill entry.",
    operation_id="update_skill",
)
async def update_skill(skill_id: int, payload: SkillUpdate, session: AsyncSession = Depends(get_db_session)):
    """Update skill."""
    obj = await session.get(Skill, skill_id)
    if not obj:
        raise not_found("Skill not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a skill",
    description="Delete a skill entry by id.",
    operation_id="delete_skill",
)
async def delete_skill(skill_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete skill."""
    obj = await session.get(Skill, skill_id)
    if not obj:
        raise not_found("Skill not found")
    await session.delete(obj)
    await session.commit()
    return None
