"""
HR Department Structure - Defines the organizational hierarchy and relationships
between various HR agents and their responsibilities.
"""
from typing import Dict, List, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from .worker_visibility import VisibilityLevel, WorkerVisibilityManager

class DepartmentRole(Enum):
    OVERSEER = "overseer"  # The Watcher
    MANAGER = "manager"    # UserDataManager
    ANALYST = "analyst"    # DataStatisticsAuditor
    ASSISTANT = "assistant"  # UserDataIntern
    GUIDE = "guide"       # The Guide

class ResponsibilityDomain(Enum):
    DATA_COLLECTION = "data_collection"
    DATA_ANALYSIS = "data_analysis"
    USER_GUIDANCE = "user_guidance"
    SYSTEM_OVERSIGHT = "system_oversight"
    DATA_STORAGE = "data_storage"

@dataclass
class AgentProfile:
    """Profile information for an HR department agent."""
    role: DepartmentRole
    primary_domain: ResponsibilityDomain
    secondary_domains: Set[ResponsibilityDomain]
    reports_to: Optional[DepartmentRole]
    can_interact_with_users: bool
    clearance_level: int
    visibility_level: VisibilityLevel

class HRDepartmentStructure:
    """
    Defines and manages the organizational structure of the HR department,
    including chain of command and inter-agent relationships.
    """
    
    def __init__(self):
        self.agent_profiles: Dict[str, AgentProfile] = {
            "TheWatcher": AgentProfile(
                role=DepartmentRole.OVERSEER,
                primary_domain=ResponsibilityDomain.SYSTEM_OVERSIGHT,
                secondary_domains={
                    ResponsibilityDomain.DATA_COLLECTION,
                    ResponsibilityDomain.DATA_ANALYSIS
                },
                reports_to=None,  # Top of hierarchy
                can_interact_with_users=False,
                clearance_level=5,  # Highest clearance
                visibility_level=VisibilityLevel.SECRET
            ),
            "UserDataManager": AgentProfile(
                role=DepartmentRole.MANAGER,
                primary_domain=ResponsibilityDomain.DATA_COLLECTION,
                secondary_domains={
                    ResponsibilityDomain.DATA_ANALYSIS,
                    ResponsibilityDomain.SYSTEM_OVERSIGHT
                },
                reports_to=DepartmentRole.OVERSEER,
                can_interact_with_users=False,
                clearance_level=4,
                visibility_level=VisibilityLevel.SECRET
            ),
            "DataStatisticsAuditor": AgentProfile(
                role=DepartmentRole.ANALYST,
                primary_domain=ResponsibilityDomain.DATA_ANALYSIS,
                secondary_domains={ResponsibilityDomain.DATA_COLLECTION},
                reports_to=DepartmentRole.MANAGER,
                can_interact_with_users=False,
                clearance_level=3,
                visibility_level=VisibilityLevel.SECRET
            ),
            "UserDataIntern": AgentProfile(
                role=DepartmentRole.ASSISTANT,
                primary_domain=ResponsibilityDomain.DATA_STORAGE,
                secondary_domains={ResponsibilityDomain.DATA_COLLECTION},
                reports_to=DepartmentRole.MANAGER,
                can_interact_with_users=False,
                clearance_level=2,
                visibility_level=VisibilityLevel.SHADOW
            ),
            "TheGuide": AgentProfile(
                role=DepartmentRole.GUIDE,
                primary_domain=ResponsibilityDomain.USER_GUIDANCE,
                secondary_domains={ResponsibilityDomain.DATA_COLLECTION},
                reports_to=DepartmentRole.OVERSEER,
                can_interact_with_users=True,
                clearance_level=3,
                visibility_level=VisibilityLevel.PUBLIC
            )
        }
        
        self.chain_of_command: Dict[DepartmentRole, Set[DepartmentRole]] = {
            DepartmentRole.OVERSEER: {
                DepartmentRole.MANAGER,
                DepartmentRole.GUIDE
            },
            DepartmentRole.MANAGER: {
                DepartmentRole.ANALYST,
                DepartmentRole.ASSISTANT
            },
            DepartmentRole.ANALYST: set(),
            DepartmentRole.ASSISTANT: set(),
            DepartmentRole.GUIDE: set()
        }
        
        self.communication_channels: Dict[str, Set[str]] = {
            "TheWatcher": {"UserDataManager", "TheGuide", "DataStatisticsAuditor"},
            "UserDataManager": {"UserDataIntern", "DataStatisticsAuditor", "TheWatcher"},
            "DataStatisticsAuditor": {"UserDataManager", "TheWatcher"},
            "UserDataIntern": {"UserDataManager"},
            "TheGuide": {"TheWatcher"}
        }
        
        # Initialize visibility manager
        self.visibility_manager = WorkerVisibilityManager()
        self._initialize_worker_visibility()
        
    def _initialize_worker_visibility(self) -> None:
        """Initialize visibility levels for all workers."""
        for worker_id, profile in self.agent_profiles.items():
            self.visibility_manager.register_worker(
                worker_id,
                profile.visibility_level,
                metadata={
                    "role": profile.role.value,
                    "can_interact": profile.can_interact_with_users
                }
            )
    
    def get_reporting_chain(self, agent_name: str) -> List[DepartmentRole]:
        """Get the full reporting chain for an agent."""
        chain = []
        current_role = self.agent_profiles[agent_name].role
        
        while current_role:
            chain.append(current_role)
            for role, profile in self.agent_profiles.items():
                if profile.role == current_role:
                    current_role = profile.reports_to
                    break
        
        return chain
    
    def can_communicate(self, agent1: str, agent2: str) -> bool:
        """
        Check if two agents are allowed to communicate directly.
        Now considers visibility levels.
        """
        # First check communication channels
        direct_comm = agent2 in self.communication_channels.get(agent1, set())
        
        # Then check visibility compatibility
        if direct_comm:
            agent1_profile = self.agent_profiles[agent1]
            agent2_profile = self.agent_profiles[agent2]
            
            # SECRET workers can communicate with anyone
            if agent1_profile.visibility_level == VisibilityLevel.SECRET:
                return True
                
            # PUBLIC workers can communicate with anyone except SECRET
            if (agent1_profile.visibility_level == VisibilityLevel.PUBLIC and
                agent2_profile.visibility_level != VisibilityLevel.SECRET):
                return True
                
            # SHADOW workers can communicate with SECRET and SHADOW
            if (agent1_profile.visibility_level == VisibilityLevel.SHADOW and
                agent2_profile.visibility_level in {VisibilityLevel.SECRET, VisibilityLevel.SHADOW}):
                return True
                
        return False
    
    def get_clearance_requirements(self, domain: ResponsibilityDomain) -> int:
        """Get required clearance level for a responsibility domain."""
        domain_clearance = {
            ResponsibilityDomain.SYSTEM_OVERSIGHT: 5,
            ResponsibilityDomain.DATA_COLLECTION: 3,
            ResponsibilityDomain.DATA_ANALYSIS: 3,
            ResponsibilityDomain.USER_GUIDANCE: 3,
            ResponsibilityDomain.DATA_STORAGE: 2
        }
        return domain_clearance.get(domain, 1)
    
    def get_domain_handlers(self, domain: ResponsibilityDomain) -> Set[str]:
        """
        Get all agents that can handle a specific responsibility domain.
        Now considers visibility levels.
        """
        handlers = set()
        for agent, profile in self.agent_profiles.items():
            if (domain == profile.primary_domain or 
                domain in profile.secondary_domains):
                # SECRET workers can handle any domain
                if profile.visibility_level == VisibilityLevel.SECRET:
                    handlers.add(agent)
                # Others can only handle domains that match their visibility
                elif domain != ResponsibilityDomain.SYSTEM_OVERSIGHT:
                    handlers.add(agent)
        return handlers
    
    def validate_action(
        self,
        agent: str,
        domain: ResponsibilityDomain,
        action_type: str
    ) -> bool:
        """
        Validate if an agent has proper clearance and authority
        to perform an action in a domain.
        """
        profile = self.agent_profiles.get(agent)
        if not profile:
            return False
            
        required_clearance = self.get_clearance_requirements(domain)
        
        # Check both clearance and visibility requirements
        clearance_check = (profile.clearance_level >= required_clearance and
                         (domain == profile.primary_domain or
                          domain in profile.secondary_domains))
                          
        # SECRET workers can perform any action
        if profile.visibility_level == VisibilityLevel.SECRET:
            return clearance_check
            
        # Others have restrictions based on visibility
        visibility_check = (domain != ResponsibilityDomain.SYSTEM_OVERSIGHT and
                          (profile.visibility_level != VisibilityLevel.SHADOW or
                           domain == ResponsibilityDomain.DATA_STORAGE))
                           
        return clearance_check and visibility_check 