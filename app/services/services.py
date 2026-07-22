from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password
from app.models import Project, Ticket, TicketHistory, User
from app.repositories import repositories as repo


async def register_user(db: AsyncSession, email: str, password: str, full_name: str) -> User:
    if await repo.get_user_by_email(db, email):
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=email, hashed_password=hash_password(password), full_name=full_name)
    db.add(user); await db.commit(); await db.refresh(user)
    return user


async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    user = await repo.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return user


async def require_project(db: AsyncSession, project_id: int) -> Project:
    project = await repo.get_project(db, project_id)
    if not project: raise HTTPException(status_code=404, detail="Project not found")
    return project


def require_owner(project: Project, user: User) -> None:
    if project.owner_id != user.id: raise HTTPException(status_code=403, detail="Only the project owner may perform this action")


async def create_ticket(db: AsyncSession, project_id: int, data, user: User) -> Ticket:
    await require_project(db, project_id)
    ticket = Ticket(project_id=project_id, reporter_id=user.id, **data.model_dump())
    db.add(ticket); await db.commit(); await db.refresh(ticket)
    return ticket


async def update_ticket(db: AsyncSession, ticket: Ticket, data, user: User) -> Ticket:
    changes = data.model_dump(exclude_unset=True)
    tracked = {"status", "priority", "assignee_id"}
    for field, new_value in changes.items():
        old_value = getattr(ticket, field)
        if field in tracked and old_value != new_value:
            db.add(TicketHistory(ticket_id=ticket.id, field_changed=field, old_value=str(getattr(old_value, "value", old_value)) if old_value is not None else None, new_value=str(getattr(new_value, "value", new_value)) if new_value is not None else None, changed_by=user.id))
        setattr(ticket, field, new_value)
    await db.commit(); await db.refresh(ticket)
    return ticket


async def require_ticket(db: AsyncSession, ticket_id: int) -> Ticket:
    ticket = await repo.get_ticket(db, ticket_id)
    if not ticket: raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
