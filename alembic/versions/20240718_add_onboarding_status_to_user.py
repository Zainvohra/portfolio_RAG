"""add onboarding_status to user table

Revision ID: 20240718_add_onboarding_status
Revises: ee4a3afe77b4
Create Date: 2024-07-18
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20240718_add_onboarding_status'
down_revision = 'ee4a3afe77b4'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('onboarding_status', sa.String(length=20), nullable=True, server_default='pending'))

def downgrade():
    op.drop_column('user', 'onboarding_status') 