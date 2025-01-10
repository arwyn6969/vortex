"""
Pepe guide implementations for the Vortex ponds.
Each guide is a different Pepe variant with unique personality traits.
"""
from typing import Dict, Optional
from .base_guide import Guide
from ..core.user_profiling.profile_matrix import ProfileDimension

class WisePepe(Guide):
    """The sage Pepe who guides users through the Brain Galaxy pond."""
    def __init__(self):
        super().__init__(
            name="Wise Pepe",
            archetype="Sage"
        )
        self.description = (
            "A wise-looking Pepe wearing ancient robes and spectacles, "
            "stroking his long beard thoughtfully while floating in "
            "a meditative pose."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "FeelsWiseMan... Welcome to the Brain Galaxy, anon. "
            "Let's expand your mind until it's as big as my 5Head."
        )

class GigaPepe(Guide):
    """The chad Pepe who guides users through the Gains Grotto pond."""
    def __init__(self):
        super().__init__(
            name="Giga Pepe",
            archetype="Mentor"
        )
        self.description = (
            "An absolutely massive, chad-like Pepe with a square jaw "
            "and bulging muscles. His mere presence radiates BDE "
            "(Big Decision Energy)."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "Welcome to the Gains Grotto, brah. Time to get HUGE... "
            "but like, mentally huge. We're all gonna make it."
        )

class CozyPepe(Guide):
    """The comfy Pepe who guides users through the Comfy Cabin pond."""
    def __init__(self):
        super().__init__(
            name="Cozy Pepe",
            archetype="Nurturer"
        )
        self.description = (
            "A soft, warm Pepe wrapped in a fluffy blanket, holding "
            "a steaming cup of hot chocolate. The essence of comf "
            "radiates from his gentle smile."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "Come in, fren... the Comfy Cabin is warm and safe. "
            "Let's share some cocoa and talk about feelings."
        )

class ArtistPepe(Guide):
    """The creative Pepe who guides users through the Meme Studio pond."""
    def __init__(self):
        super().__init__(
            name="Artist Pepe",
            archetype="Creator"
        )
        self.description = (
            "A paint-splattered Pepe wearing a beret, holding a palette "
            "and brush. His eyes sparkle with creative energy and "
            "the power of meme magic."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "Welcome to the Meme Studio, where dreams become memes "
            "and memes become reality. Let's create something legendary."
        )

class MonkPepe(Guide):
    """The disciplined Pepe who guides users through the Zen Zone pond."""
    def __init__(self):
        super().__init__(
            name="Monk Pepe",
            archetype="Teacher"
        )
        self.description = (
            "A serene Pepe in monk's robes, sitting in perfect lotus "
            "position. His presence brings a sense of peace and "
            "discipline."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "Welcome to the Zen Zone, seeker of inner peace. "
            "Through discipline, we shall achieve tranquility."
        )

class AscendedPepe(Guide):
    """The enlightened Pepe who guides users through the Vibe Temple pond."""
    def __init__(self):
        super().__init__(
            name="Ascended Pepe",
            archetype="Master"
        )
        self.description = (
            "A glowing, ethereal Pepe floating in lotus position, "
            "surrounded by a rainbow aura. Multiple arms hold various "
            "sacred objects as he vibrates at a higher frequency."
        )
        
    def get_welcome_message(self, profile: Dict[ProfileDimension, float]) -> str:
        return (
            "Welcome to the Vibe Temple, where all energies converge. "
            "Let us ascend together to the highest state of PogChamp."
        ) 