# backend/alembic/versions/001_initial.py
from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'job_searches',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_title', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('is_remote', sa.Boolean(), default=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('total_jobs_found', sa.Integer(), default=0),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'jobs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('search_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('salary', sa.String()),
        sa.Column('is_remote', sa.Boolean(), default=False),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('requirements', sa.JSON()),
        sa.Column('technologies', sa.JSON()),
        sa.Column('experience_level', sa.String()),
        sa.Column('benefits', sa.JSON()),
        sa.Column('date_posted', sa.DateTime()),
        sa.Column('date_scraped', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['search_id'], ['job_searches.id'])
    )

    op.create_table(
        'applications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('tailored_resume', sa.Text(), nullable=False),
        sa.Column('cover_letter', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'])
    )

def downgrade():
    op.drop_table('applications')
    op.drop_table('jobs')
    op.drop_table('job_searches')
