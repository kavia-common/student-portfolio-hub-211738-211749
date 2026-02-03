from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import Project
from src.schemas import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/",
    response_model=list[ProjectOut],
    summary="List projects",
    description="Return a list of projects.",
    operation_id="list_projects",
)
async def list_projects(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List projects."""
    limit, offset = pagination
    result = await session.execute(select(Project).order_by(Project.id.desc()).limit(limit).offset(offset))
    return list(result.scalars().all())


@router.get(
    "/{project_id}",
    response_model=ProjectOut,
    summary="Get a project",
    description="Fetch a project by id.",
    operation_id="get_project",
)
async def get_project(project_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get project by id."""
    obj = await session.get(Project, project_id)
    if not obj:
        raise not_found("Project not found")
    return obj


@router.post(
    "/",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
    description="Create a new project entry.",
    operation_id="create_project",
)
async def create_project(payload: ProjectCreate, session: AsyncSession = Depends(get_db_session)):
    """Create project."""
    obj = Project(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{project_id}",
    response_model=ProjectOut,
    summary="Update a project",
    description="Update an existing project entry.",
    operation_id="update_project",
)
async def update_project(project_id: int, payload: ProjectUpdate, session: AsyncSession = Depends(get_db_session)):
    """Update project."""
    obj = await session.get(Project, project_id)
    if not obj:
        raise not_found("Project not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete a project entry by id.",
    operation_id="delete_project",
)
async def delete_project(project_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete project."""
    obj = await session.get(Project, project_id)
    if not obj:
        raise not_found("Project not found")
    await session.delete(obj)
    await session.commit()
    return None
