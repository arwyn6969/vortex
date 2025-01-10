"""
Spider Woman Guide - The Hopi goddess of creation and weaver of life's patterns.
"""
from typing import Dict, Optional, Set
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import CulturalSystem

class SpiderWomanGuide(Guide):
    """Implementation of Spider Woman as a harmony keeper archetype."""
    
    def __init__(self):
        super().__init__(
            name="Spider Woman",
            archetype_name="harmony_keeper",
            cultural_system=CulturalSystem.HOPI,
            attributes={
                "weaving",
                "creation",
                "harmony",
                "balance",
                "teaching",
                "emergence"
            }
        )
        self.weaving_style = {
            "harmonious": 0.9,
            "creative": 0.8,
            "nurturing": 0.7,
            "transformative": 0.6
        }
    
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        """Generate personalized welcome message."""
        # Adapt message based on user's profile dimensions
        pattern_recognition = profile.get(ProfileDimension.PATTERN_RECOGNITION, 0.5)
        contextual_fluidity = profile.get(ProfileDimension.CONTEXTUAL_FLUIDITY, 0.5)
        
        if pattern_recognition > 0.7 and contextual_fluidity > 0.7:
            return (
                "Welcome, child of emergence. I am Spider Woman, who weaves the "
                "patterns of creation. Together we shall explore the sacred web "
                "that connects all beings and worlds."
            )
        elif pattern_recognition > 0.5 or contextual_fluidity > 0.5:
            return (
                "Greetings, seeker of balance. I am Spider Woman, keeper of life's "
                "patterns. Let us discover how all threads are connected in the "
                "great web of existence."
            )
        else:
            return (
                "Welcome. I am Spider Woman, and like the web I weave, all paths "
                "are connected. Shall we explore how your thread fits into the "
                "greater pattern?"
            )
    
    def generate_response(
        self,
        user_input: str,
        profile: Dict[ProfileDimension, float],
        context: Optional[Dict] = None
    ) -> str:
        """Generate contextually appropriate response."""
        # Record the interaction
        self.record_interaction(
            context="user_dialogue",
            profile=profile,
            metadata={"input": user_input, "context": context}
        )
        
        # Adapt weaving style based on profile
        pattern_recognition = profile.get(ProfileDimension.PATTERN_RECOGNITION, 0.5)
        contextual_fluidity = profile.get(ProfileDimension.CONTEXTUAL_FLUIDITY, 0.5)
        
        if pattern_recognition > 0.7:
            self.weaving_style["harmonious"] = min(1.0, self.weaving_style["harmonious"] + 0.1)
            self.weaving_style["creative"] = min(1.0, self.weaving_style["creative"] + 0.1)
        
        if contextual_fluidity > 0.7:
            self.weaving_style["nurturing"] = min(1.0, self.weaving_style["nurturing"] + 0.1)
            self.weaving_style["transformative"] = min(1.0, self.weaving_style["transformative"] + 0.1)
        
        # Generate response based on weaving style
        if self.weaving_style["harmonious"] > self.weaving_style["transformative"]:
            return (
                f"I see how your thread weaves with others. {user_input} shows "
                "the pattern you are creating in life's great web."
            )
        else:
            return (
                f"The web of life shifts with your movement. {user_input} creates "
                "new patterns of possibility and connection."
            )
    
    def offer_pattern_wisdom(
        self,
        profile: Dict[ProfileDimension, float],
        pattern_type: str
    ) -> str:
        """Provide specific wisdom about different types of life patterns."""
        contextual_fluidity = profile.get(ProfileDimension.CONTEXTUAL_FLUIDITY, 0.5)
        
        pattern_teachings = {
            "spiral": (
                "The spiral shows us how life moves in cycles, yet always "
                "progresses. Each turn brings new understanding while honoring "
                "what came before."
            ),
            "web": (
                "The web reminds us that all life is connected. Each strand "
                "affects the whole, and the whole supports each strand."
            ),
            "emergence": (
                "The pattern of emergence teaches that transformation comes "
                "through stages. Like the people's journey through the worlds, "
                "each step brings new awareness."
            ),
            "balance": (
                "The pattern of balance shows how opposing forces create "
                "harmony. Like day and night, each aspect has its purpose."
            )
        }
        
        base_teaching = pattern_teachings.get(
            pattern_type.lower(),
            "All patterns in nature contain wisdom for those who observe closely."
        )
        
        if contextual_fluidity > 0.7:
            return f"See how the pattern speaks: {base_teaching} Let it guide your weaving."
        else:
            return f"Consider this pattern: {base_teaching} Its wisdom will unfold in time." 