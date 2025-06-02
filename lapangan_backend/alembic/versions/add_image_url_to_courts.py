"""add image_url to courts

Revision ID: add_image_url_to_courts
Revises: 5a1ef589e1f1
Create Date: 2025-06-01 05:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_image_url_to_courts'
down_revision = '5a1ef589e1f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('courts', sa.Column('image_url', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('courts', 'image_url')
