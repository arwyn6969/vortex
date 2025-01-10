from typing import Dict, List, Optional
from collections import deque
from datetime import datetime

class ExperienceMemory:
    """Memory system for storing and processing zone experiences."""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.experiences = deque(maxlen=max_size)
        self.patterns = {}  # Detected interaction patterns
        self.insights = {}  # Learned insights from experiences
        
    def add_experience(self, experience_data: Dict) -> None:
        """Add a new experience to memory with timestamp."""
        experience = {
            "timestamp": datetime.now().isoformat(),
            "data": experience_data,
            "processed": False
        }
        self.experiences.append(experience)
        self._process_new_experience(experience)
        
    def get_recent_experiences(self, n: int) -> List[Dict]:
        """Get the n most recent experiences."""
        return [exp["data"] for exp in list(self.experiences)[-n:]]
        
    def get_pattern_insights(self) -> Dict:
        """Get detected patterns and insights from experiences."""
        return {
            "patterns": self.patterns,
            "insights": self.insights
        }
        
    def _process_new_experience(self, experience: Dict) -> None:
        """Process new experience for patterns and insights."""
        # Update interaction patterns
        self._update_patterns(experience["data"])
        
        # Generate new insights if enough data
        if len(self.experiences) % 10 == 0:  # Process every 10 experiences
            self._generate_insights()
            
    def _update_patterns(self, experience_data: Dict) -> None:
        """Update detected interaction patterns."""
        # Track user interaction patterns
        for key, value in experience_data.items():
            if key not in self.patterns:
                self.patterns[key] = {
                    "sum": value,
                    "count": 1,
                    "avg": value
                }
            else:
                self.patterns[key]["sum"] += value
                self.patterns[key]["count"] += 1
                self.patterns[key]["avg"] = self.patterns[key]["sum"] / self.patterns[key]["count"]
                
    def _generate_insights(self) -> None:
        """Generate insights from accumulated experiences."""
        if len(self.experiences) < 10:
            return
            
        recent_experiences = self.get_recent_experiences(10)
        
        # Analyze trends in user interaction
        trends = self._analyze_trends(recent_experiences)
        
        # Update insights based on trends
        for trend_type, trend_value in trends.items():
            if trend_type not in self.insights:
                self.insights[trend_type] = []
            if trend_value not in self.insights[trend_type]:
                self.insights[trend_type].append(trend_value)
                
    def _analyze_trends(self, experiences: List[Dict]) -> Dict:
        """Analyze trends in recent experiences."""
        trends = {}
        
        # Analyze user interaction patterns
        harmony_trend = sum(exp.get("user_harmony", 0.5) for exp in experiences) / len(experiences)
        if harmony_trend > 0.7:
            trends["harmony"] = "increasing"
        elif harmony_trend < 0.3:
            trends["harmony"] = "decreasing"
            
        # Analyze interaction intensity
        intensity_trend = sum(exp.get("intensity", 0.5) for exp in experiences) / len(experiences)
        if intensity_trend > 0.7:
            trends["intensity"] = "high"
        elif intensity_trend < 0.3:
            trends["intensity"] = "low"
            
        return trends
        
    def __len__(self) -> int:
        """Return the number of stored experiences."""
        return len(self.experiences) 