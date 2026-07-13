"""Remove tables genres and book_genres

Revision ID: 03be4d7cebc1
Revises: cc6f16ebb96a
Create Date: 2026-06-10 17:09:19.144575

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "03be4d7cebc1"
down_revision: Union[str, Sequence[str], None] = "cc6f16ebb96a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("book_genres")
    op.drop_table("genres")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "genres",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_genres")),
    )
    op.create_table(
        "book_genres",
        sa.Column("book_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("genre_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_genres_book_id_books")
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_book_genres_genre_id_genres")
        ),
        sa.PrimaryKeyConstraint("book_id", "genre_id", name=op.f("pk_book_genres")),
    )
