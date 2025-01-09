"""
Base class for game zones (ponds).
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..guides.base_guide import Guide
from .stream_manager import StreamManager
from ..core.user_profiling.profile_matrix import ProfileDimension
from ..core.user_profiling.personalization import ContentItem

class Zone(ABC):
    _stream_manager = StreamManager()  # Shared instance for all zones
    
    def __init__(self, name: str, guide: Guide):
        self.name = name
        self.guide = guide
        self.description: str = ""
        self.challenges: dict = {}
        self.dimension_weights: Dict[ProfileDimension, float] = {}
        self.required_dimensions: List[ProfileDimension] = []
        self.min_dimension_values: Dict[ProfileDimension, float] = {}
        self.current_state: Dict[str, Any] = {}
        self.active_players: List[Any] = []
        
    def enter(self, player) -> None:
        """Called when a player enters this zone.
        
        Args:
            player: The player object entering the zone
            
        This method:
        1. Updates the zone's state with the new player
        2. Triggers the guide's welcome message
        3. Adapts the zone's content based on player's profile
        4. Renders the initial zone state
        """
        self.active_players.append(player)
        self.current_state['last_player'] = player
        
        # Adapt zone content to player
        adapted_description = self.adapt_description(player.profile)
        self.description = adapted_description
        
        # Get personalized guidance
        welcome_message = self.guide.get_welcome_message(player.profile)
        self.current_state['last_message'] = welcome_message
        
        # Update available challenges
        self.current_state['available_challenges'] = self.get_available_challenges(player.profile)
        
        # Initial render
        self.render(player.ui)
        
    def process_action(self, action: str) -> bool:
        """Process a player action in this zone.
        
        Args:
            action: String representing the player's action
            
        Returns:
            bool: True if action was processed successfully
            
        This method:
        1. Validates the action
        2. Updates zone state based on action
        3. Triggers appropriate guide responses
        4. Returns success/failure
        """
        if not self.current_state.get('last_player'):
            return False
            
        player = self.current_state['last_player']
        action = action.lower().strip()
        
        # Basic actions
        if action == "look":
            self.render(player.ui)
            return True
            
        if action == "help":
            guidance = self.guide.get_guidance_message(player.profile)
            player.ui.display_text(guidance)
            return True
            
        if action == "talk":
            response = self.guide.get_contextual_response(
                player.profile,
                self.current_state.get('context', '')
            )
            player.ui.display_text(response)
            return True
            
        # Movement actions
        if action.startswith("move "):
            target_zone = action[5:].strip()
            if self.can_access_zone(target_zone, player):
                return player.move_to_zone(target_zone)
            else:
                player.ui.display_text(f"You cannot access {target_zone} yet.")
                return False
                
        # Challenge actions
        if action.startswith("challenge "):
            challenge_id = action[10:].strip()
            available_challenges = self.current_state.get('available_challenges', [])
            challenge = next((c for c in available_challenges if c.id == challenge_id), None)
            if challenge:
                return self.start_challenge(challenge, player)
            else:
                player.ui.display_text("Challenge not available.")
                return False
                
        return False
        
    def render(self, ui) -> None:
        """Render the zone's current state.
        
        Args:
            ui: The UI interface to render to
            
        This method:
        1. Displays zone name and description
        2. Shows symbolic information
        3. Lists available connections
        4. Shows current challenges
        5. Displays guide presence
        6. Lists available actions
        """
        # Basic zone information
        ui.display_title(self.name)
        ui.display_text(self.description)
        
        # Display symbolic information
        symbols = self.get_symbolic_info()
        if symbols:
            ui.display_text("\nSymbolic Associations:")
            ui.display_text(f"Element: {symbols['element']}")
            ui.display_text(f"Color: {symbols['color']}")
        
        # Display available connections
        connections = self.get_connected_zones()
        if connections:
            ui.display_text("\nConnected Ponds:")
            for zone in connections:
                path_desc = self.get_path_description(zone)
                if path_desc:
                    ui.display_text(f"- {path_desc}")
        
        # Display available challenges
        available_challenges = self.current_state.get('available_challenges', [])
        if available_challenges:
            ui.display_text("\nAvailable Challenges:")
            for challenge in available_challenges:
                ui.display_text(f"- {challenge.title}")
        
        # Display guide presence
        if self.guide:
            ui.display_text(f"\n{self.guide.name} is present here to assist you.")
        
        # Display last message if any
        last_message = self.current_state.get('last_message')
        if last_message:
            ui.display_text(f"\nGuide: {last_message}")
        
        # Display available actions
        ui.display_available_actions(self.get_available_actions())
    
    def get_connected_zones(self) -> List[str]:
        """Get list of zones connected to this one."""
        return self._stream_manager.get_connected_ponds(self.name)
    
    def can_access_zone(self, target_zone: str, player) -> bool:
        """Check if player can access the target zone."""
        if not self._stream_manager.are_connected(self.name, target_zone):
            return False
        path_details = self._stream_manager.get_path_details(self.name, target_zone)
        stream_id = f"stream_{path_details['letter']}"
        return player.can_access_stream(stream_id)
    
    def get_path_description(self, target_zone: str) -> Optional[str]:
        """Get description of the path to target zone."""
        path = self._stream_manager.get_path_details(self.name, target_zone)
        if path:
            return f"The {path['name']} ({path['letter']}) connects to the {target_zone}."
        return None
    
    def get_available_actions(self) -> List[str]:
        """Get list of available actions in this zone."""
        actions = ["look", "inventory", "talk", "help"]
        # Add connected zones as possible movement actions
        for zone in self.get_connected_zones():
            actions.append(f"move {zone}")
        return actions
    
    def get_symbolic_info(self) -> Optional[Dict]:
        """Get symbolic associations for this zone."""
        return self._stream_manager.get_symbolic_info(self.name)
    
    def get_entry_requirements(self) -> Dict[str, float]:
        """Get the minimum dimension values required to enter this zone."""
        return {
            dim.value: value 
            for dim, value in self.min_dimension_values.items()
        }
        
    def is_accessible(self, profile: Dict[ProfileDimension, float]) -> bool:
        """Check if a user's profile meets the zone's requirements."""
        for dim, min_value in self.min_dimension_values.items():
            if profile.get(dim, 0.0) < min_value:
                return False
        return True
        
    def get_challenge_difficulty(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> float:
        """Calculate appropriate challenge difficulty based on profile."""
        if not self.dimension_weights:
            return 0.5
            
        weighted_sum = 0.0
        total_weight = 0.0
        
        for dim, weight in self.dimension_weights.items():
            weighted_sum += profile.get(dim, 0.5) * weight
            total_weight += weight
            
        return weighted_sum / total_weight if total_weight > 0 else 0.5
        
    def adapt_description(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Adapt zone description based on user's profile."""
        # Override in specific zone classes
        return self.description
        
    def get_available_challenges(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> List[ContentItem]:
        """Get challenges appropriate for the user's profile."""
        # Override in specific zone classes
        return []
        
    def process_interaction(
        self,
        interaction_type: str,
        context: str,
        duration: float,
        metadata: Optional[Dict] = None
    ) -> Dict[ProfileDimension, float]:
        """Process user interaction and return dimension impacts."""
        # Override in specific zone classes
        return {}
        
    def get_mastery_requirements(self) -> Dict[ProfileDimension, float]:
        """Get the dimension values required to master this zone."""
        return {
            dim: 0.8  # Default mastery threshold
            for dim in self.required_dimensions
        }
        
    def calculate_mastery_progress(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> float:
        """Calculate user's progress towards mastering this zone."""
        if not self.required_dimensions:
            return 0.0
            
        requirements = self.get_mastery_requirements()
        progress_values = []
        
        for dim, required in requirements.items():
            current = profile.get(dim, 0.0)
            progress = min(1.0, current / required)
            progress_values.append(progress)
            
        return sum(progress_values) / len(progress_values)
        
    def get_guidance_message(
        self,
        profile: Dict[ProfileDimension, float]
    ) -> str:
        """Get personalized guidance message based on profile."""
        progress = self.calculate_mastery_progress(profile)
        
        if progress < 0.3:
            return "You are beginning your journey in this pond. Take time to observe and learn."
        elif progress < 0.6:
            return "You are making progress. Focus on understanding the pond's deeper meanings."
        elif progress < 0.9:
            return "You are approaching mastery. Seek the subtle truths within."
        else:
            return "You have achieved deep understanding of this pond's wisdom." 
        
    @abstractmethod
    def start_challenge(self, challenge: ContentItem, player: Any) -> bool:
        """Start a challenge for the player.
        
        Args:
            challenge: The challenge to start
            player: The player attempting the challenge
            
        Returns:
            bool: True if challenge started successfully
        """
        pass 