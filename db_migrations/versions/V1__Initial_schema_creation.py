"""Initial Schema Creation

Create Date: January 6, 2022
Created By : Arpan Mahanty

-- SQL

CREATE TABLE artist (
    pid SERIAL,
    name TEXT NOT NULL,
    CONSTRAINT pk_artist PRIMARY KEY (pid)
);

CREATE TABLE album (
    pid SERIAL,
    title TEXT NOT NULL,
    artist_pid INTEGER NOT NULL,
    CONSTRAINT pk_album PRIMARY KEY (pid),
    CONSTRAINT fk_album_artist FOREIGN KEY (artist_pid) REFERENCES artist (pid)
);

CREATE TABLE track (
    pid SERIAL,
    title TEXT NOT NULL,
    artist_pid INTEGER NOT NULL,
    album_pid INTEGER NOT NULL,
    CONSTRAINT pk_track PRIMARY KEY (pid),
    CONSTRAINT fk_track_artist FOREIGN KEY (artist_pid) REFERENCES artist (pid),
    CONSTRAINT fk_track_album FOREIGN KEY (album_pid) REFERENCES album (pid)
);

"""

import sqlalchemy as sa
from alembic import op

revision = 'V1'
down_revision = None


def upgrade():
    # Create new 'artist' table
    op.create_table(
        'artist',
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.PrimaryKeyConstraint('pid', name='pk_artist'),
    )

    # Create new 'album' table
    op.create_table(
        'album',
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('artist_pid', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('pid', name='pk_album'),
        sa.ForeignKeyConstraint(('artist_pid',), refcolumns=('artist.pid',), name='fk_album_artist'),
    )

    # Create new 'track' table
    op.create_table(
        'track',
        sa.Column('pid', sa.Integer, autoincrement=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('artist_pid', sa.Integer, nullable=False),
        sa.Column('album_pid', sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint('pid', name='pk_track'),
        sa.ForeignKeyConstraint(('artist_pid',), refcolumns=('artist.pid',), name='fk_track_artist'),
        sa.ForeignKeyConstraint(('album_pid',), refcolumns=('album.pid',), name='fk_track_album'),
    )


def downgrade():
    # Drop 'track' table
    op.drop_table('track')

    # Drop 'album' table
    op.drop_table('album')

    # Drop 'artist' table
    op.drop_table('artist')
