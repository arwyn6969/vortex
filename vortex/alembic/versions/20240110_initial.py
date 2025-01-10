"""Initial database migration.

Revision ID: 20240110_initial
Revises: 
Create Date: 2024-01-10 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic
revision = '20240110_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create assets table
    op.create_table(
        'assets',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('asset_type', sa.String(), nullable=False),
        sa.Column('creator_id', UUID(as_uuid=True), nullable=True),
        sa.Column('creation_date', sa.DateTime(), nullable=False),
        sa.Column('last_modified', sa.DateTime(), nullable=False),
        sa.Column('tags', JSONB, nullable=False),
        sa.Column('properties', JSONB, nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('content_data', JSONB, nullable=True),
        sa.Column('content_type', sa.String(), nullable=True),
        sa.Column('content_size', sa.Integer(), nullable=True),
        sa.Column('content_checksum', sa.String(), nullable=True)
    )
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('sender_id', UUID(as_uuid=True), nullable=False),
        sa.Column('scene_id', UUID(as_uuid=True), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('metadata', JSONB, nullable=False),
        sa.Column('recipient_ids', JSONB, nullable=False),
        sa.Column('read_by', JSONB, nullable=False)
    )
    
    # Create agents table
    op.create_table(
        'agents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('zone_id', UUID(as_uuid=True), nullable=True),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('experience', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('metadata', JSONB, nullable=False),
        sa.Column('skill_levels', JSONB, nullable=False)
    )
    
    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('task_type', sa.String(), nullable=False),
        sa.Column('assigned_agent_id', UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('metadata', JSONB, nullable=False),
        sa.Column('result', sa.Text(), nullable=True)
    )
    
    # Create agent_skills association table
    op.create_table(
        'agent_skills',
        sa.Column('agent_id', UUID(as_uuid=True), sa.ForeignKey('agents.id')),
        sa.Column('skill', sa.String())
    )
    
    # Create task_required_skills association table
    op.create_table(
        'task_required_skills',
        sa.Column('task_id', UUID(as_uuid=True), sa.ForeignKey('tasks.id')),
        sa.Column('skill', sa.String())
    )
    
    # Create indexes
    op.create_index('ix_assets_asset_type', 'assets', ['asset_type'])
    op.create_index('ix_assets_creator_id', 'assets', ['creator_id'])
    op.create_index('ix_assets_is_deleted', 'assets', ['is_deleted'])
    
    op.create_index('ix_messages_sender_id', 'messages', ['sender_id'])
    op.create_index('ix_messages_scene_id', 'messages', ['scene_id'])
    op.create_index('ix_messages_status', 'messages', ['status'])
    op.create_index('ix_messages_timestamp', 'messages', ['timestamp'])
    
    op.create_index('ix_agents_zone_id', 'agents', ['zone_id'])
    op.create_index('ix_agents_level', 'agents', ['level'])
    op.create_index('ix_agents_status', 'agents', ['status'])
    
    op.create_index('ix_tasks_assigned_agent_id', 'tasks', ['assigned_agent_id'])
    op.create_index('ix_tasks_status', 'tasks', ['status'])
    op.create_index('ix_tasks_created_at', 'tasks', ['created_at'])

def downgrade():
    # Drop indexes
    op.drop_index('ix_tasks_created_at')
    op.drop_index('ix_tasks_status')
    op.drop_index('ix_tasks_assigned_agent_id')
    
    op.drop_index('ix_agents_status')
    op.drop_index('ix_agents_level')
    op.drop_index('ix_agents_zone_id')
    
    op.drop_index('ix_messages_timestamp')
    op.drop_index('ix_messages_status')
    op.drop_index('ix_messages_scene_id')
    op.drop_index('ix_messages_sender_id')
    
    op.drop_index('ix_assets_is_deleted')
    op.drop_index('ix_assets_creator_id')
    op.drop_index('ix_assets_asset_type')
    
    # Drop tables
    op.drop_table('task_required_skills')
    op.drop_table('agent_skills')
    op.drop_table('tasks')
    op.drop_table('agents')
    op.drop_table('messages')
    op.drop_table('assets') 