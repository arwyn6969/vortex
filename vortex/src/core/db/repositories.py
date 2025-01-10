"""Repository classes for database operations."""

from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from uuid import UUID

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from .models import Asset, Message, Agent, Task

class AssetRepository:
    """Repository for asset operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        asset_type: str,
        content: Any,
        content_type: str,
        creator_id: Optional[UUID] = None,
        properties: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Asset:
        """Create a new asset."""
        asset = Asset(
            asset_type=asset_type,
            creator_id=creator_id,
            content_data=content,
            content_type=content_type,
            content_size=len(str(content)),
            content_checksum=str(hash(str(content))),
            properties=properties or {},
            tags=tags or []
        )
        self.session.add(asset)
        self.session.flush()
        return asset
    
    def get_by_id(self, asset_id: UUID) -> Optional[Asset]:
        """Get an asset by ID."""
        return self.session.query(Asset).filter(
            and_(Asset.id == asset_id, Asset.is_deleted.is_(False))
        ).first()
    
    def update(
        self,
        asset_id: UUID,
        content: Optional[Any] = None,
        properties: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Asset]:
        """Update an asset."""
        asset = self.get_by_id(asset_id)
        if not asset:
            return None
            
        if content is not None:
            asset.content_data = content
            asset.content_size = len(str(content))
            asset.content_checksum = str(hash(str(content)))
            
        if properties is not None:
            asset.properties.update(properties)
            
        if tags is not None:
            asset.tags = tags
            
        asset.last_modified = datetime.utcnow()
        self.session.flush()
        return asset
    
    def delete(self, asset_id: UUID) -> bool:
        """Mark an asset as deleted."""
        asset = self.get_by_id(asset_id)
        if not asset:
            return False
            
        asset.is_deleted = True
        asset.last_modified = datetime.utcnow()
        self.session.flush()
        return True
    
    def query(
        self,
        asset_type: Optional[str] = None,
        tags: Optional[List[str]] = None,
        creator_id: Optional[UUID] = None
    ) -> List[Asset]:
        """Query assets based on criteria."""
        query = self.session.query(Asset).filter(Asset.is_deleted.is_(False))
        
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        if tags:
            for tag in tags:
                query = query.filter(Asset.tags.contains([tag]))
        if creator_id:
            query = query.filter(Asset.creator_id == creator_id)
            
        return query.order_by(Asset.last_modified.desc()).all()

class MessageRepository:
    """Repository for message operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        sender_id: UUID,
        recipient_ids: Set[UUID],
        content: str,
        message_type: str,
        scene_id: Optional[UUID] = None,
        metadata: Optional[Dict] = None
    ) -> Message:
        """Create a new message."""
        message = Message(
            sender_id=sender_id,
            recipient_ids=list(recipient_ids),
            content=content,
            message_type=message_type,
            scene_id=scene_id,
            status='DELIVERED',
            metadata=metadata or {}
        )
        self.session.add(message)
        self.session.flush()
        return message
    
    def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID."""
        return self.session.query(Message).filter(
            Message.id == message_id
        ).first()
    
    def get_user_messages(
        self,
        user_id: UUID,
        since: Optional[datetime] = None,
        message_type: Optional[str] = None,
        include_archived: bool = False
    ) -> List[Message]:
        """Get messages for a user."""
        query = self.session.query(Message).filter(
            or_(
                Message.sender_id == user_id,
                Message.recipient_ids.contains([str(user_id)])
            )
        )
        
        if not include_archived:
            query = query.filter(Message.status != 'ARCHIVED')
        query = query.filter(Message.status != 'DELETED')
        
        if since:
            query = query.filter(Message.timestamp >= since)
        if message_type:
            query = query.filter(Message.message_type == message_type)
            
        return query.order_by(Message.timestamp.desc()).all()
    
    def mark_read(self, message_id: UUID, user_id: UUID) -> bool:
        """Mark a message as read by a user."""
        message = self.get_by_id(message_id)
        if not message:
            return False
            
        if str(user_id) not in message.read_by:
            message.read_by.append(str(user_id))
            if set(message.read_by) == set(message.recipient_ids):
                message.status = 'READ'
            self.session.flush()
            
        return True

class AgentRepository:
    """Repository for agent operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        name: str,
        skills: Set[str],
        zone_id: Optional[UUID] = None,
        level: int = 1,
        metadata: Optional[Dict] = None
    ) -> Agent:
        """Create a new agent."""
        agent = Agent(
            name=name,
            zone_id=zone_id,
            level=level,
            skill_levels={skill: 1 for skill in skills},
            metadata=metadata or {}
        )
        agent.skills = list(skills)
        self.session.add(agent)
        self.session.flush()
        return agent
    
    def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Get an agent by ID."""
        return self.session.query(Agent).filter(Agent.id == agent_id).first()
    
    def find_agents(
        self,
        required_skills: Optional[Set[str]] = None,
        zone_id: Optional[UUID] = None,
        min_level: Optional[int] = None,
        available_only: bool = False
    ) -> List[Agent]:
        """Find agents matching criteria."""
        query = self.session.query(Agent)
        
        if required_skills:
            for skill in required_skills:
                query = query.filter(Agent.skills.contains([skill]))
                
        if zone_id:
            query = query.filter(Agent.zone_id == zone_id)
            
        if min_level:
            query = query.filter(Agent.level >= min_level)
            
        if available_only:
            query = query.filter(Agent.status == 'IDLE')
            
        return query.order_by(Agent.level.desc()).all()
    
    def update_experience(
        self,
        agent_id: UUID,
        amount: int,
        skill: Optional[str] = None
    ) -> bool:
        """Update an agent's experience."""
        agent = self.get_by_id(agent_id)
        if not agent:
            return False
            
        agent.experience += amount
        
        if skill and skill in agent.skills:
            current_level = agent.skill_levels.get(skill, 1)
            new_level = 1 + (current_level * amount) // 100
            if new_level > current_level:
                agent.skill_levels[skill] = new_level
                
        new_level = 1 + agent.experience // 100
        if new_level > agent.level:
            agent.level = new_level
            
        self.session.flush()
        return True

class TaskRepository:
    """Repository for task operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(
        self,
        task_type: str,
        required_skills: Set[str],
        metadata: Optional[Dict] = None
    ) -> Task:
        """Create a new task."""
        task = Task(
            task_type=task_type,
            status='PENDING',
            metadata=metadata or {}
        )
        task.required_skills = list(required_skills)
        self.session.add(task)
        self.session.flush()
        return task
    
    def get_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get a task by ID."""
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def assign(self, task_id: UUID, agent_id: UUID) -> bool:
        """Assign a task to an agent."""
        task = self.get_by_id(task_id)
        if not task or task.status != 'PENDING':
            return False
            
        task.assigned_agent_id = agent_id
        task.status = 'IN_PROGRESS'
        task.started_at = datetime.utcnow()
        self.session.flush()
        return True
    
    def complete(
        self,
        task_id: UUID,
        result: Optional[str] = None,
        success: bool = True
    ) -> bool:
        """Mark a task as completed."""
        task = self.get_by_id(task_id)
        if not task or task.status not in ['PENDING', 'IN_PROGRESS']:
            return False
            
        task.status = 'COMPLETED' if success else 'FAILED'
        task.completed_at = datetime.utcnow()
        task.result = result
        self.session.flush()
        return True 