"""SQLAlchemy models for the Vortex system."""

from datetime import datetime
from typing import Dict, List, Optional, Set
from uuid import UUID

from sqlalchemy import (
    Column, DateTime, Enum, ForeignKey, Integer, String, Table, Text, Boolean,
    JSON, Float
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association tables
agent_skills = Table(
    'agent_skills',
    Base.metadata,
    Column('agent_id', PGUUID(as_uuid=True), ForeignKey('agents.id')),
    Column('skill', String)
)

task_required_skills = Table(
    'task_required_skills',
    Base.metadata,
    Column('task_id', PGUUID(as_uuid=True), ForeignKey('tasks.id')),
    Column('skill', String)
)

class Asset(Base):
    """Database model for assets."""
    __tablename__ = 'assets'
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    asset_type = Column(String, nullable=False)
    creator_id = Column(PGUUID(as_uuid=True), nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_modified = Column(DateTime, nullable=False, default=datetime.utcnow)
    tags = Column(JSON, nullable=False, default=list)
    properties = Column(JSON, nullable=False, default=dict)
    is_deleted = Column(Boolean, nullable=False, default=False)
    
    # Asset content
    content_data = Column(JSON, nullable=True)
    content_type = Column(String, nullable=True)
    content_size = Column(Integer, nullable=True)
    content_checksum = Column(String, nullable=True)

class Message(Base):
    """Database model for messages."""
    __tablename__ = 'messages'
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    sender_id = Column(PGUUID(as_uuid=True), nullable=False)
    scene_id = Column(PGUUID(as_uuid=True), nullable=True)
    content = Column(Text, nullable=False)
    message_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default='PENDING')
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    metadata = Column(JSON, nullable=False, default=dict)
    
    # Recipients and read status
    recipient_ids = Column(JSON, nullable=False)  # List of UUIDs
    read_by = Column(JSON, nullable=False, default=list)  # List of UUIDs

class Agent(Base):
    """Database model for AI agents."""
    __tablename__ = 'agents'
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    zone_id = Column(PGUUID(as_uuid=True), nullable=True)
    level = Column(Integer, nullable=False, default=1)
    experience = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default='IDLE')
    metadata = Column(JSON, nullable=False, default=dict)
    skill_levels = Column(JSON, nullable=False, default=dict)
    
    # Relationships
    skills = relationship('AgentSkill', secondary=agent_skills)
    tasks = relationship('Task', back_populates='assigned_agent')

class Task(Base):
    """Database model for agent tasks."""
    __tablename__ = 'tasks'
    
    id = Column(PGUUID(as_uuid=True), primary_key=True)
    task_type = Column(String, nullable=False)
    assigned_agent_id = Column(PGUUID(as_uuid=True), ForeignKey('agents.id'), nullable=True)
    status = Column(String, nullable=False, default='PENDING')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=False, default=dict)
    result = Column(Text, nullable=True)
    
    # Relationships
    assigned_agent = relationship('Agent', back_populates='tasks')
    required_skills = relationship('AgentSkill', secondary=task_required_skills)

# Indexes and constraints will be added in migrations 