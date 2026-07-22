from fastapi import APIRouter, Query, Response, status
from app.api.deps import CurrentUser, DBSession
from app.models import Project
from app.repositories import repositories as repo
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from app.services import services

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, db: DBSession, user: CurrentUser):
    project = Project(owner_id=user.id, **data.model_dump())
    db.add(project); await db.commit(); await db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def get_projects(db: DBSession, user: CurrentUser, skip: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return await repo.list_projects(db, skip, limit)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, db: DBSession, user: CurrentUser):
    return await services.require_project(db, project_id)


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, data: ProjectUpdate, db: DBSession, user: CurrentUser):
    project = await services.require_project(db, project_id); services.require_owner(project, user)
    for field, value in data.model_dump(exclude_unset=True).items(): setattr(project, field, value)
    await db.commit(); await db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: DBSession, user: CurrentUser):
    project = await services.require_project(db, project_id); services.require_owner(project, user)
    await db.delete(project); await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
