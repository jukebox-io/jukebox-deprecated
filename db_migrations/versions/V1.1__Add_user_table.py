"""Add User Table

Create Date: January 23, 2022
Created By : Arpan Mahanty

-- SQL

CREATE TABLE user (
    pid SERIAL,
    user_name TEXT NOT NULL,
    email TEXT,
    phone_no TEXT,
    hashed_password TEXT NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY (pid),
    CONSTRAINT uc_user_user_name UNIQUE (user_name),
    CONSTRAINT uc_user_email UNIQUE (email),
    CONSTRAINT uc_user_phone_no UNIQUE (phone_no)
);

"""

import sqlalchemy as sa
from alembic import op

revision = 'V1.1'
down_revision = 'V1'


def upgrade():
    # Create new 'user' table
    op.create_table(
        'user',  # Table Name
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('user_name', sa.Text, nullable=False),
        sa.Column('email', sa.Text),
        sa.Column('phone_no', sa.Text),
        sa.Column('hashed_password', sa.Text, nullable=False),

        # Constraints Definition
        sa.PrimaryKeyConstraint('pid', name='pk_user'),  # Primary Key
        sa.UniqueConstraint('user_name', name='uc_user_user_name'),
        sa.UniqueConstraint('email', name='uc_user_email'),
        sa.UniqueConstraint('phone_no', name='uc_user_phone_no'),
    )


def downgrade():
    # Drop 'user' table
    op.drop_table('user')
