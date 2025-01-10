"""AI agent system for handling AI-mediated tasks and communication."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4

class AgentSkill(Enum):
    """Skills that AI agents can possess."""
    COMMUNICATION = auto()
    CRAFTING = auto()
    NAVIGATION = auto()
    COMBAT = auto()
    TRADING = auto()
    TEACHING = auto()
    LORE = auto()

class TaskStatus(Enum):
    """Status of a task in the system."""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()

@dataclass
class Task:
    """Represents a task that can be assigned to an agent."""
    task_id: UUID
    task_type: str
    required_skills: Set[AgentSkill]
    assigned_agent: Optional[UUID]
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    metadata: Dict[str, str]
    result: Optional[str] = None

@dataclass
class AgentProfile:
    """Profile for an AI agent."""
    agent_id: UUID
    name: str
    skills: Set[AgentSkill]
    zone_id: Optional[UUID]
    level: int
    experience: int
    skill_levels: Dict[AgentSkill, int] = field(default_factory=dict)
    current_task: Optional[UUID] = None
    status: str = "IDLE"
    metadata: Dict[str, str] = field(default_factory=dict)

class AgentSystem:
    """Manages AI agents and their interactions."""
    
    MAX_CONCURRENT_TASKS = 3  # Maximum number of tasks an agent can handle
    TASK_TIMEOUT = timedelta(hours=1)  # Default timeout for tasks
    
    def __init__(self):
        self._agents: Dict[UUID, AgentProfile] = {}
        self._zone_agents: Dict[UUID, Set[UUID]] = {}
        self._skill_index: Dict[AgentSkill, Set[UUID]] = {
            skill: set() for skill in AgentSkill
        }
        self._tasks: Dict[UUID, Task] = {}
        self._agent_tasks: Dict[UUID, Set[UUID]] = {}
    
    def register_agent(
        self,
        name: str,
        skills: Set[AgentSkill],
        zone_id: Optional[UUID] = None,
        level: int = 1,
        metadata: Optional[Dict[str, str]] = None
    ) -> UUID:
        """Register a new AI agent in the system."""
        agent_id = uuid4()
        profile = AgentProfile(
            agent_id=agent_id,
            name=name,
            skills=skills,
            zone_id=zone_id,
            level=level,
            experience=0,
            skill_levels={skill: 1 for skill in skills},
            metadata=metadata or {}
        )
        
        self._agents[agent_id] = profile
        self._agent_tasks[agent_id] = set()
        
        # Index by skills
        for skill in skills:
            self._skill_index[skill].add(agent_id)
        
        # Index by zone
        if zone_id:
            if zone_id not in self._zone_agents:
                self._zone_agents[zone_id] = set()
            self._zone_agents[zone_id].add(agent_id)
        
        return agent_id
    
    def deactivate_agent(self, agent_id: UUID) -> bool:
        """Deactivate an agent, cancelling their current tasks."""
        if agent_id not in self._agents:
            return False
            
        agent = self._agents[agent_id]
        
        # Cancel current tasks
        for task_id in self._agent_tasks[agent_id]:
            self.cancel_task(task_id)
        
        # Remove from indexes
        for skill in agent.skills:
            self._skill_index[skill].remove(agent_id)
        if agent.zone_id and agent.zone_id in self._zone_agents:
            self._zone_agents[agent.zone_id].remove(agent_id)
            
        # Mark as inactive
        agent.status = "INACTIVE"
        return True
    
    def find_agents(
        self,
        required_skills: Optional[Set[AgentSkill]] = None,
        zone_id: Optional[UUID] = None,
        min_level: Optional[int] = None,
        available_only: bool = False
    ) -> List[AgentProfile]:
        """Find agents matching the specified criteria."""
        candidates = set(self._agents.keys())
        
        if required_skills:
            skill_candidates = set.intersection(
                *[self._skill_index[skill] for skill in required_skills]
            )
            candidates &= skill_candidates
        
        if zone_id and zone_id in self._zone_agents:
            candidates &= self._zone_agents[zone_id]
        
        results = []
        for agent_id in candidates:
            agent = self._agents[agent_id]
            if agent.status == "INACTIVE":
                continue
            if min_level is not None and agent.level < min_level:
                continue
            if available_only and len(self._agent_tasks[agent_id]) >= self.MAX_CONCURRENT_TASKS:
                continue
            results.append(agent)
        
        return sorted(results, key=lambda a: a.level, reverse=True)
    
    def create_task(
        self,
        task_type: str,
        required_skills: Set[AgentSkill],
        metadata: Optional[Dict[str, str]] = None
    ) -> UUID:
        """Create a new task that can be assigned to an agent."""
        task_id = uuid4()
        task = Task(
            task_id=task_id,
            task_type=task_type,
            required_skills=required_skills,
            assigned_agent=None,
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            started_at=None,
            completed_at=None,
            metadata=metadata or {}
        )
        
        self._tasks[task_id] = task
        return task_id
    
    def assign_task(
        self,
        task_id: UUID,
        agent_id: UUID
    ) -> bool:
        """Assign a task to an agent if they have the required skills."""
        if task_id not in self._tasks or agent_id not in self._agents:
            return False
            
        task = self._tasks[task_id]
        agent = self._agents[agent_id]
        
        if task.status != TaskStatus.PENDING:
            return False
        
        if not task.required_skills.issubset(agent.skills):
            return False
            
        if len(self._agent_tasks[agent_id]) >= self.MAX_CONCURRENT_TASKS:
            return False
        
        task.assigned_agent = agent_id
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.utcnow()
        self._agent_tasks[agent_id].add(task_id)
        
        return True
    
    def complete_task(
        self,
        task_id: UUID,
        result: Optional[str] = None,
        success: bool = True
    ) -> bool:
        """Mark a task as completed or failed."""
        if task_id not in self._tasks:
            return False
            
        task = self._tasks[task_id]
        if task.status not in [TaskStatus.IN_PROGRESS, TaskStatus.PENDING]:
            return False
            
        task.completed_at = datetime.utcnow()
        task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
        task.result = result
        
        if task.assigned_agent:
            self._agent_tasks[task.assigned_agent].remove(task_id)
            if success:
                self.gain_experience(task.assigned_agent, 10, list(task.required_skills)[0])
        
        return True
    
    def cancel_task(self, task_id: UUID) -> bool:
        """Cancel a pending or in-progress task."""
        if task_id not in self._tasks:
            return False
            
        task = self._tasks[task_id]
        if task.status not in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
            return False
            
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.utcnow()
        
        if task.assigned_agent:
            self._agent_tasks[task.assigned_agent].remove(task_id)
        
        return True
    
    def gain_experience(
        self,
        agent_id: UUID,
        amount: int,
        skill: Optional[AgentSkill] = None
    ) -> bool:
        """Award experience to an agent, potentially leveling them up."""
        if agent_id not in self._agents:
            return False
            
        agent = self._agents[agent_id]
        agent.experience += amount
        
        # Update skill level if specified
        if skill and skill in agent.skills:
            current_level = agent.skill_levels[skill]
            new_level = 1 + (current_level * amount) // 100
            if new_level > current_level:
                agent.skill_levels[skill] = new_level
        
        # Update overall level
        new_level = 1 + agent.experience // 100
        if new_level > agent.level:
            agent.level = new_level
            if skill and skill not in agent.skills:
                agent.skills.add(skill)
                self._skill_index[skill].add(agent_id)
        
        return True
    
    def cleanup_stale_tasks(self) -> int:
        """Clean up stale tasks. Returns number of tasks cleaned up."""
        now = datetime.utcnow()
        cleaned = 0
        
        for task_id, task in list(self._tasks.items()):
            if task.status == TaskStatus.IN_PROGRESS:
                if now - task.started_at > self.TASK_TIMEOUT:
                    self.complete_task(task_id, "Task timed out", success=False)
                    cleaned += 1
                    
        return cleaned 