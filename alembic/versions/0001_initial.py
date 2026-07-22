"""initial schema

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # SQLAlchemy creates each named enum as the owning table is created.
    # Creating them explicitly as well would issue CREATE TYPE twice on PostgreSQL.
    ticket_status = sa.Enum("backlog", "todo", "in_progress", "in_review", "done", name="ticketstatus")
    ticket_priority = sa.Enum("low", "medium", "high", "urgent", name="ticketpriority")
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("full_name", sa.String(120), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.UniqueConstraint("email"))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("description", sa.Text()), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.create_table("tickets", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(200), nullable=False), sa.Column("description", sa.Text()), sa.Column("status", ticket_status, nullable=False, server_default="backlog"), sa.Column("priority", ticket_priority, nullable=False, server_default="medium"), sa.Column("assignee_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("reporter_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.create_table("ticket_history", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("ticket_id", sa.Integer(), sa.ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False), sa.Column("field_changed", sa.String(50), nullable=False), sa.Column("old_value", sa.String(255)), sa.Column("new_value", sa.String(255)), sa.Column("changed_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False), sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))


def downgrade() -> None:
    op.drop_table("ticket_history"); op.drop_table("tickets"); op.drop_table("projects"); op.drop_index("ix_users_email", table_name="users"); op.drop_table("users")
