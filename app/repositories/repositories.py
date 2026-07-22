from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Project, Ticket, TicketHistory, User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    return await db.scalar(select(User).where(User.email == email))


async def get_project(db: AsyncSession, project_id: int) -> Project | None:
    return await db.get(Project, project_id)


async def list_projects(db: AsyncSession, skip: int, limit: int) -> list[Project]:
    return list((await db.scalars(select(Project).order_by(Project.id).offset(skip).limit(limit))).all())


async def get_ticket(db: AsyncSession, ticket_id: int) -> Ticket | None:
    return await db.get(Ticket, ticket_id)


async def list_tickets(db: AsyncSession, project_id: int, skip: int, limit: int, status=None, priority=None, assignee_id=None) -> list[Ticket]:
    stmt = select(Ticket).where(Ticket.project_id == project_id)
    if status is not None: stmt = stmt.where(Ticket.status == status)
    if priority is not None: stmt = stmt.where(Ticket.priority == priority)
    if assignee_id is not None: stmt = stmt.where(Ticket.assignee_id == assignee_id)
    return list((await db.scalars(stmt.order_by(Ticket.id).offset(skip).limit(limit))).all())


async def list_history(db: AsyncSession, ticket_id: int) -> list[TicketHistory]:
    return list((await db.scalars(select(TicketHistory).where(TicketHistory.ticket_id == ticket_id).order_by(TicketHistory.id))).all())
