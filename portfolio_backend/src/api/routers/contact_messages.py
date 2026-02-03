from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.routers.common import not_found, pagination_params
from src.db.session import get_db_session
from src.models import ContactMessage
from src.schemas import ContactMessageCreate, ContactMessageOut, ContactMessageUpdate

router = APIRouter(prefix="/contact-messages", tags=["Contact"])


@router.get(
    "/",
    response_model=list[ContactMessageOut],
    summary="List contact messages",
    description="Return a list of contact messages (admin view).",
    operation_id="list_contact_messages",
)
async def list_contact_messages(
    pagination: tuple[int, int] = Depends(pagination_params),
    session: AsyncSession = Depends(get_db_session),
):
    """List contact messages."""
    limit, offset = pagination
    result = await session.execute(
        select(ContactMessage).order_by(ContactMessage.id.desc()).limit(limit).offset(offset)
    )
    return list(result.scalars().all())


@router.get(
    "/{message_id}",
    response_model=ContactMessageOut,
    summary="Get a contact message",
    description="Fetch a contact message by id.",
    operation_id="get_contact_message",
)
async def get_contact_message(message_id: int, session: AsyncSession = Depends(get_db_session)):
    """Get contact message by id."""
    obj = await session.get(ContactMessage, message_id)
    if not obj:
        raise not_found("Contact message not found")
    return obj


@router.post(
    "/",
    response_model=ContactMessageOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a contact message",
    description="Submit a new contact message (public contact form).",
    operation_id="create_contact_message",
)
async def create_contact_message(payload: ContactMessageCreate, session: AsyncSession = Depends(get_db_session)):
    """Create contact message."""
    obj = ContactMessage(**payload.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


@router.put(
    "/{message_id}",
    response_model=ContactMessageOut,
    summary="Update a contact message",
    description="Update an existing contact message entry (admin).",
    operation_id="update_contact_message",
)
async def update_contact_message(
    message_id: int, payload: ContactMessageUpdate, session: AsyncSession = Depends(get_db_session)
):
    """Update contact message."""
    obj = await session.get(ContactMessage, message_id)
    if not obj:
        raise not_found("Contact message not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    for k, v in updates.items():
        setattr(obj, k, v)

    await session.commit()
    await session.refresh(obj)
    return obj


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a contact message",
    description="Delete a contact message entry by id (admin).",
    operation_id="delete_contact_message",
)
async def delete_contact_message(message_id: int, session: AsyncSession = Depends(get_db_session)):
    """Delete contact message."""
    obj = await session.get(ContactMessage, message_id)
    if not obj:
        raise not_found("Contact message not found")
    await session.delete(obj)
    await session.commit()
    return None
