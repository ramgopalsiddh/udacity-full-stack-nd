"""Add many-to-many relationship

Revision ID: a5e5cab7001e
Revises: 35291c8315b4
Create Date: 2023-12-27 23:01:10.559543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5e5cab7001e'
down_revision = '35291c8315b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor_movie_association',
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.drop_constraint('actors_movie_id_fkey', type_='foreignkey')
        batch_op.drop_column('movie_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('actors_movie_id_fkey', 'movies', ['movie_id'], ['id'])

    op.drop_table('actor_movie_association')
    # ### end Alembic commands ###
