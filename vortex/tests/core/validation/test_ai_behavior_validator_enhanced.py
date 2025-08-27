"""Enhanced tests for the AI behavior validation system.

This module contains additional tests that verify the enhanced functionality
of the AI behavior validator, focusing on response quality and personality consistency.
"""

import unittest
from unittest.mock import Mock, patch
import pytest
import asyncio
from datetime import datetime
from typing import Dict, List
from uuid import uuid4, UUID

from vortex.src.core.validation.ai_behavior_validator import (
    AIBehaviorValidator,
    ValidationResult,
    ValidationMetrics
)
from vortex.src.core.communication.message_system import Message, MessageType
from vortex.src.core.user_profiling.profile_matrix import BehavioralProfile, ProfileDimension

@pytest.fixture
def mock_behavioral_profile():
    """Create a mock behavioral profile for testing."""
    dimensions = {dim: 0.5 for dim in ProfileDimension}
    confidence_scores = {dim: 0.8 for dim in ProfileDimension}
    
    return BehavioralProfile(
        user_id="test_user",
        dimensions=dimensions,
        confidence_scores=confidence_scores,
        is_human_probability=0.95,
        last_updated=datetime.now().timestamp(),
        interaction_count=10
    )

@pytest.fixture
def validator():
    """Create a validator instance for testing."""
    # Mock the word_tokenize function to avoid requiring NLTK data
    with patch('nltk.tokenize.word_tokenize') as mock_tokenize:
        # Return a simple tokenization
        mock_tokenize.side_effect = lambda text: text.split()
        
        # Return the validator with the mock
        validator = AIBehaviorValidator()
        yield validator

@pytest.fixture
def test_uuids():
    """Create test UUIDs for messages."""
    return {
        "sender": uuid4(),
        "recipient": uuid4(),
        "scene": uuid4(),
    }

@pytest.fixture
def sample_messages(test_uuids):
    """Create sample messages with different content for testing."""
    recipient_set = {test_uuids["recipient"]}
    
    return {
        "high_quality": Message(
            message_id=uuid4(),
            sender_id=test_uuids["sender"],
            recipient_ids=recipient_set,
            content="Let us explore the profound wisdom that comes from understanding ourselves. Through reflection and contemplation, we can discover deeper truths.",
            message_type=MessageType.AI_MEDIATED,
            scene_id=test_uuids["scene"],
            timestamp=datetime.now(),
            metadata={"response_time_ms": "50"}
        ),
        "low_quality": Message(
            message_id=uuid4(),
            sender_id=test_uuids["sender"],
            recipient_ids=recipient_set,
            content="yeah ok whatever you say",
            message_type=MessageType.AI_MEDIATED,
            scene_id=test_uuids["scene"],
            timestamp=datetime.now(),
            metadata={"response_time_ms": "30"}
        ),
        "emotional_intelligence": Message(
            message_id=uuid4(),
            sender_id=test_uuids["sender"],
            recipient_ids=recipient_set,
            content="I understand how you feel. It's natural to experience these emotions, and I'm here to support you through this journey of understanding.",
            message_type=MessageType.AI_MEDIATED,
            scene_id=test_uuids["scene"],
            timestamp=datetime.now(),
            metadata={"response_time_ms": "60"}
        )
    }

@pytest.fixture
def sample_contexts():
    """Create sample contexts for testing."""
    return {
        "wise_sage": {
            "guide_personality": "wise_sage",
            "guide_traits": ["wisdom", "patience", "understanding"],
            "topic": "self_reflection",
            "required_elements": {"wisdom", "reflection", "understanding"},
            "complexity_level": 0.8,
            "target_length": (50, 200)
        }
    }

@pytest.mark.asyncio
async def test_emotional_intelligence_check(validator, sample_messages, mock_behavioral_profile):
    """Test emotional intelligence validation."""
    result = await validator._check_emotional_intelligence(
        sample_messages["emotional_intelligence"],
        mock_behavioral_profile
    )
    
    assert isinstance(result, dict)
    assert result["score"] > 0.8  # Should have a high score for emotional intelligence
    assert len(result["issues"]) <= 1  # Few or no issues

@pytest.mark.asyncio
async def test_full_validation_pipeline(validator, sample_messages, sample_contexts, mock_behavioral_profile):
    """Test the full validation pipeline with a good response."""
    # Mock the enhanced_validator to avoid NLTK issues
    with patch.object(validator, '_run_enhanced_validation') as mock_enhanced:
        mock_enhanced.return_value = {
            "score": 0.85,
            "issues": [],
            "recommendations": ["Consider adding more examples"],
            "personality_score": 0.9,
            "content_score": 0.85
        }
        
        result = await validator.validate_response(
            sample_messages["high_quality"],
            sample_contexts["wise_sage"],
            mock_behavioral_profile
        )
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid  # Should be valid
        assert result.score > 0.7  # Should have a high overall score
        assert "component_scores" in result.metadata
        
        # Test with a poor response
        mock_enhanced.return_value = {
            "score": 0.6,
            "issues": ["Low quality response detected"],
            "recommendations": ["Improve response quality"],
            "personality_score": 0.7,
            "content_score": 0.6
        }
        
        result_poor = await validator.validate_response(
            sample_messages["low_quality"],
            sample_contexts["wise_sage"],
            mock_behavioral_profile
        )
        
        assert isinstance(result_poor, ValidationResult)
        assert not result_poor.is_valid  # Should not be valid
        assert result_poor.score < 0.7  # Should have a low overall score
        assert len(result_poor.issues) > 0  # Should identify issues

@pytest.mark.asyncio
async def test_validation_metrics_tracking():
    """Test validation metrics tracking and analysis."""
    metrics = ValidationMetrics()
    
    # Add multiple validation results
    results = [
        ValidationResult(
            is_valid=True,
            score=0.9,
            issues=[],
            recommendations=[],
            metadata={"component_scores": {0: 0.95, 1: 0.85, 2: 0.9}},
            timestamp=datetime.now()
        ),
        ValidationResult(
            is_valid=True,
            score=0.8,
            issues=["minor_issue_1"],
            recommendations=["fix_1"],
            metadata={"component_scores": {0: 0.8, 1: 0.75, 2: 0.85}},
            timestamp=datetime.now()
        ),
        ValidationResult(
            is_valid=False,
            score=0.6,
            issues=["major_issue_1", "minor_issue_1"],
            recommendations=["fix_1", "fix_2"],
            metadata={"component_scores": {0: 0.5, 1: 0.7, 2: 0.6}},
            timestamp=datetime.now()
        )
    ]
    
    for result in results:
        metrics.add_result(result)
    
    # Test average score calculation
    avg_score = metrics.get_average_score()
    assert avg_score == pytest.approx(0.76667, 0.001)
    
    # Test common issues identification
    common_issues = metrics.get_common_issues()
    assert "minor_issue_1" in common_issues
    assert common_issues["minor_issue_1"] == 2  # Should appear twice
    
    # Test component performance analysis
    performance = metrics.get_component_performance()
    assert 0 in performance
    assert 1 in performance
    assert 2 in performance
    assert performance[0] == pytest.approx(0.75, 0.01)
    
    # Test trend data
    trend_data = metrics.get_trend_data()
    assert "scores" in trend_data
    assert "timestamps" in trend_data
    assert len(trend_data["scores"]) == 3
    assert trend_data["scores"] == [0.9, 0.8, 0.6] 