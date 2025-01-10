"""
Demo script showing how to use the new GUI interface for Vortex of Enlightenment.
"""
import sys
import os
from pathlib import Path
import time
from typing import Dict

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.ui.interface import VortexInterface, UIMode
from src.core.user_profiling.profile_matrix import ProfileMatrix, ProfileDimension

def create_demo_profile(profile_matrix: ProfileMatrix, user_id: str = "demo_user"):
    """Create a demo profile with some interesting personality traits."""
    # Create initial profile
    profile = profile_matrix.create_profile(user_id)
    
    # Set up an analytical but empathetic personality
    dimensions = {
        ProfileDimension.STRATEGIC_THINKING: 0.8,
        ProfileDimension.DECISION_MAKING: 0.7,
        ProfileDimension.EMPATHY: 0.6,
        ProfileDimension.EMOTIONAL_RESPONSE: 0.6,
        ProfileDimension.CREATIVITY: 0.4,
        ProfileDimension.QUANTUM_INTUITION: 0.5,
        ProfileDimension.DREAM_LOGIC: 0.3,
        ProfileDimension.METAPHORICAL_THINKING: 0.4,
        ProfileDimension.ADAPTABILITY: 0.6,
        ProfileDimension.RISK_TOLERANCE: 0.4,
        ProfileDimension.MORAL_ALIGNMENT: 0.7,
        ProfileDimension.SOCIAL_AWARENESS: 0.6,
        ProfileDimension.CONSCIOUSNESS_DEPTH: 0.5,
        ProfileDimension.CONTEXTUAL_FLUIDITY: 0.6,
        ProfileDimension.TEMPORAL_AWARENESS: 0.7,
        ProfileDimension.SYNCHRONICITY_AWARENESS: 0.4,
        ProfileDimension.EMERGENT_CREATIVITY: 0.5,
        ProfileDimension.SENSORY_INTEGRATION: 0.6
    }
    
    # Update profile with high confidence
    for dimension, value in dimensions.items():
        profile_matrix.update_profile(
            user_id,
            dimension,
            value,
            confidence=0.9
        )
    
    return profile

def simulate_location_changes(interface: VortexInterface):
    """Simulate moving through different locations to show context-aware responses."""
    locations = [
        ("Wisdom Pond", "You approach the serene Wisdom Pond, its surface reflecting ancient knowledge."),
        ("Temple of Reflection", "You enter the Temple of Reflection, where thoughts echo through time."),
        ("Challenge Chamber", "You stand before the Challenge Chamber, ready to test your understanding."),
        ("Library of Ages", "You browse the Library of Ages, surrounded by timeless wisdom.")
    ]
    
    for location, description in locations:
        interface.display_message(f"\n{description}")
        interface.set_location(location)
        time.sleep(2)  # Pause to show the transition

def main():
    """Run the GUI demo."""
    # Create profile matrix and demo profile
    profile_matrix = ProfileMatrix()
    create_demo_profile(profile_matrix)
    
    # Create the interface in GUI mode with our profile matrix
    interface = VortexInterface(
        mode=UIMode.GUI,
        profile_matrix=profile_matrix
    )
    
    # Show the introduction
    interface.show_intro()
    
    # Update some example stats
    interface.update_stats({
        "Level": "5",
        "Experience": "450/1000",
        "Wisdom": "75",
        "Progress": "45%"
    })
    
    # Display welcome messages
    interface.display_message("Welcome to the Vortex of Enlightenment GUI demo!")
    interface.display_message(
        "This demo showcases our dynamic response system that adapts to your personality.",
        message_type="system"
    )
    interface.display_message(
        "The quick response buttons will change based on your personality traits and current context.",
        message_type="system"
    )
    
    # Start location simulation in a separate thread to not block the GUI
    import threading
    simulation_thread = threading.Thread(
        target=simulate_location_changes,
        args=(interface,)
    )
    simulation_thread.daemon = True
    simulation_thread.start()
    
    # Start the GUI
    try:
        interface.start()
    except KeyboardInterrupt:
        interface.stop()

if __name__ == "__main__":
    main() 