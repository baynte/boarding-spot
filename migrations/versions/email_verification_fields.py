"""Add email verification fields

Revision ID: email_verification_fields
Revises: 156f7fd3026c
Create Date: 2023-07-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'email_verification_fields'
down_revision = '156f7fd3026c'  # Updated to the previous migration ID
branch_labels = None
depends_on = None


def upgrade():
    # Add email verification fields to the user table
    op.add_column('user', sa.Column('is_email_verified', sa.Boolean(), nullable=False, server_default='0'))
    op.add_column('user', sa.Column('verification_token', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('token_expiry', sa.DateTime(), nullable=True))
    
    # Note: We're not adding a unique constraint on verification_token due to SQLite limitations
    # The uniqueness will be enforced at the application level


def downgrade():
    # Remove email verification fields from the user table
    op.drop_column('user', 'is_email_verified')
    op.drop_column('user', 'verification_token')
    op.drop_column('user', 'token_expiry') 