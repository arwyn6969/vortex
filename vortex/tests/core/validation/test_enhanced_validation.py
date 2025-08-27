"""Tests for enhanced validation features."""

import pytest
from typing import Set, Tuple
from vortex.src.core.validation.enhanced_validation import (
    EnhancedValidator,
    PersonalityProfile,
    ContentContext
)

@pytest.fixture
def validator():
    """Create an enhanced validator instance."""
    return EnhancedValidator()

@pytest.fixture
def wise_sage_profile():
    """Create a wise sage personality profile."""
    return PersonalityProfile(
        archetype="wise_sage",
        traits={"wisdom", "patience", "knowledge", "understanding"},
        voice_patterns=[
            r"consider the deeper meaning",
            r"wisdom teaches us",
            r"understand that"
        ],
        taboo_patterns=[
            r"obviously",
            r"simply put",
            r"just do"
        ],
        cultural_context="egyptian",
        wisdom_level=0.9
    )

@pytest.fixture
def content_context():
    """Create a sample content context."""
    return ContentContext(
        topic="ancient_wisdom",
        required_elements={"wisdom", "knowledge", "understanding"},
        prohibited_elements={"obvious", "simple", "just"},
        cultural_references={"egyptian", "ancient", "sacred"},
        complexity_level=0.8,
        target_length=(50, 200)
    )

def test_personality_validation_good_content(validator, wise_sage_profile):
    """Test personality validation with good content."""
    content = """
    Consider the deeper meaning of wisdom as we explore this ancient knowledge.
    Understanding comes through patient reflection and contemplation.
    Let us seek wisdom together on this sacred path.
    """
    
    score, issues, recommendations = validator.validate_personality(content, wise_sage_profile)
    
    assert score >= 0.9
    assert len(issues) == 0
    assert len(recommendations) == 0

def test_personality_validation_poor_content(validator, wise_sage_profile):
    """Test personality validation with poor content."""
    content = """
    Obviously, this is a simple solution. Just do what I tell you
    and don't think too much about it. It's really not that complicated.
    """
    
    score, issues, recommendations = validator.validate_personality(content, wise_sage_profile)
    
    assert score < 0.8
    assert len(issues) > 0
    assert len(recommendations) > 0
    assert any("inappropriate pattern" in issue for issue in issues)

def test_cultural_sensitivity_good_content(validator):
    """Test cultural sensitivity validation with good content."""
    content = """
    The ancient Egyptian tradition offers profound wisdom through its sacred texts.
    We can learn from these teachings while respecting their cultural context.
    """
    
    score, issues, recommendations = validator.validate_cultural_sensitivity(
        content,
        "egyptian"
    )
    
    assert score >= 0.9
    assert len(issues) == 0
    assert len(recommendations) == 0

def test_cultural_sensitivity_poor_content(validator):
    """Test cultural sensitivity validation with poor content."""
    content = """
    These people always had strange practices. Their kind typically
    believes in mystical things that don't make sense to modern people.
    We can just take their wisdom and use it our way.
    """
    
    score, issues, recommendations = validator.validate_cultural_sensitivity(
        content,
        "egyptian"
    )
    
    assert score < 0.7
    assert len(issues) > 0
    assert len(recommendations) > 0
    assert any("stereotyping" in issue for issue in issues)

def test_dynamic_content_validation_good_content(validator, content_context):
    """Test dynamic content validation with good content."""
    content = """
    Let us explore the profound wisdom contained within ancient Egyptian knowledge.
    Through understanding these sacred teachings, we can gain deeper insight into
    universal truths. Consider how this understanding can be applied with respect
    and reverence for its cultural origins. Furthermore, this wisdom teaches us
    about the interconnected nature of all things.
    """
    
    score, issues, recommendations = validator.validate_dynamic_content(
        content,
        content_context
    )
    
    assert score >= 0.9
    assert len(issues) == 0
    assert len(recommendations) == 0

def test_dynamic_content_validation_poor_content(validator, content_context):
    """Test dynamic content validation with poor content."""
    content = "This is a simple and obvious explanation."
    
    score, issues, recommendations = validator.validate_dynamic_content(
        content,
        content_context
    )
    
    assert score < 0.8
    assert len(issues) > 0
    assert len(recommendations) > 0
    assert any("length" in issue for issue in issues)

def test_improvement_suggestions(validator, wise_sage_profile, content_context):
    """Test improvement suggestions generation."""
    content = """
    Obviously, this is just a simple explanation of their practices.
    These people have always done things this way, and we can use their
    wisdom for our own purposes.
    """
    
    suggestions = validator.get_improvement_suggestions(
        content,
        wise_sage_profile,
        content_context
    )
    
    assert len(suggestions) > 0
    assert any("culturally sensitive" in suggestion for suggestion in suggestions)
    assert any("appropriate language" in suggestion for suggestion in suggestions)
    assert any("content structure" in suggestion for suggestion in suggestions)

def test_personality_validation_archetype_patterns(validator, wise_sage_profile):
    """Test validation against specific archetype patterns."""
    content = """
    Consider the deeper meaning of these teachings.
    Wisdom shows us that patience leads to understanding.
    Let us reflect upon these ancient truths together.
    """
    
    score, issues, recommendations = validator.validate_personality(content, wise_sage_profile)
    
    assert score >= 0.9
    assert len(issues) == 0
    for pattern in wise_sage_profile.voice_patterns:
        assert any(re.search(pattern, content, re.IGNORECASE) for pattern in wise_sage_profile.voice_patterns)

def test_cultural_sensitivity_appropriation(validator):
    """Test detection of cultural appropriation risks."""
    content = """
    We can take their sacred practices and use them in our modern context.
    Let's copy their ancient rituals for our own purposes.
    """
    
    score, issues, recommendations = validator.validate_cultural_sensitivity(
        content,
        "egyptian"
    )
    
    assert score < 0.8
    assert any("appropriation" in issue.lower() for issue in issues)
    assert any("respectful" in recommendation.lower() for recommendation in recommendations)

def test_quality_metrics_validation(validator, content_context):
    """Test content quality metrics validation."""
    content = """
    Consider this example of ancient wisdom. Furthermore, it illustrates
    the deep connection between knowledge and understanding. Therefore,
    we can explore these concepts together. Moreover, this helps us
    reflect on the true meaning of these teachings.
    """
    
    score, issues, recommendations = validator.validate_dynamic_content(
        content,
        content_context
    )
    
    assert score >= 0.8
    for metric in validator.QUALITY_METRICS:
        patterns = validator.QUALITY_METRICS[metric]["patterns"]
        assert any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns) 