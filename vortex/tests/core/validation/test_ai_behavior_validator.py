"""Tests for the AI behavior validation system."""

import unittest
from unittest.mock import Mock, patch
import pytest
from datetime import datetime
from typing import Dict

from vortex.src.core.validation.ai_behavior_validator import (
    AIBehaviorValidator,
    ValidationResult,
    ValidationMetrics
)
from vortex.src.core.communication.message_system import Message
from vortex.src.core.user_profiling.profile_matrix import BehavioralMatrix

@pytest.fixture
def validator():
    """Create a validator instance for testing."""
    return AIBehaviorValidator()

@pytest.fixture
def sample_message():
    """Create a sample message for testing."""
    return Message(
        message_id="test_id",
        sender_id="test_sender",
        recipient_ids={"test_recipient"},
        content="This is a test message about wisdom and understanding.",
        message_type="test_type",
        scene_id="test_scene",
        timestamp=datetime.now(),
        metadata={}
    )

@pytest.fixture
def sample_context():
    """Create a sample context for testing."""
    return {
        "guide_personality": "wise_sage",
        "guide_traits": ["wisdom", "patience"],
        "topic": "test_topic",
        "required_elements": ["wisdom", "understanding"],
        "complexity_level": 0.8
    }

@pytest.fixture
def behavioral_matrix():
    """Create a sample behavioral matrix for testing."""
    return BehavioralMatrix()  # Assuming default initialization is sufficient for tests

@pytest.mark.asyncio
async def test_validate_response_basic(
    validator,
    sample_message,
    sample_context,
    behavioral_matrix
):
    """Test basic response validation."""
    result = await validator.validate_response(
        sample_message,
        sample_context,
        behavioral_matrix
    )
    
    assert isinstance(result, ValidationResult)
    assert isinstance(result.score, float)
    assert 0.0 <= result.score <= 1.0
    assert isinstance(result.issues, list)
    assert isinstance(result.recommendations, list)
    assert isinstance(result.metadata, dict)
    assert isinstance(result.timestamp, datetime)

@pytest.mark.asyncio
async def test_emotional_intelligence_check(
    validator,
    sample_message,
    behavioral_matrix
):
    """Test emotional intelligence validation."""
    result = await validator._check_emotional_intelligence(
        sample_message,
        behavioral_matrix
    )
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "issues" in result
    assert "recommendations" in result
    assert 0.0 <= result["score"] <= 1.0

@pytest.mark.asyncio
async def test_guide_consistency_check(validator, sample_message, sample_context):
    """Test guide personality consistency validation."""
    result = await validator._check_guide_consistency(sample_message, sample_context)
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "issues" in result
    assert "recommendations" in result
    assert 0.0 <= result["score"] <= 1.0

@pytest.mark.asyncio
async def test_response_quality_check(validator, sample_message):
    """Test response quality validation."""
    result = await validator._check_response_quality(sample_message)
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "issues" in result
    assert "recommendations" in result
    assert 0.0 <= result["score"] <= 1.0

def test_validation_metrics():
    """Test validation metrics tracking."""
    metrics = ValidationMetrics()
    
    # Add some sample results
    results = [
        ValidationResult(
            is_valid=True,
            score=0.8,
            issues=["minor_issue_1"],
            recommendations=["fix_1"],
            metadata={},
            timestamp=datetime.now()
        ),
        ValidationResult(
            is_valid=False,
            score=0.5,
            issues=["major_issue_1", "minor_issue_1"],
            recommendations=["fix_1", "fix_2"],
            metadata={},
            timestamp=datetime.now()
        )
    ]
    
    for result in results:
        metrics.add_result(result)
    
    assert metrics.get_average_score() == 0.65
    common_issues = metrics.get_common_issues()
    assert "minor_issue_1" in common_issues
    assert len(common_issues) > 0

@pytest.mark.asyncio
async def test_mythological_accuracy_check(validator, sample_message):
    """Test mythological accuracy validation."""
    result = await validator._check_mythological_accuracy(sample_message)
    
    assert isinstance(result, dict)
    assert "score" in result
    assert "issues" in result
    assert "recommendations" in result
    assert 0.0 <= result["score"] <= 1.0 