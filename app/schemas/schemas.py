from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import TicketPriority, TicketStatus


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=120)


class UserRead(ORMModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=5000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=5000)


class ProjectRead(ORMModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime


class TicketCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10000)
    status: TicketStatus = TicketStatus.backlog
    priority: TicketPriority = TicketPriority.medium
    assignee_id: int | None = None


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=10000)
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    assignee_id: int | None = None


class TicketRead(ORMModel):
    id: int
    project_id: int
    title: str
    description: str | None
    status: TicketStatus
    priority: TicketPriority
    assignee_id: int | None
    reporter_id: int
    created_at: datetime
    updated_at: datetime


class TicketHistoryRead(ORMModel):
    id: int
    ticket_id: int
    field_changed: str
    old_value: str | None
    new_value: str | None
    changed_by: int
    changed_at: datetime
