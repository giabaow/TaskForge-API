from fastapi import APIRouter, Query, Response, status
from app.api.deps import CurrentUser, DBSession
from app.models import TicketPriority, TicketStatus
from app.repositories import repositories as repo
from app.schemas import TicketCreate, TicketHistoryRead, TicketRead, TicketUpdate
from app.services import services

router = APIRouter(tags=["tickets"])


@router.post("/projects/{project_id}/tickets", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
async def create(project_id: int, data: TicketCreate, db: DBSession, user: CurrentUser):
    return await services.create_ticket(db, project_id, data, user)


@router.get("/projects/{project_id}/tickets", response_model=list[TicketRead])
async def list_for_project(project_id: int, db: DBSession, user: CurrentUser, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100), status_filter: TicketStatus | None = Query(None, alias="status"), priority: TicketPriority | None = None, assignee_id: int | None = Query(None, ge=1)):
    await services.require_project(db, project_id)
    return await repo.list_tickets(db, project_id, skip, limit, status_filter, priority, assignee_id)


@router.get("/tickets/{ticket_id}", response_model=TicketRead)
async def get(ticket_id: int, db: DBSession, user: CurrentUser):
    return await services.require_ticket(db, ticket_id)


@router.patch("/tickets/{ticket_id}", response_model=TicketRead)
async def update(ticket_id: int, data: TicketUpdate, db: DBSession, user: CurrentUser):
    return await services.update_ticket(db, await services.require_ticket(db, ticket_id), data, user)


@router.delete("/tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(ticket_id: int, db: DBSession, user: CurrentUser):
    ticket = await services.require_ticket(db, ticket_id)
    await db.delete(ticket); await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/tickets/{ticket_id}/history", response_model=list[TicketHistoryRead])
async def history(ticket_id: int, db: DBSession, user: CurrentUser):
    await services.require_ticket(db, ticket_id)
    return await repo.list_history(db, ticket_id)
