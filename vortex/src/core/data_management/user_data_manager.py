"""
UserDataManager - Orchestrates the collection, curation, and distribution of user data
throughout the system.
"""
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from ..hr_department.department_structure import (
    HRDepartmentStructure,
    ResponsibilityDomain,
    DepartmentRole
)

class DataPointType(Enum):
    BEHAVIORAL = "behavioral"
    INTERACTION = "interaction"
    PERFORMANCE = "performance"
    PREFERENCE = "preference"
    PROGRESSION = "progression"
    ENVIRONMENTAL = "environmental"
    DIRECTIVE = "directive"

@dataclass
class DataPoint:
    type: DataPointType
    value: Any
    timestamp: datetime
    context: Dict
    confidence: float
    source: str
    metadata: Dict

class UserDataManager:
    """
    Central manager for all user-related data collection, curation, and distribution.
    Works in conjunction with UserDataIntern for storage/retrieval and DataStatisticsAuditor
    for quality control, following the HR department chain of command.
    """
    
    def __init__(self):
        self.active_collection_strategies: Dict[str, Dict] = {}
        self.data_quality_metrics: Dict[str, float] = {}
        self.collection_priorities: Dict[DataPointType, float] = {}
        self.pending_analyses: List[Dict] = []
        self.department = HRDepartmentStructure()
        
    def _validate_operation(
        self,
        source_agent: str,
        operation_domain: ResponsibilityDomain
    ) -> bool:
        """Validate operation against department structure."""
        return self.department.validate_action(
            source_agent,
            operation_domain,
            "data_operation"
        )
        
    def register_data_point(
        self,
        user_id: str,
        data_point: DataPoint,
        priority: Optional[float] = None,
        source_agent: str = "UserDataManager"
    ) -> str:
        """
        Register a new data point for processing and storage.
        Now includes department structure validation.
        """
        if not self._validate_operation(
            source_agent,
            ResponsibilityDomain.DATA_COLLECTION
        ):
            raise PermissionError(
                f"{source_agent} does not have permission for data collection"
            )
            
        # Generate unique identifier
        data_point_id = f"dp_{user_id}_{datetime.now().timestamp()}"
        
        # Determine handlers based on data type
        handlers = self.department.get_domain_handlers(
            ResponsibilityDomain.DATA_COLLECTION
        )
        
        # Route to appropriate handlers
        for handler in handlers:
            if self.department.can_communicate("UserDataManager", handler):
                # Implementation would handle actual routing
                pass
                
        return data_point_id
        
    def update_collection_strategy(
        self,
        strategy_type: DataPointType,
        new_parameters: Dict,
        source_agent: str = "UserDataManager"
    ) -> None:
        """
        Update how certain types of data are collected and processed.
        Now includes department structure validation.
        """
        if not self._validate_operation(
            source_agent,
            ResponsibilityDomain.DATA_COLLECTION
        ):
            raise PermissionError(
                f"{source_agent} does not have permission to update collection strategy"
            )
            
        self.active_collection_strategies[strategy_type.value] = {
            "parameters": new_parameters,
            "last_updated": datetime.now(),
            "performance_metrics": {},
            "approved_by": source_agent
        }
        
    def request_data_analysis(
        self,
        user_id: str,
        analysis_type: str,
        parameters: Dict,
        source_agent: str = "UserDataManager"
    ) -> str:
        """
        Request a specific type of data analysis.
        Now includes department structure validation.
        """
        if not self._validate_operation(
            source_agent,
            ResponsibilityDomain.DATA_ANALYSIS
        ):
            raise PermissionError(
                f"{source_agent} does not have permission to request analysis"
            )
            
        analysis_id = f"analysis_{user_id}_{datetime.now().timestamp()}"
        
        # Route to appropriate analyst based on department structure
        analysts = self.department.get_domain_handlers(
            ResponsibilityDomain.DATA_ANALYSIS
        )
        
        self.pending_analyses.append({
            "id": analysis_id,
            "user_id": user_id,
            "type": analysis_type,
            "parameters": parameters,
            "status": "pending",
            "requested_by": source_agent,
            "assigned_to": next(iter(analysts), None)
        })
        
        return analysis_id
        
    def distribute_insights(
        self,
        user_id: str,
        insights: Dict,
        target_components: Set[str],
        source_agent: str = "UserDataManager"
    ) -> Dict[str, bool]:
        """
        Distribute processed insights to relevant system components.
        Now includes department structure validation.
        """
        if not self._validate_operation(
            source_agent,
            ResponsibilityDomain.DATA_COLLECTION
        ):
            raise PermissionError(
                f"{source_agent} does not have permission to distribute insights"
            )
            
        results = {}
        for component in target_components:
            if self.department.can_communicate(source_agent, component):
                results[component] = True
            else:
                results[component] = False
                
        return results
        
    def get_data_quality_report(
        self,
        source_agent: str = "UserDataManager"
    ) -> Dict:
        """
        Generate a comprehensive report on data quality metrics.
        Now includes department structure validation.
        """
        if not self._validate_operation(
            source_agent,
            ResponsibilityDomain.DATA_ANALYSIS
        ):
            raise PermissionError(
                f"{source_agent} does not have permission to access quality reports"
            )
            
        return {
            "completeness": self.data_quality_metrics.get("completeness", 0.0),
            "accuracy": self.data_quality_metrics.get("accuracy", 0.0),
            "timeliness": self.data_quality_metrics.get("timeliness", 0.0),
            "consistency": self.data_quality_metrics.get("consistency", 0.0)
        } 