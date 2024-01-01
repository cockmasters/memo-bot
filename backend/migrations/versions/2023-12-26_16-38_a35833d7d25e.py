"""empty message

Revision ID: a35833d7d25e
Revises: a98568c2a132
Create Date: 2023-12-26 16:38:51.056969+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a35833d7d25e'
down_revision: Union[str, None] = 'a98568c2a132'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_note_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_note')),
    sa.UniqueConstraint('user_id', name=op.f('uq_note_user_id'))
    )
    op.create_table('tag',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_tag_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tag')),
    sa.UniqueConstraint('name', name=op.f('uq_tag_name')),
    sa.UniqueConstraint('user_id', name=op.f('uq_tag_user_id'))
    )
    op.create_table('notes_tags',
    sa.Column('note_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], name=op.f('fk_notes_tags_note_id_note')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_notes_tags_tag_id_tag')),
    sa.PrimaryKeyConstraint('note_id', 'tag_id', name=op.f('pk_notes_tags'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes_tags')
    op.drop_table('tag')
    op.drop_table('note')
    # ### end Alembic commands ###