"""
Severity Pond (Gevurah) - The fifth Sefirot, representing discipline, judgment, and necessary boundaries.
"""
from typing import Dict, List, Optional
from .base_zone import Zone
from ..guides.base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem
from ..mythology.sefirot import SefirotAttribute
from ..core.user_profiling.adaptive_learning import LearningPathNode

class GainsGrotto(Zone):
    """The Gains Grotto - A place of discipline, judgment, and necessary boundaries."""
    
    def __init__(self):
        # Initialize with Sekhmet as the guide (Egyptian goddess of divine judgment)
        from ..guides.sekhmet import SekhmetGuide
        guide = SekhmetGuide()
        super().__init__("Gains Grotto", guide)
        
        self.description = (
            "A deep crimson pool whose waters pulse with intense energy. Obsidian "
            "pillars rise from the depths, their surfaces etched with laws and "
            "boundaries. The air crackles with the power of divine judgment."
        )
        
        # Configure behavioral dimensions
        self.dimension_weights = {
            ProfileDimension.JUDGMENT: 0.6,
            ProfileDimension.DISCIPLINE: 0.5,
            ProfileDimension.DISCERNMENT: 0.4,
            ProfileDimension.COURAGE: 0.3
        }
        
        self.required_dimensions = [
            ProfileDimension.JUDGMENT,
            ProfileDimension.DISCIPLINE
        ]
        
        self.min_dimension_values = {
            ProfileDimension.JUDGMENT: 0.3,
            ProfileDimension.DISCIPLINE: 0.3
        }
        
        # Initialize challenges
        self.setup_challenges()
        
        # Symbolic associations
        self.symbols = {
            "element": "Fire",
            "color": "Red",
            "sefirot": SefirotAttribute.GEVURAH,
            "animal": "Lion",
            "mineral": "Ruby",
            "crypto_aspects": {
                "bitcoin_elements": [
                    "Proof of Work (Divine Judgment)",
                    "Consensus Rules (Sacred Boundaries)",
                    "Mining Difficulty (Trial by Fire)",
                    "21M Cap (Divine Limitation)"
                ],
                "blockchain_wisdom": [
                    "Code is Law (Digital Judgment)",
                    "Don't Trust, Verify (Divine Discernment)",
                    "Network Effect (Collective Strength)",
                    "Digital Scarcity (Sacred Limits)"
                ]
            }
        }
        
    def setup_challenges(self) -> None:
        """Initialize the pond's challenge system."""
        self.challenges = {
            "bitcoin_trial": {
                "title": "The Blockchain's Trial",
                "description": (
                    "Face the challenges of Bitcoin's consensus mechanism. Each decision "
                    "tests your understanding of digital sovereignty and sacred boundaries."
                ),
                "trials": [
                    {
                        "name": "Proof of Work Meditation",
                        "description": "Channel computational energy to secure the network",
                        "consequence": "Balance energy expenditure with network security"
                    },
                    {
                        "name": "Consensus Formation",
                        "description": "Participate in network-wide agreement",
                        "consequence": "Navigate between individual and collective truth"
                    },
                    {
                        "name": "Block Validation",
                        "description": "Verify transactions without trust",
                        "consequence": "Maintain network integrity through vigilance"
                    }
                ],
                "difficulty": 0.7,
                "rewards": {
                    ProfileDimension.JUDGMENT: 0.3,
                    ProfileDimension.DISCIPLINE: 0.2
                }
            },
            "boundary_test": {
                "title": "The Lines of Power",
                "description": (
                    "Sacred boundaries appear in the water. You must decide which "
                    "to maintain and which to transcend, each choice affecting "
                    "the balance of power."
                ),
                "boundaries": [
                    {
                        "name": "The Veil of Knowledge",
                        "description": "Separates sacred from profane wisdom",
                        "consequence": "Maintaining strengthens tradition but limits growth"
                    },
                    {
                        "name": "The Circle of Protection",
                        "description": "Guards against external corruption",
                        "consequence": "Maintaining ensures safety but isolates"
                    },
                    {
                        "name": "The Chain of Command",
                        "description": "Establishes hierarchy and order",
                        "consequence": "Maintaining provides structure but restricts innovation"
                    }
                ],
                "difficulty": 0.6,
                "rewards": {
                    ProfileDimension.JUDGMENT: 0.2,
                    ProfileDimension.DISCERNMENT: 0.2
                }
            },
            "justice_trial": {
                "title": "The Scales of Truth",
                "description": (
                    "Three cases appear before you, each requiring judgment. "
                    "Balance mercy with justice, knowing each decision ripples "
                    "through the fabric of reality."
                ),
                "cases": [
                    {
                        "scenario": "A theft driven by desperate need",
                        "context": "The thief stole medicine for a dying child",
                        "options": ["Strict punishment", "Merciful rehabilitation", "Balanced restitution"]
                    },
                    {
                        "scenario": "A betrayal of trust",
                        "context": "A guardian misused their power for personal gain",
                        "options": ["Public censure", "Private redemption", "Systemic reform"]
                    },
                    {
                        "scenario": "An act of rebellion",
                        "context": "Breaking unjust rules to help others",
                        "options": ["Uphold law", "Support change", "Guide transformation"]
                    }
                ],
                "difficulty": 0.8,
                "rewards": {
                    ProfileDimension.JUDGMENT: 0.3,
                    ProfileDimension.WISDOM: 0.2
                }
            },
            "purification_ritual": {
                "title": "The Flames of Purification",
                "description": (
                    "Channel the pond's purifying energy to burn away what no "
                    "longer serves. But beware - the flames consume both weakness "
                    "and strength without discrimination."
                ),
                "aspects": [
                    "Fear holding you back",
                    "Attachments clouding judgment",
                    "False beliefs limiting growth",
                    "Misplaced mercy enabling harm"
                ],
                "difficulty": 0.9,
                "rewards": {
                    ProfileDimension.DISCIPLINE: 0.3,
                    ProfileDimension.COURAGE: 0.2,
                    ProfileDimension.DISCERNMENT: 0.2
                }
            }
        }

    def process_action(self, action: str) -> bool:
        """Process zone-specific actions."""
        if not super().process_action(action):
            if action.startswith("judge"):
                return self.handle_judgment()
            elif action.startswith("purify"):
                return self.handle_purification()
            return False
        return True

    def handle_judgment(self) -> bool:
        """Handle judgment action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        judgment_impact = {
            ProfileDimension.JUDGMENT: 0.05,
            ProfileDimension.DISCERNMENT: 0.05
        }
        player.update_profile(judgment_impact)
        
        player.ui.display_text(
            "You focus your mind on the principles of divine justice. The obsidian "
            "pillars resonate with your contemplation, their etched laws glowing."
        )
        return True

    def handle_purification(self) -> bool:
        """Handle purification action."""
        player = self.current_state.get('last_player')
        if not player:
            return False
            
        purification_impact = {
            ProfileDimension.DISCIPLINE: 0.05,
            ProfileDimension.COURAGE: 0.03
        }
        player.update_profile(purification_impact)
        
        player.ui.display_text(
            "You immerse yourself in the crimson waters, letting their purifying "
            "energy burn away impurities. Each moment strengthens your resolve."
        )
        return True

    def get_available_actions(self) -> List[str]:
        """Get list of available actions specific to Severity Pond."""
        actions = super().get_available_actions()
        actions.extend(["judge", "purify"])
        return actions

    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt the pond's description based on user's profile."""
        judgment = profile.get(ProfileDimension.JUDGMENT, 0.0)
        discipline = profile.get(ProfileDimension.DISCIPLINE, 0.0)
        
        if judgment < 0.3 and discipline < 0.3:
            return (
                "The crimson waters churn with intimidating power. The obsidian "
                "pillars loom over you, their meanings yet unclear."
            )
        elif judgment < 0.6 or discipline < 0.6:
            return (
                "The pond's energy feels more focused now, its power responding "
                "to your growing sense of judgment. The pillars' laws begin to "
                "reveal their deeper purpose."
            )
        else:
            return (
                "The waters of severity recognize your disciplined spirit. The "
                "obsidian pillars resonate with your presence, their laws now "
                "clear as crystal. You feel the perfect balance of power and "
                "restraint."
            )

    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            ProfileDimension.JUDGMENT: 0.8,
            ProfileDimension.DISCIPLINE: 0.8,
            ProfileDimension.DISCERNMENT: 0.7
        } 