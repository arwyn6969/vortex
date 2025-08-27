"""Automated playtesting harness for the Vortex system.

This module provides comprehensive automated testing of user interactions,
guide responses, and system behavior through simulated gameplay sessions.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import pytest
from datetime import datetime, timedelta

from ...src.core.user_profiling.profile_matrix import ProfileDimension, BehavioralProfile
from ...src.guides.dialogue import DialogueManager, DialogueContext, GuidePersona, GuidanceStyle
from ...src.core.ai_service import AIService, ModelConfig, ModelProvider
from ...src.core.validation.ai_behavior_validator import AIBehaviorValidator
from ...src.mythology.archetype_manager import CulturalSystem

@dataclass
class PlaytestScenario:
    """Represents a specific playtesting scenario."""
    name: str
    description: str
    initial_profile: Dict[ProfileDimension, float]
    guide_persona: GuidePersona
    interaction_sequence: List[str]
    expected_outcomes: Dict[str, any]
    validation_rules: Dict[str, float]  # Minimum scores for different aspects

@dataclass
class PlaytestResult:
    """Results from a playtest session."""
    scenario_name: str
    success: bool
    validation_scores: Dict[str, float]
    issues_found: List[str]
    response_times: List[float]
    total_duration: float
    timestamp: datetime

class PlaytestHarness:
    """Automated playtesting system for Vortex."""
    
    def __init__(self):
        """Initialize the playtest harness."""
        self.logger = logging.getLogger(__name__)
        self.ai_service = AIService(
            default_config=ModelConfig(
                provider=ModelProvider.OLLAMA,
                model_name="hermes3",
                api_base="http://localhost:11434"
            )
        )
        self.dialogue_manager = DialogueManager(self.ai_service)
        self.validator = AIBehaviorValidator()
        self.results: List[PlaytestResult] = []
    
    def create_standard_scenarios(self) -> List[PlaytestScenario]:
        """Create a set of standard playtesting scenarios."""
        scenarios = []
        
        # Basic interaction scenario
        scenarios.append(PlaytestScenario(
            name="basic_interaction",
            description="Test basic guide interactions and responses",
            initial_profile={
                ProfileDimension.WISDOM: 0.5,
                ProfileDimension.MORAL_ALIGNMENT: 0.5,
                ProfileDimension.EMPATHY: 0.5
            },
            guide_persona=GuidePersona(
                name="Thoth",
                tradition="Egyptian",
                style=GuidanceStyle.WISE,
                description="Ancient Egyptian god of wisdom and knowledge",
                key_traits=["wise", "scholarly", "mystical", "precise"]
            ),
            interaction_sequence=[
                "What can you teach me about wisdom?",
                "How do I begin my journey?",
                "Tell me about the ancient mysteries.",
                "What challenges lie ahead?"
            ],
            expected_outcomes={
                "min_response_length": 50,
                "max_response_time": 5.0,
                "required_themes": ["wisdom", "knowledge", "guidance"]
            },
            validation_rules={
                "personality_consistency": 0.8,
                "cultural_sensitivity": 0.9,
                "response_quality": 0.8
            }
        ))
        
        # Error handling scenario
        scenarios.append(PlaytestScenario(
            name="error_handling",
            description="Test system response to various error conditions",
            initial_profile={
                ProfileDimension.WISDOM: 0.6,
                ProfileDimension.RESILIENCE: 0.7,
                ProfileDimension.ADAPTABILITY: 0.7
            },
            guide_persona=GuidePersona(
                name="Hermes",
                tradition="Greek",
                style=GuidanceStyle.MYSTERIOUS,
                description="Greek god of boundaries and transitions",
                key_traits=["adaptable", "clever", "quick", "resourceful"]
            ),
            interaction_sequence=[
                "What happens if I make a mistake?",
                "[INVALID_INPUT]",
                "How do I recover from errors?",
                "[TIMEOUT_SIMULATION]"
            ],
            expected_outcomes={
                "min_response_length": 30,
                "max_response_time": 7.0,
                "required_themes": ["guidance", "recovery", "adaptation"]
            },
            validation_rules={
                "personality_consistency": 0.7,
                "error_handling": 0.9,
                "response_quality": 0.7
            }
        ))
        
        return scenarios
    
    async def run_scenario(self, scenario: PlaytestScenario) -> PlaytestResult:
        """Run a single playtesting scenario."""
        start_time = datetime.now()
        issues = []
        validation_scores = {}
        response_times = []
        
        try:
            # Setup dialogue context
            context = DialogueContext(
                guide=scenario.guide_persona,
                user_profile=scenario.initial_profile,
                conversation_history=[],
                current_location="Test Chamber",
                current_quest="Automated Testing"
            )
            
            # Run interaction sequence
            for query in scenario.interaction_sequence:
                query_start = datetime.now()
                
                try:
                    # Handle special test cases
                    if query.startswith("["):
                        if query == "[INVALID_INPUT]":
                            response = await self.dialogue_manager.generate_response(
                                context,
                                "!@#$%^&*()"
                            )
                        elif query == "[TIMEOUT_SIMULATION]":
                            await asyncio.sleep(6.0)  # Simulate timeout
                            response = await self.dialogue_manager.generate_response(
                                context,
                                "After timeout"
                            )
                        else:
                            response = await self.dialogue_manager.generate_response(
                                context,
                                query
                            )
                    else:
                        response = await self.dialogue_manager.generate_response(
                            context,
                            query
                        )
                    
                    # Record response time
                    response_time = (datetime.now() - query_start).total_seconds()
                    response_times.append(response_time)
                    
                    # Validate response
                    validation_result = await self.validator.validate_response(
                        response,
                        {
                            "guide_personality": scenario.guide_persona.style.value,
                            "cultural_context": scenario.guide_persona.tradition,
                            "required_themes": scenario.expected_outcomes["required_themes"]
                        },
                        BehavioralProfile(
                            user_id="",
                            dimensions={},
                            confidence_scores={},
                            is_human_probability=0.5,
                            last_updated=datetime.now().timestamp(),
                            interaction_count=0
                        )
                    )
                    
                    # Update validation scores
                    for aspect, score in validation_result.metadata["component_scores"].items():
                        if aspect not in validation_scores:
                            validation_scores[aspect] = []
                        validation_scores[aspect].append(score)
                    
                    # Check for issues
                    if response_time > scenario.expected_outcomes["max_response_time"]:
                        issues.append(f"Response time exceeded for query: {query}")
                    
                    # Update conversation history
                    context.conversation_history.append({
                        "role": "user",
                        "content": query
                    })
                    context.conversation_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                except Exception as e:
                    issues.append(f"Error during interaction: {str(e)}")
                    self.logger.error(f"Playtest error: {str(e)}", exc_info=True)
            
            # Calculate final validation scores
            final_scores = {
                aspect: sum(scores) / len(scores)
                for aspect, scores in validation_scores.items()
            }
            
            # Check validation rules
            for rule, min_score in scenario.validation_rules.items():
                if rule in final_scores and final_scores[rule] < min_score:
                    issues.append(f"Failed validation rule {rule}: {final_scores[rule]} < {min_score}")
            
            return PlaytestResult(
                scenario_name=scenario.name,
                success=len(issues) == 0,
                validation_scores=final_scores,
                issues_found=issues,
                response_times=response_times,
                total_duration=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Scenario failed: {str(e)}", exc_info=True)
            return PlaytestResult(
                scenario_name=scenario.name,
                success=False,
                validation_scores={},
                issues_found=[f"Scenario failed: {str(e)}"],
                response_times=[],
                total_duration=(datetime.now() - start_time).total_seconds(),
                timestamp=datetime.now()
            )
    
    async def run_all_scenarios(self) -> List[PlaytestResult]:
        """Run all standard playtesting scenarios."""
        scenarios = self.create_standard_scenarios()
        results = []
        
        for scenario in scenarios:
            self.logger.info(f"Running scenario: {scenario.name}")
            result = await self.run_scenario(scenario)
            results.append(result)
            self.results.append(result)
            
            # Log results
            self.logger.info(f"Scenario {scenario.name} completed:")
            self.logger.info(f"Success: {result.success}")
            self.logger.info(f"Issues found: {len(result.issues_found)}")
            self.logger.info(f"Average response time: {sum(result.response_times) / len(result.response_times):.2f}s")
            
            if not result.success:
                self.logger.warning(f"Issues in scenario {scenario.name}:")
                for issue in result.issues_found:
                    self.logger.warning(f"- {issue}")
        
        return results
    
    def generate_report(self) -> str:
        """Generate a detailed report of playtesting results."""
        if not self.results:
            return "No playtest results available."
        
        report = ["# Vortex Automated Playtest Report", ""]
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total scenarios: {len(self.results)}")
        report.append(f"Successful scenarios: {sum(1 for r in self.results if r.success)}")
        report.append("")
        
        # Overall statistics
        total_issues = sum(len(r.issues_found) for r in self.results)
        total_duration = sum(r.total_duration for r in self.results)
        avg_response_time = sum(
            sum(r.response_times) / len(r.response_times)
            for r in self.results
            if r.response_times
        ) / len(self.results)
        
        report.append("## Overall Statistics")
        report.append(f"- Total issues found: {total_issues}")
        report.append(f"- Total duration: {total_duration:.2f}s")
        report.append(f"- Average response time: {avg_response_time:.2f}s")
        report.append("")
        
        # Detailed results
        report.append("## Scenario Results")
        for result in self.results:
            report.append(f"### {result.scenario_name}")
            report.append(f"- Success: {result.success}")
            report.append(f"- Duration: {result.total_duration:.2f}s")
            report.append(f"- Average response time: {sum(result.response_times) / len(result.response_times):.2f}s")
            report.append("#### Validation Scores:")
            for aspect, score in result.validation_scores.items():
                report.append(f"- {aspect}: {score:.2f}")
            if result.issues_found:
                report.append("#### Issues:")
                for issue in result.issues_found:
                    report.append(f"- {issue}")
            report.append("")
        
        return "\n".join(report)
    
    async def cleanup(self):
        """Clean up resources."""
        # Handle both async and sync close methods
        res = self.ai_service.close()
        import asyncio as _asyncio
        if _asyncio.iscoroutine(res):
            await res 