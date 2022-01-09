"""Initial Schema Creation

Create Date: January 6, 2022
Created By : Arpan Mahanty

-- SQL

CREATE TABLE artist (
    pid SERIAL,
    name TEXT NOT NULL,
    CONSTRAINT pk_artist PRIMARY KEY (pid),
    CONSTRAINT uc_artist_name UNIQUE (name)
);

CREATE TABLE album (
    pid SERIAL,
    title TEXT NOT NULL,
    artist_pid INTEGER NOT NULL,
    CONSTRAINT pk_album PRIMARY KEY (pid),
    CONSTRAINT fk_album_artist FOREIGN KEY (artist_pid) REFERENCES artist (pid),
    CONSTRAINT uc_album_title_artist UNIQUE (title, artist_pid)
);

CREATE TABLE track (
    pid SERIAL,
    title TEXT NOT NULL,
    artist_pid INTEGER NOT NULL,
    album_pid INTEGER,
    CONSTRAINT pk_track PRIMARY KEY (pid),
    CONSTRAINT fk_track_artist FOREIGN KEY (artist_pid) REFERENCES artist (pid),
    CONSTRAINT fk_track_album FOREIGN KEY (album_pid) REFERENCES album (pid),
    CONSTRAINT uc_track_title_artist UNIQUE (title, artist_pid)
);

"""

import sqlalchemy as sa
from alembic import op

revision = 'V1'
down_revision = None


def upgrade():
    # Create new 'artist' table
    op.create_table(
        'artist',  # Table Name
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('name', sa.Text, nullable=False),

        # Constraints Definition
        sa.PrimaryKeyConstraint('pid', name='pk_artist'),  # Primary Key
        sa.UniqueConstraint('name', name='uc_artist_name'),
    )

    # Create new 'album' table
    op.create_table(
        'album',  # Table Name
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('artist_pid', sa.Integer, nullable=False),

        # Constraints Definition
        sa.PrimaryKeyConstraint('pid', name='pk_album'),  # Primary Key
        sa.ForeignKeyConstraint(('artist_pid',), refcolumns=('artist.pid',), name='fk_album_artist'),
        sa.UniqueConstraint('title', 'artist_pid', name='uc_album_title_artist'),
    )

    # Create new 'track' table
    op.create_table(
        'track',  # Table Name
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('artist_pid', sa.Integer, nullable=False),
        sa.Column('album_pid', sa.Integer),

        # Constraints Definition
        sa.PrimaryKeyConstraint('pid', name='pk_track'),  # Primary Key
        sa.ForeignKeyConstraint(('artist_pid',), refcolumns=('artist.pid',), name='fk_track_artist'),
        sa.ForeignKeyConstraint(('album_pid',), refcolumns=('album.pid',), name='fk_track_album'),
        sa.UniqueConstraint('title', 'artist_pid', name='uc_track_title_artist'),
    )


def downgrade():
    # Drop 'track' table
    op.drop_table('track')

    # Drop 'album' table
    op.drop_table('album')

    # Drop 'artist' table
    op.drop_table('artist')
