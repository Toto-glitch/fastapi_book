"""create_genre_table

Revision ID: 88f9e156a0de
Revises: 03be4d7cebc1
Create Date: 2026-07-17 12:26:24.557404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88f9e156a0de'
down_revision: Union[str, Sequence[str], None] = '03be4d7cebc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('genres',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genres')),
    sa.UniqueConstraint('name', name=op.f('uq_genres_name'))
    )
    op.create_table('book_genres',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_book_genres_book_id_books')),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], name=op.f('fk_book_genres_genre_id_genres')),
    sa.PrimaryKeyConstraint('book_id', 'genre_id', name=op.f('pk_book_genres'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('book_genres')
    op.drop_table('genres')
