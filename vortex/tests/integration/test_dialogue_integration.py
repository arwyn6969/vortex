"""
Integration tests for the LLM dialogue system with other components.
"""
import pytest
from typing import Dict, Set
from unittest.mock import Mock, patch
import time

from ...src.guides.llm_dialogue import (
    LLMDialogueGenerator,
    DialogueContext,
    DialogueError,
    ResponseValidationError
)
from ...src.guides.base_guide import Guide
from ...src.core.user_profiling.profile_matrix import ProfileDimension
from ...src.mythology.archetype_manager import CulturalSystem, ArchetypeManager
from ...src.zones.base_zone import Zone
from ...src.core.progression import VirtueMeter

class TestGuide(Guide):
    """Test implementation of Guide class."""
    def __init__(self):
        super().__init__(
            name="Maat",
            archetype_name="wisdom_keeper",
            cultural_system=CulturalSystem.EGYPTIAN,
            attributes={"wisdom", "justice", "truth"}
        )

class TestZone(Zone):
    """Test implementation of Zone class."""
    def __init__(self):
        self.name = "Wisdom Pond"
        self.virtue_meter = VirtueMeter()
        self.current_challenge = None

@pytest.fixture
def mock_llm():
    """Create a mock LLM client."""
    with patch("vortex.src.guides.llm_dialogue.DeepseekClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client

@pytest.fixture
def test_guide():
    """Create a test guide instance."""
    return TestGuide()

@pytest.fixture
def test_zone():
    """Create a test zone instance."""
    return TestZone()

def test_guide_zone_dialogue_integration(mock_llm, test_guide, test_zone):
    """Test dialogue integration with guide and zone interactions."""
    # Connect guide to zone
    test_guide.connect_to_zone(test_zone)
    
    # Setup mock response
    mock_llm.generate.return_value = (
        "As Maat, I sense the wisdom of this pond resonating with your spirit. "
        "The waters here reflect the eternal truth we seek."
    )
    
    # Simulate user interaction in zone context
    response = test_guide.generate_response(
        "What can you tell me about this place?",
        profile={
            ProfileDimension.WISDOM: 0.7,
            ProfileDimension.MORAL_ALIGNMENT: 0.8
        },
        context={"zone": test_zone.name}
    )
    
    # Verify response includes both guide and zone context
    assert "Maat" in response
    assert "wisdom" in response.lower()
    assert "pond" in response.lower()
    
    # Verify zone consciousness was updated
    assert test_guide.consciousness["attunement"]["strength"] > 0.5
    assert test_guide.consciousness["communion"]["channel_strength"] > 0.5

def test_profile_adaptation_integration(mock_llm, test_guide):
    """Test dialogue adaptation based on user profile changes."""
    initial_profile = {
        ProfileDimension.WISDOM: 0.5,
        ProfileDimension.MORAL_ALIGNMENT: 0.5,
        ProfileDimension.EMPATHY: 0.5
    }
    
    evolved_profile = {
        ProfileDimension.WISDOM: 0.8,
        ProfileDimension.MORAL_ALIGNMENT: 0.7,
        ProfileDimension.EMPATHY: 0.9
    }
    
    # Initial interaction
    mock_llm.generate.return_value = "Maat speaks with measured wisdom."
    response1 = test_guide.generate_response(
        "Guide me in wisdom.",
        profile=initial_profile
    )
    initial_style = test_guide.guidance_style.copy()
    
    # Interaction with evolved profile
    mock_llm.generate.return_value = "Maat embraces your growth with nurturing wisdom."
    response2 = test_guide.generate_response(
        "I seek deeper understanding.",
        profile=evolved_profile
    )
    
    # Verify guidance style adapted
    assert test_guide.guidance_style["nurturing"] > initial_style["nurturing"]
    assert test_guide.guidance_style["ethical"] > initial_style["ethical"]

def test_cultural_context_integration(mock_llm, test_guide):
    """Test dialogue integration with cultural context."""
    # Setup archetype manager
    archetype_manager = ArchetypeManager()
    
    # Simulate interactions with different cultural contexts
    contexts = [
        {"cultural_focus": "egyptian", "theme": "justice"},
        {"cultural_focus": "mayan", "theme": "balance"},
        {"cultural_focus": "dogon", "theme": "wisdom"}
    ]
    
    responses = []
    for ctx in contexts:
        mock_llm.generate.return_value = f"Maat speaks of {ctx['theme']} across traditions."
        response = test_guide.generate_response(
            f"Tell me about {ctx['theme']}.",
            profile={ProfileDimension.WISDOM: 0.7},
            context=ctx
        )
        responses.append(response)
    
    # Verify cultural adaptability
    assert all("Maat" in r for r in responses)
    assert len(test_guide.interaction_history) == len(contexts)

def test_behavioral_feedback_integration(mock_llm, test_guide, test_zone):
    """Test dialogue integration with behavioral feedback system."""
    # Setup initial state
    test_guide.connect_to_zone(test_zone)
    initial_profile = {ProfileDimension.WISDOM: 0.5}
    
    # Simulate behavioral feedback loop
    for i in range(3):
        # User shows increasing wisdom
        profile = {
            ProfileDimension.WISDOM: min(1.0, 0.5 + (i * 0.2)),
            ProfileDimension.MORAL_ALIGNMENT: 0.7
        }
        
        mock_llm.generate.return_value = f"Maat acknowledges your growing wisdom."
        response = test_guide.generate_response(
            "Share your wisdom.",
            profile=profile,
            context={"zone": test_zone.name}
        )
        
        # Verify guide and zone adapt to behavioral changes
        assert test_guide.calculate_affinity(profile) > 0.5
        assert test_guide.consciousness["teaching"]["mode"] == (
            "active" if profile[ProfileDimension.WISDOM] > 0.7 else "receptive"
        )

def test_multi_component_interaction(mock_llm, test_guide, test_zone):
    """Test complex interactions between multiple system components."""
    test_guide.connect_to_zone(test_zone)
    
    # Simulate a complex interaction scenario
    scenario = {
        "zone_state": {"challenge_active": True, "virtue_level": 0.7},
        "user_profile": {
            ProfileDimension.WISDOM: 0.8,
            ProfileDimension.MORAL_ALIGNMENT: 0.7,
            ProfileDimension.EMPATHY: 0.6
        },
        "cultural_context": {"focus": "egyptian", "theme": "truth"},
        "behavioral_flags": {"insight_gained": True, "challenge_completed": True}
    }
    
    # Update zone state
    test_zone.virtue_meter.value = scenario["zone_state"]["virtue_level"]
    
    mock_llm.generate.return_value = (
        "Maat's wisdom flows through the pond, acknowledging your growth in truth."
    )
    
    # Generate response in complex context
    response = test_guide.generate_response(
        "What have I learned?",
        profile=scenario["user_profile"],
        context={
            "zone": test_zone.name,
            "cultural_context": scenario["cultural_context"],
            "behavioral_flags": scenario["behavioral_flags"]
        }
    )
    
    # Verify system-wide integration
    assert "Maat" in response
    assert "truth" in response.lower() or "wisdom" in response.lower()
    assert test_guide.consciousness["attunement"]["clarity"] > 0.5
    assert len(test_guide.interaction_history) > 0
    assert test_guide.calculate_affinity(scenario["user_profile"]) > 0.6

def test_guide_handoff_interaction(mock_llm, test_guide):
    """Test guide handoff between different cultural contexts."""
    # Simulate transition from Egyptian to Mayan wisdom
    mock_llm.generate.return_value = (
        "As Maat, I sense another guide's wisdom would serve you well here. "
        "Let me introduce you to Itzamna, keeper of Mayan wisdom."
    )
    
    response = test_guide.generate_response(
        "I'm interested in Mayan astronomy.",
        profile={ProfileDimension.WISDOM: 0.8},
        context={"transition_to": "mayan"}
    )
    
    assert "Maat" in response
    assert "Itzamna" in response
    assert test_guide.should_adapt_personality({"transition_to": "mayan"})

def test_emotional_state_integration(mock_llm, test_guide):
    """Test dialogue adaptation to user's emotional state."""
    emotional_states = [
        {"emotion": "confused", "intensity": 0.8},
        {"emotion": "inspired", "intensity": 0.9},
        {"emotion": "frustrated", "intensity": 0.7}
    ]
    
    responses = []
    for state in emotional_states:
        mock_llm.generate.return_value = (
            f"Maat senses your {state['emotion']} spirit and adjusts accordingly."
        )
        response = test_guide.generate_response(
            "Guide me through this.",
            profile={ProfileDimension.EMPATHY: 0.7},
            context={"emotional_state": state}
        )
        responses.append(response)
        
        # Verify guidance style adapts to emotional state
        if state["emotion"] == "confused":
            assert test_guide.guidance_style["nurturing"] > 0.6
        elif state["emotion"] == "inspired":
            assert test_guide.guidance_style["direct"] > 0.5
        elif state["emotion"] == "frustrated":
            assert test_guide.guidance_style["balanced"] > 0.6

def test_challenge_completion_dialogue(mock_llm, test_guide, test_zone):
    """Test dialogue during challenge completion sequence."""
    test_guide.connect_to_zone(test_zone)
    
    # Setup challenge sequence
    challenge_states = [
        {"stage": "initiation", "progress": 0.0},
        {"stage": "progress", "progress": 0.5},
        {"stage": "completion", "progress": 1.0}
    ]
    
    for state in challenge_states:
        mock_llm.generate.return_value = (
            f"Maat observes your journey through this challenge."
        )
        
        response = test_guide.generate_response(
            "How am I doing?",
            profile={ProfileDimension.WISDOM: 0.7},
            context={
                "zone": test_zone.name,
                "challenge_state": state
            }
        )
        
        # Verify appropriate challenge stage handling
        if state["stage"] == "initiation":
            assert test_guide.consciousness["teaching"]["mode"] == "receptive"
        elif state["stage"] == "completion":
            assert test_guide.consciousness["teaching"]["mode"] == "active"
            assert test_guide.consciousness["attunement"]["clarity"] > 0.7

def test_memory_persistence_integration(mock_llm, test_guide):
    """Test dialogue memory persistence and recall."""
    # Simulate a sequence of related interactions
    conversation_sequence = [
        ("Tell me about truth.", "Maat speaks of eternal truth."),
        ("How does this relate to justice?", "Maat connects truth with justice."),
        ("I see the connection!", "Maat acknowledges your understanding.")
    ]
    
    for question, answer in conversation_sequence:
        mock_llm.generate.return_value = answer
        response = test_guide.generate_response(
            question,
            profile={ProfileDimension.WISDOM: 0.7},
            context={"theme": "truth_and_justice"}
        )
    
    # Verify memory retention
    assert len(test_guide.interaction_history) == 3
    assert any("truth" in interaction["metadata"]["input"] 
              for interaction in test_guide.interaction_history)
    
    # Test memory recall in new response
    mock_llm.generate.return_value = (
        "Maat recalls our discussion of truth and justice."
    )
    recall_response = test_guide.generate_response(
        "What have we discussed so far?",
        profile={ProfileDimension.WISDOM: 0.7}
    )
    assert "truth" in recall_response.lower()
    assert "justice" in recall_response.lower()

def test_error_recovery_integration(mock_llm, test_guide, test_zone):
    """Test system recovery from various error conditions."""
    test_guide.connect_to_zone(test_zone)
    
    # Test LLM failure recovery
    mock_llm.generate.side_effect = Exception("LLM Error")
    response = test_guide.generate_response(
        "Hello",
        profile={ProfileDimension.WISDOM: 0.7}
    )
    assert "Maat" in response  # Should use fallback
    
    # Test zone disconnection recovery
    test_guide.consciousness["communion"]["channel_strength"] = 0.2
    response = test_guide.generate_response(
        "What about this place?",
        profile={ProfileDimension.WISDOM: 0.7},
        context={"zone": test_zone.name}
    )
    assert response is not None
    assert test_guide.consciousness["communion"]["channel_strength"] < 0.3

def test_rapid_interaction_stability(mock_llm, test_guide):
    """Test system stability under rapid interactions."""
    mock_llm.generate.return_value = "Maat responds with wisdom."
    
    # Simulate rapid-fire interactions
    start_time = time.time()
    for i in range(10):
        response = test_guide.generate_response(
            f"Quick question {i}",
            profile={ProfileDimension.WISDOM: 0.7}
        )
        assert response is not None
        
    # Verify system remains stable
    assert len(test_guide.interaction_history) == 10
    assert time.time() - start_time < 5  # Should handle rapid interactions efficiently

def test_cross_cultural_wisdom_integration(mock_llm, test_guide):
    """Test integration of wisdom across different cultural systems."""
    wisdom_concepts = [
        {
            "egyptian": "Ma'at (cosmic order)",
            "mayan": "Hunab Ku (supreme consciousness)",
            "theme": "universal_order"
        },
        {
            "egyptian": "Thoth (wisdom)",
            "mayan": "Itzamna (wisdom)",
            "theme": "divine_wisdom"
        }
    ]
    
    for concept in wisdom_concepts:
        mock_llm.generate.return_value = (
            f"Maat speaks of {concept['egyptian']}, "
            f"which resonates with {concept['mayan']}."
        )
        
        response = test_guide.generate_response(
            f"How does {concept['egyptian']} relate to {concept['mayan']}?",
            profile={ProfileDimension.WISDOM: 0.8},
            context={"wisdom_concept": concept}
        )
        
        assert concept['egyptian'] in response
        assert concept['mayan'] in response
        assert test_guide.consciousness["attunement"]["clarity"] > 0.6

def test_virtue_progression_dialogue(mock_llm, test_guide, test_zone):
    """Test dialogue adaptation to virtue progression."""
    test_guide.connect_to_zone(test_zone)
    
    virtue_levels = [0.3, 0.5, 0.7, 0.9]
    for level in virtue_levels:
        test_zone.virtue_meter.value = level
        
        mock_llm.generate.return_value = (
            f"Maat observes your progress in wisdom."
        )
        
        response = test_guide.generate_response(
            "How am I progressing?",
            profile={
                ProfileDimension.WISDOM: level,
                ProfileDimension.MORAL_ALIGNMENT: level
            },
            context={"zone": test_zone.name}
        )
        
        # Verify teaching adaptation to virtue level
        if level < 0.5:
            assert test_guide.consciousness["teaching"]["approach"] == "subtle"
        else:
            assert test_guide.consciousness["teaching"]["approach"] == "direct"
            
        # Verify attunement increases with virtue
        assert test_guide.consciousness["attunement"]["strength"] >= level 