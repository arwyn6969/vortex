"""
Factory for creating and managing guides based on user profiles and cultural preferences.
"""
from typing import Dict, List, Optional, Set
from .base_guide import Guide
from .thoth import ThothGuide
from .maat import MaatGuide
from .wadjet import WadjetGuide
from .set import SetGuide
from .horus import HorusGuide
from .isis import IsisGuide
from .odin import OdinGuide
from .spider_woman import SpiderWomanGuide
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..mythology.archetype_manager import ArchetypeManager, CulturalSystem
from ..core.lattice import Placement

class GuideFactory:
    """Factory for creating and managing guide instances."""
    
    def __init__(self):
        self.archetype_manager = ArchetypeManager()
        self.available_guides: Dict[str, type] = {
            "thoth": ThothGuide,
            "maat": MaatGuide,
            "wadjet": WadjetGuide,
            "set": SetGuide,
            "horus": HorusGuide,
            "isis": IsisGuide,
            "odin": OdinGuide,
            "spider_woman": SpiderWomanGuide,
        }
        self.active_guides: Dict[str, Guide] = {}
    
    def create_guide(
        self,
        guide_id: str,
        cultural_system: Optional[CulturalSystem] = None
    ) -> Optional[Guide]:
        guide_class = self.available_guides.get(guide_id.lower())
        if not guide_class:
            return None
        guide = guide_class()
        self.active_guides[guide_id] = guide
        return guide

    def create_for_placement(self, placement: Placement) -> Optional[Guide]:
        """Honor a lattice placement. Folk ids fall back to the classical office."""
        guide = self.create_guide(placement.guide_id)
        if guide:
            return guide
        return self.create_guide(placement.node.classical_guide_id)
    
    def get_guide(self, guide_id: str) -> Optional[Guide]:
        return self.active_guides.get(guide_id)
    
    def find_suitable_guides(
        self,
        profile: Dict[ProfileDimension, float],
        cultural_preference: Optional[CulturalSystem] = None,
        min_affinity: float = 0.5
    ) -> List[Guide]:
        suitable_guides = []
        for guide_id, guide_class in self.available_guides.items():
            guide = guide_class()
            if cultural_preference and guide.cultural_system != cultural_preference:
                continue
            affinity = guide.calculate_affinity(profile)
            if affinity >= min_affinity:
                suitable_guides.append((affinity, guide))
        suitable_guides.sort(reverse=True, key=lambda x: x[0])
        return [guide for _, guide in suitable_guides]
    
    def get_resonant_guide(
        self,
        profile: Dict[ProfileDimension, float],
        attributes: Set[str],
        cultural_preference: Optional[CulturalSystem] = None
    ) -> Optional[Guide]:
        resonant_archetypes = self.archetype_manager.get_resonant_archetypes(
            attributes,
            threshold=0.3
        )
        if not resonant_archetypes:
            return None
        potential_guides = []
        for guide_id, guide_class in self.available_guides.items():
            guide = guide_class()
            for archetype in resonant_archetypes:
                if guide.archetype_name == archetype.name:
                    if not cultural_preference or guide.cultural_system == cultural_preference:
                        affinity = guide.calculate_affinity(profile)
                        potential_guides.append((affinity, guide))
                    break
        if not potential_guides:
            return None
        potential_guides.sort(reverse=True, key=lambda x: x[0])
        return potential_guides[0][1]
