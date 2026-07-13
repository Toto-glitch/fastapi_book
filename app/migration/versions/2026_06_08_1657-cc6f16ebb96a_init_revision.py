"""Init revision

Revision ID: cc6f16ebb96a
Revises:
Create Date: 2026-06-08 16:57:32.327250

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "cc6f16ebb96a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=False),
        sa.Column("last_name", sa.String(length=255), nullable=False),
        sa.Column("father_name", sa.String(length=255), nullable=True),
        sa.Column("birth_year", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_authors")),
    )
    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_genres")),
    )
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["author_id"], ["authors.id"], name=op.f("fk_books_author_id_authors")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )
    op.create_table(
        "book_genres",
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("genre_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name=op.f("fk_book_genres_book_id_books")
        ),
        sa.ForeignKeyConstraint(
            ["genre_id"], ["genres.id"], name=op.f("fk_book_genres_genre_id_genres")
        ),
        sa.PrimaryKeyConstraint("book_id", "genre_id", name=op.f("pk_book_genres")),
    )


def downgrade() -> None:
    op.drop_table("book_genres")
    op.drop_table("books")
    op.drop_table("genres")
    op.drop_table("authors")
