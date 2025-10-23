"""add chat_session and chat_message tables

Revision ID: 2156796338a0
Revises:
Create Date: 2025-10-23 19:02:51.743920

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "2156796338a0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

sender_type_enum = postgresql.ENUM("USER", "AI", name="sender_type_enum", create_type=False)


def upgrade() -> None:
    sender_type_enum.create(op.get_bind())

    op.create_table(
        "chat_session",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("is_favorite", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_chat_session_user_id_created_at", "chat_session", ["user_id", "created_at"], unique=False)

    op.create_table(
        "chat_message",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.Column("sender", sender_type_enum, nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column(
            "context",
            postgresql.JSONB(none_as_null=True, astext_type=sa.Text()),
            server_default="{}",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["session_id"], ["chat_session.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_chat_message_session_id_created_at", "chat_message", ["session_id", "created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_chat_message_session_id_created_at", table_name="chat_message")
    op.drop_table("chat_message")
    op.drop_index("ix_chat_session_user_id_created_at", table_name="chat_session")
    op.drop_table("chat_session")
    sender_type_enum.drop(op.get_bind())
