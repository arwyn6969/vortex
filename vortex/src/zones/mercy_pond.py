"""
Mercy Pond (Chesed) - The fourth Sefirot, representing loving-kindness and compassion.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute

class MercyPond(Zone):
    """The Pond of Mercy - A place of compassion, kindness, and benevolent action."""
    
    def __init__(self):
        # Initialize with Ma'at as the guide (Egyptian goddess of truth, justice, and harmony)
        from ..guides.maat import MaatGuide
        guide = MaatGuide()
        super().__init__("Pond of Mercy", guide)
        
        self.description = (
            "A radiant pool of silver-blue water, its surface perfectly still yet "
            "somehow flowing with gentle currents. White lotus flowers float serenely "
            "on the surface, their petals occasionally opening to reveal soft light."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.EMPATHY: 0.6,
            ProfileDimension.COMPASSION: 0.5,
            ProfileDimension.WISDOM: 0.3,
            ProfileDimension.HARMONY: 0.4
        }
        
        self.required_dimensions = [
            ProfileDimension.EMPATHY,
            ProfileDimension.COMPASSION
        ]
        
        self.min_dimension_values = {
            ProfileDimension.EMPATHY: 0.3,
            ProfileDimension.COMPASSION: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Water",
            "color": "Blue",
            "sefirot": SefirotAttribute.CHESED,
            "animal": "Swan",
            "mineral": "Sapphire"
        }
        
    def setup_challenges(self) -> None:
        """Initialize the pond's challenge system."""
        self.challenges = {
            "empathy_bridge": {
                "title": "The Bridge of Understanding",
                "description": (
                    "Before you stand three spirits, each bearing a different burden. "
                    "You must help them find peace by understanding their perspectives."
                ),
                "spirits": [
                    {
                        "name": "The Grieving",
                        "story": "Lost something precious, fears to love again",
                        "need": "Acceptance of cycles of loss and renewal"
                    },
                    {
                        "name": "The Angry",
                        "story": "Suffered injustice, seeks vengeance",
                        "need": "Understanding that hatred harms the self"
                    },
                    {
                        "name": "The Fearful",
                        "story": "Paralyzed by possible futures",
                        "need": "Courage to embrace uncertainty with hope"
                    }
                ],
                "difficulty": 0.5,
                "rewards": {
                    ProfileDimension.EMPATHY: 0.2,
                    ProfileDimension.COMPASSION: 0.2
                }
            },
            "healing_choice": {
                "title": "The Healer's Dilemma",
                "description": (
                    "Two seekers need healing, but you only have energy for one. "
                    "Choose wisely, considering both immediate and long-term effects."
                ),
                "options": {
                    "healer": {
                        "description": "Heal the traveling healer who can help others",
                        "impact": {
                            ProfileDimension.WISDOM: 0.2,
                            ProfileDimension.COMPASSION: 0.1
                        }
                    },
                    "child": {
                        "description": "Heal the child who needs immediate help",
                        "impact": {
                            ProfileDimension.EMPATHY: 0.2,
                            ProfileDimension.COMPASSION: 0.1
                        }
                    }
                },
                "difficulty": 0.7
            },
            "harmony_weaving": {
                "title": "Weaving the Threads of Peace",
                "description": (
                    "Guide conflicting energies into harmony by weaving them together. "
                    "Each thread represents a different aspect that must be balanced."
                ),
                "threads": [
                    "Justice and Mercy",
                    "Truth and Kindness",
                    "Strength and Gentleness",
                    "Wisdom and Love"
                ],
                "difficulty": 0.8,
                "rewards": {
                    ProfileDimension.HARMONY: 0.3,
                    ProfileDimension.WISDOM: 0.2,
                    ProfileDimension.EMPATHY: 0.2
                }
            }
        }

    def process_action(self, action: str) -> bool:
        """Process zone-specific actions."""
        if not super().process_action(action):
            if action.startswith("comfort"):
                return self.handle_comfort()
            elif action.startswith("heal"):
                return self.handle_healing()
            return False
        return True

    def handle_comfort(self) -> bool:
        """Handle comfort action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        comfort_impact = {
            ProfileDimension.EMPATHY: 0.05,
            ProfileDimension.COMPASSION: 0.05
        }
        player.update_profile(comfort_impact)
        
        player.ui.display_text(
            "You extend your compassion to those around you. The lotus flowers "
            "seem to glow more brightly in response to your kindness."
        )
        return True

    def handle_healing(self) -> bool:
        """Handle healing action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        healing_impact = {
            ProfileDimension.COMPASSION: 0.05,
            ProfileDimension.HARMONY: 0.03
        }
        player.update_profile(healing_impact)
        
        player.ui.display_text(
            "You channel the pond's healing energy, letting it flow through you. "
            "The water ripples with silver light, responding to your intention."
        )
        return True

    def get_available_actions(self) -> List[str]:
        """Get list of available actions specific to Mercy Pond."""
        actions = super().get_available_actions()
        actions.extend(["comfort", "heal"])
        return actions

    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt the pond's description based on user's profile."""
        empathy = profile.get(ProfileDimension.EMPATHY, 0.0)
        compassion = profile.get(ProfileDimension.COMPASSION, 0.0)
        
        if empathy < 0.3 and compassion < 0.3:
            return (
                "The silver-blue waters lie still and quiet. You sense there is "
                "healing here, but its source remains distant and unclear."
            )
        elif empathy < 0.6 or compassion < 0.6:
            return (
                "The lotus flowers seem to respond to your presence, their petals "
                "gradually opening to reveal soft, healing light. The water's "
                "gentle currents carry whispers of compassion."
            )
        else:
            return (
                "The pond resonates with your compassionate nature. Each lotus "
                "flower glows with inner light, and the waters themselves seem "
                "to reach out with healing energy. You feel at one with the "
                "pond's merciful essence."
            )

    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            ProfileDimension.EMPATHY: 0.8,
            ProfileDimension.COMPASSION: 0.8,
            ProfileDimension.HARMONY: 0.7
        }
``` 