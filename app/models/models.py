import enum
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class TicketStatus(str, enum.Enum):
    backlog = "backlog"
    todo = "todo"
    in_progress = "in_progress"
    in_review = "in_review"
    done = "done"


class TicketPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class User(Timestamped, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)


class Project(Timestamped, Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner: Mapped[User] = relationship()
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Ticket(Timestamped, Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.backlog, nullable=False)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.medium, nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    project: Mapped[Project] = relationship(back_populates="tickets")
    assignee: Mapped[User | None] = relationship(foreign_keys=[assignee_id])
    reporter: Mapped[User] = relationship(foreign_keys=[reporter_id])


class TicketHistory(Base):
    __tablename__ = "ticket_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    field_changed: Mapped[str] = mapped_column(String(50), nullable=False)
    old_value: Mapped[str | None] = mapped_column(String(255))
    new_value: Mapped[str | None] = mapped_column(String(255))
    changed_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
