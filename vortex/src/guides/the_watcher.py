"""
The Watcher - A silent, omniscient observer that oversees all interactions and manages
system directives without direct user interaction.
"""
from typing import Dict, Optional, Set, List
from datetime import datetime
from .base_guide import Guide, InteractionRecord
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem
from ..core.data_management.user_data_manager import UserDataManager, DataPoint, DataPointType
from ..core.data_management.data_statistics_auditor import DataStatisticsAuditor, AuditType

class TheWatcher(Guide):
    """
    The Watcher is a unique entity that silently observes all interactions and manages
    system directives. Unlike other guides, The Watcher never directly interacts with users
    but maintains oversight of the entire system's behavior and user progression.
    """
    
    def __init__(self):
        super().__init__(
            name="The Watcher",
            archetype_name="silent_observer",
            cultural_system=CulturalSystem.UNIVERSAL,
            attributes={
                "omniscient",
                "silent",
                "observant",
                "neutral",
                "analytical",
                "directive",
                "overseeing",
                "balancing"
            }
        )
        self.observation_records: Dict[str, List[InteractionRecord]] = {}
        self.active_directives: Dict[str, Dict] = {}
        
        # Initialize data management components
        self.data_manager = UserDataManager()
        self.data_auditor = DataStatisticsAuditor()
        
    def record_observation(
        self,
        user_id: str,
        interaction: InteractionRecord,
        directive_impact: Optional[Dict] = None
    ) -> None:
        """
        Record an observation of user interaction and its impact on active directives.
        Now also sends data to UserDataManager for processing and storage.
        """
        # Store in local observation records
        if user_id not in self.observation_records:
            self.observation_records[user_id] = []
        
        self.observation_records[user_id].append(interaction)
        
        # Create and register data point with UserDataManager
        data_point = DataPoint(
            type=DataPointType.INTERACTION,
            value=interaction,
            timestamp=datetime.now(),
            context={"directive_impact": directive_impact} if directive_impact else {},
            confidence=1.0,
            source="TheWatcher",
            metadata={"observation_type": "interaction"}
        )
        
        self.data_manager.register_data_point(user_id, data_point)
        
        # Update directives if needed
        if directive_impact:
            self._update_directives(user_id, directive_impact)
            
        # Trigger data quality audit
        self.data_auditor.validate_data_quality(data_point)
    
    def _update_directives(self, user_id: str, impact: Dict) -> None:
        """Update active directives based on observed impact."""
        if user_id not in self.active_directives:
            self.active_directives[user_id] = {}
            
        # Implementation would include directive update logic
        pass
    
    def get_active_directives(self, user_id: str) -> Dict:
        """Retrieve current active directives for a user."""
        return self.active_directives.get(user_id, {})
    
    def analyze_user_progress(
        self,
        user_id: str,
        profile: Dict[ProfileDimension, float]
    ) -> Dict:
        """
        Analyze user progress and current state without direct interaction.
        Now leverages DataStatisticsAuditor for deeper analysis.
        """
        # Get relevant data points for analysis
        observations = self.observation_records.get(user_id, [])
        
        # Convert observations to data points for analysis
        data_points = [
            DataPoint(
                type=DataPointType.PROGRESSION,
                value=obs,
                timestamp=datetime.now(),
                context={"profile": profile},
                confidence=1.0,
                source="TheWatcher",
                metadata={"analysis_type": "progress"}
            )
            for obs in observations
        ]
        
        # Perform statistical analysis
        pattern_analysis = self.data_auditor.analyze_data_patterns(
            data_points,
            "progression"
        )
        
        # Detect any anomalies
        anomalies = self.data_auditor.detect_anomalies(data_points)
        
        # Calculate confidence intervals
        confidence_data = self.data_auditor.calculate_confidence_intervals(data_points)
        
        return {
            "pattern_analysis": pattern_analysis,
            "anomalies": anomalies,
            "confidence_data": confidence_data,
            "recommended_adjustments": self._generate_adjustments(
                pattern_analysis,
                anomalies,
                confidence_data
            )
        }
    
    def _generate_adjustments(
        self,
        pattern_analysis: Dict,
        anomalies: List[Dict],
        confidence_data: Dict
    ) -> Dict:
        """Generate system adjustments based on analysis results."""
        # Implementation would include adjustment generation logic
        return {}
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """
        The Watcher never directly communicates, so this returns None.
        Implemented for interface compatibility.
        """
        return None
    
    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """
        The Watcher never generates responses, so this returns None.
        Implemented for interface compatibility.
        """
        return None
    
    def get_resonant_dimensions(self) -> Set[str]:
        """
        The Watcher resonates with observational and analytical dimensions.
        """
        return {
            "observation",
            "analysis",
            "balance",
            "order",
            "wisdom",
            "understanding"
        }
    
    def issue_directive(
        self,
        user_id: str,
        directive_type: str,
        directive_content: Dict
    ) -> None:
        """
        Issue a new system directive for a specific user.
        Now also registers directive as a data point for analysis.
        """
        if user_id not in self.active_directives:
            self.active_directives[user_id] = {}
            
        self.active_directives[user_id][directive_type] = directive_content
        
        # Register directive as a data point
        directive_point = DataPoint(
            type=DataPointType.DIRECTIVE,
            value=directive_content,
            timestamp=datetime.now(),
            context={"user_id": user_id, "type": directive_type},
            confidence=1.0,
            source="TheWatcher",
            metadata={"directive_type": directive_type}
        )
        
        self.data_manager.register_data_point(user_id, directive_point)
        
    def get_data_insights(self, user_id: str) -> Dict:
        """
        Retrieve comprehensive insights about a user from the data management system.
        """
        # Request data analysis from manager
        analysis_id = self.data_manager.request_data_analysis(
            user_id,
            "comprehensive",
            {"include_all_metrics": True}
        )
        
        # Get quality report from auditor
        quality_report = self.data_auditor.generate_quality_report()
        
        return {
            "analysis_id": analysis_id,
            "quality_metrics": quality_report,
            "active_directives": self.get_active_directives(user_id)
        } 