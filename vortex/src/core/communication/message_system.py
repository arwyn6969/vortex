"""Message system for handling communication between players and AI agents."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Set
from uuid import UUID, uuid4
from ..redis_config import RedisConfig
from .. import redis_service

class MessageType(Enum):
    """Types of messages that can be sent."""
    DIRECT = auto()
    SCENE = auto()
    AI_MEDIATED = auto()
    SYSTEM = auto()

class MessageStatus(Enum):
    """Status of a message in the system."""
    PENDING = auto()
    DELIVERED = auto()
    READ = auto()
    ARCHIVED = auto()
    DELETED = auto()

@dataclass
class Message:
    """Represents a message in the system."""
    message_id: UUID
    sender_id: UUID
    recipient_ids: Set[UUID]
    content: str
    message_type: MessageType
    scene_id: Optional[UUID]
    timestamp: datetime
    status: MessageStatus = MessageStatus.PENDING
    read_by: Set[UUID] = field(default_factory=set)
    metadata: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert message to dictionary for serialization."""
        return {
            "message_id": str(self.message_id),
            "sender_id": str(self.sender_id),
            "recipient_ids": [str(rid) for rid in self.recipient_ids],
            "content": self.content,
            "message_type": self.message_type.name,
            "scene_id": str(self.scene_id) if self.scene_id else None,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.name,
            "read_by": [str(uid) for uid in self.read_by],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create message from dictionary."""
        return cls(
            message_id=UUID(data["message_id"]),
            sender_id=UUID(data["sender_id"]),
            recipient_ids={UUID(rid) for rid in data["recipient_ids"]},
            content=data["content"],
            message_type=MessageType[data["message_type"]],
            scene_id=UUID(data["scene_id"]) if data["scene_id"] else None,
            timestamp=datetime.fromisoformat(data["timestamp"]),
            status=MessageStatus[data["status"]],
            read_by={UUID(uid) for uid in data["read_by"]},
            metadata=data["metadata"]
        )

class MessageSystem:
    """Handles all communication within the game."""
    
    MAX_MESSAGE_SIZE = 10000  # Maximum message size in characters
    MESSAGE_TTL = timedelta(days=30)  # Time to live for messages
    
    def __init__(self):
        self._messages: Dict[UUID, Message] = {}
        self._user_inbox: Dict[UUID, List[UUID]] = {}
        self._scene_messages: Dict[UUID, List[UUID]] = {}
        self._archived_messages: Dict[UUID, List[UUID]] = {}
    
    def send_message(
        self,
        sender_id: UUID,
        recipient_ids: Set[UUID],
        content: str,
        message_type: MessageType,
        scene_id: Optional[UUID] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[UUID]:
        """Send a message to one or more recipients."""
        # Validate message size
        if len(content) > self.MAX_MESSAGE_SIZE:
            return None
        
        message_id = uuid4()
        message = Message(
            message_id=message_id,
            sender_id=sender_id,
            recipient_ids=recipient_ids,
            content=content,
            message_type=message_type,
            scene_id=scene_id,
            timestamp=datetime.utcnow(),
            status=MessageStatus.DELIVERED,
            metadata=metadata or {}
        )
        
        # Store in memory
        self._messages[message_id] = message
        
        # Store in Redis cache
        cache_key = RedisConfig.MESSAGE_CACHE.format(message_id=str(message_id))
        redis_service.cache_set(
            cache_key,
            message.to_dict(),
            ttl=int(self.MESSAGE_TTL.total_seconds())
        )
        
        # Queue message for processing
        redis_service.queue_push(
            RedisConfig.MESSAGE_QUEUE,
            {
                "type": "new_message",
                "message": message.to_dict()
            }
        )
        
        # Store in recipients' inboxes
        for recipient_id in recipient_ids:
            if recipient_id not in self._user_inbox:
                self._user_inbox[recipient_id] = []
            self._user_inbox[recipient_id].append(message_id)
        
        # Store in scene if applicable
        if scene_id:
            if scene_id not in self._scene_messages:
                self._scene_messages[scene_id] = []
            self._scene_messages[scene_id].append(message_id)
            
            # Publish scene update
            redis_service.publish(
                RedisConfig.POND_UPDATES,
                {
                    "type": "new_message",
                    "scene_id": str(scene_id),
                    "message": message.to_dict()
                }
            )
        
        return message_id
    
    def get_message(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID with Redis caching."""
        # Try Redis cache first
        cache_key = RedisConfig.MESSAGE_CACHE.format(message_id=str(message_id))
        cached_message = redis_service.cache_get(cache_key)
        
        if cached_message:
            return Message.from_dict(cached_message)
        
        # If not in cache, get from memory
        message = self._messages.get(message_id)
        
        # Cache if found
        if message:
            redis_service.cache_set(
                cache_key,
                message.to_dict(),
                ttl=int(self.MESSAGE_TTL.total_seconds())
            )
        
        return message

    def get_user_messages(
        self,
        user_id: UUID,
        since: Optional[datetime] = None,
        message_type: Optional[MessageType] = None,
        include_archived: bool = False
    ) -> List[Message]:
        """Retrieve messages for a user with optional filtering."""
        message_ids = self._user_inbox.get(user_id, []).copy()
        if include_archived:
            message_ids.extend(self._archived_messages.get(user_id, []))
            
        if not message_ids:
            return []
            
        messages = []
        for message_id in message_ids:
            message = self.get_message(message_id)  # Use cached get_message
            if not message or message.status == MessageStatus.DELETED:
                continue
            if since and message.timestamp < since:
                continue
            if message_type and message.message_type != message_type:
                continue
            messages.append(message)
            
        return sorted(messages, key=lambda m: m.timestamp, reverse=True)
    
    def get_scene_messages(
        self,
        scene_id: UUID,
        since: Optional[datetime] = None,
        include_archived: bool = False
    ) -> List[Message]:
        """Retrieve all messages from a specific scene."""
        if scene_id not in self._scene_messages:
            return []
            
        messages = []
        for message_id in self._scene_messages[scene_id]:
            if message_id not in self._messages:
                continue
                
            message = self._messages[message_id]
            if not include_archived and message.status == MessageStatus.ARCHIVED:
                continue
            if message.status == MessageStatus.DELETED:
                continue
            if since and message.timestamp < since:
                continue
            messages.append(message)
            
        return sorted(messages, key=lambda m: m.timestamp)
    
    def mark_messages_read(
        self,
        user_id: UUID,
        message_ids: List[UUID]
    ) -> None:
        """Mark messages as read for a user."""
        for message_id in message_ids:
            if message_id in self._messages:
                message = self._messages[message_id]
                message.read_by.add(user_id)
                if message.read_by == message.recipient_ids:
                    message.status = MessageStatus.READ
    
    def archive_messages(
        self,
        user_id: UUID,
        message_ids: List[UUID]
    ) -> None:
        """Archive messages for a user."""
        if user_id not in self._archived_messages:
            self._archived_messages[user_id] = []
            
        for message_id in message_ids:
            if message_id in self._messages and message_id in self._user_inbox.get(user_id, []):
                self._user_inbox[user_id].remove(message_id)
                self._archived_messages[user_id].append(message_id)
                message = self._messages[message_id]
                if all(
                    mid in self._archived_messages.get(rid, [])
                    for rid in message.recipient_ids
                ):
                    message.status = MessageStatus.ARCHIVED
    
    def delete_messages(
        self,
        user_id: UUID,
        message_ids: List[UUID]
    ) -> None:
        """Delete messages for a user."""
        for message_id in message_ids:
            if message_id in self._messages:
                message = self._messages[message_id]
                # Only allow deletion if user is sender or recipient
                if user_id == message.sender_id or user_id in message.recipient_ids:
                    message.status = MessageStatus.DELETED
                    # Remove from all storage locations
                    for inbox in [self._user_inbox, self._archived_messages]:
                        if user_id in inbox and message_id in inbox[user_id]:
                            inbox[user_id].remove(message_id)
    
    def cleanup_old_messages(self, before: Optional[datetime] = None) -> int:
        """Clean up old messages. Returns number of messages cleaned up."""
        if before is None:
            before = datetime.utcnow() - self.MESSAGE_TTL
            
        cleaned = 0
        for message_id, message in list(self._messages.items()):
            if message.timestamp < before:
                self.delete_messages(message.sender_id, [message_id])
                cleaned += 1
                
        return cleaned 