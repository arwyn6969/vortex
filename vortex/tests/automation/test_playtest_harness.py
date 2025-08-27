"""Tests for the automated playtesting harness."""

import pytest
from unittest.mock import Mock, patch
import asyncio
from datetime import datetime

from ...src.core.user_profiling.profile_matrix import ProfileDimension
from ...src.guides.dialogue import GuidePersona, GuidanceStyle
from .playtest_harness import PlaytestHarness, PlaytestScenario, PlaytestResult

@pytest.fixture
def harness(event_loop):
    """Create a playtest harness instance."""
    harness = PlaytestHarness()
    yield harness
    event_loop.run_until_complete(harness.cleanup())

@pytest.fixture
def mock_dialogue_manager():
    """Create a mock dialogue manager."""
    manager = Mock()
    async def mock_generate_response(*args, **kwargs):
        return "Mock response that demonstrates wisdom and understanding."
    manager.generate_response = mock_generate_response
    return manager

@pytest.fixture
def mock_validator():
    """Create a mock validator."""
    validator = Mock()
    async def mock_validate(*args, **kwargs):
        return Mock(
            is_valid=True,
            score=0.9,
            issues=[],
            recommendations=[],
            metadata={
                "component_scores": {
                    "personality_consistency": 0.85,
                    "cultural_sensitivity": 0.95,
                    "response_quality": 0.88
                }
            },
            timestamp=datetime.now()
        )
    validator.validate_response = mock_validate
    return validator

@pytest.mark.asyncio
async def test_scenario_creation(harness):
    """Test creation of standard scenarios."""
    scenarios = harness.create_standard_scenarios()
    
    assert len(scenarios) > 0
    for scenario in scenarios:
        assert isinstance(scenario, PlaytestScenario)
        assert scenario.name
        assert scenario.description
        assert isinstance(scenario.initial_profile, dict)
        assert isinstance(scenario.guide_persona, GuidePersona)
        assert len(scenario.interaction_sequence) > 0
        assert isinstance(scenario.expected_outcomes, dict)
        assert isinstance(scenario.validation_rules, dict)

@pytest.mark.asyncio
async def test_successful_scenario_run(harness, mock_dialogue_manager, mock_validator):
    """Test running a successful scenario."""
    # Replace real components with mocks
    harness.dialogue_manager = mock_dialogue_manager
    harness.validator = mock_validator
    
    # Get a test scenario
    scenario = harness.create_standard_scenarios()[0]
    
    # Run the scenario
    result = await harness.run_scenario(scenario)
    
    assert isinstance(result, PlaytestResult)
    assert result.success
    assert result.scenario_name == scenario.name
    assert len(result.validation_scores) > 0
    assert len(result.issues_found) == 0
    assert len(result.response_times) == len(scenario.interaction_sequence)
    assert result.total_duration > 0

@pytest.mark.asyncio
async def test_error_handling_scenario(harness, mock_dialogue_manager, mock_validator):
    """Test handling of errors during scenario execution."""
    # Make dialogue manager fail
    async def mock_failed_response(*args, **kwargs):
        raise Exception("Simulated error")
    mock_dialogue_manager.generate_response = mock_failed_response
    harness.dialogue_manager = mock_dialogue_manager
    
    # Get error handling scenario
    scenario = [s for s in harness.create_standard_scenarios() 
               if s.name == "error_handling"][0]
    
    # Run the scenario
    result = await harness.run_scenario(scenario)
    
    assert isinstance(result, PlaytestResult)
    assert not result.success
    assert len(result.issues_found) > 0
    assert "Simulated error" in str(result.issues_found[0])

@pytest.mark.asyncio
async def test_validation_rule_checking(harness, mock_dialogue_manager, mock_validator):
    """Test validation rule checking in scenarios."""
    # Make validator return low scores
    async def mock_low_score(*args, **kwargs):
        return Mock(
            is_valid=False,
            score=0.5,
            issues=["Low quality response"],
            recommendations=["Improve response quality"],
            metadata={
                "component_scores": {
                    "personality_consistency": 0.5,
                    "cultural_sensitivity": 0.5,
                    "response_quality": 0.5
                }
            },
            timestamp=datetime.now()
        )
    mock_validator.validate_response = mock_low_score
    harness.validator = mock_validator
    harness.dialogue_manager = mock_dialogue_manager
    
    # Get a test scenario with high validation requirements
    scenario = harness.create_standard_scenarios()[0]
    
    # Run the scenario
    result = await harness.run_scenario(scenario)
    
    assert not result.success
    assert len(result.issues_found) > 0
    assert any("validation rule" in issue.lower() for issue in result.issues_found)

@pytest.mark.asyncio
async def test_response_time_monitoring(harness, mock_dialogue_manager, mock_validator):
    """Test monitoring of response times."""
    # Make dialogue manager slow
    async def mock_slow_response(*args, **kwargs):
        await asyncio.sleep(0.1)  # Simulate slow response
        return "Slow response"
    mock_dialogue_manager.generate_response = mock_slow_response
    harness.dialogue_manager = mock_dialogue_manager
    harness.validator = mock_validator
    
    # Get a test scenario with strict timing requirements
    scenario = harness.create_standard_scenarios()[0]
    scenario.expected_outcomes["max_response_time"] = 0.05  # Set very low timeout
    
    # Run the scenario
    result = await harness.run_scenario(scenario)
    
    assert not result.success
    assert len(result.issues_found) > 0
    assert any("response time exceeded" in issue.lower() for issue in result.issues_found)
    assert all(t > 0.1 for t in result.response_times)

@pytest.mark.asyncio
async def test_report_generation(harness, mock_dialogue_manager, mock_validator):
    """Test generation of playtest reports."""
    harness.dialogue_manager = mock_dialogue_manager
    harness.validator = mock_validator
    
    # Run all scenarios
    await harness.run_all_scenarios()
    
    # Generate report
    report = harness.generate_report()
    
    assert isinstance(report, str)
    assert "Vortex Automated Playtest Report" in report
    assert "Overall Statistics" in report
    assert "Scenario Results" in report
    for result in harness.results:
        assert result.scenario_name in report

@pytest.mark.asyncio
async def test_cleanup(harness):
    """Test cleanup of resources."""
    # Mock the AI service close method
    mock_close = Mock()
    harness.ai_service.close = mock_close
    
    # Run cleanup
    await harness.cleanup()
    
    # Verify cleanup was called
    mock_close.assert_called_once() 