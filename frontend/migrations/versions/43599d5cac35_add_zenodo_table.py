"""add zenodo table

Revision ID: 43599d5cac35
Revises: ad7a403de905
Create Date: 2019-07-22 12:05:50.105352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43599d5cac35'
down_revision = 'ad7a403de905'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('zenodo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('deposit_id', sa.Integer(), nullable=False),
    sa.Column('dump_id', sa.Integer(), nullable=False),
    sa.Column('doi', sa.Text(), nullable=False),
    sa.Column('target', sa.Enum('SANDBOX', 'RELEASE', name='zenodotarget'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('started_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('uploaded_bytes', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['dump_id'], ['dump.id'], name=op.f('fk_zenodo_dump_id_dump')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_zenodo'))
    )
    op.add_column('dump', sa.Column('compressed_size', sa.Integer(), server_default=sa.text('0'), nullable=False))
    op.add_column('dump', sa.Column('entity_count', sa.Integer(), server_default=sa.text('0'), nullable=False))
    op.add_column('dump_error', sa.Column('zenodo_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_dump_error_zenodo_id_zenodo'), 'dump_error', 'zenodo', ['zenodo_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_dump_error_zenodo_id_zenodo'), 'dump_error', type_='foreignkey')
    op.drop_column('dump_error', 'zenodo_id')
    op.drop_column('dump', 'entity_count')
    op.drop_column('dump', 'compressed_size')
    op.drop_table('zenodo')
    # ### end Alembic commands ###
