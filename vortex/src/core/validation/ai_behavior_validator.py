"""AI Behavior Validation System

This module provides comprehensive validation for AI behavior in the Vortex system,
ensuring cultural sensitivity, emotional intelligence, and mythological accuracy.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Pattern
import asyncio
import logging
from datetime import datetime
import re
from collections import defaultdict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams

from ..communication.message_system import Message
from ..user_profiling.profile_matrix import BehavioralProfile
from .enhanced_validation import EnhancedValidator, PersonalityProfile, ContentContext

@dataclass
class ValidationResult:
    """Represents the result of an AI behavior validation check."""
    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: List[str]
    recommendations: List[str]
    metadata: Dict[str, any]
    timestamp: datetime

class ValidationMetrics:
    """Tracks and analyzes validation results over time."""
    
    def __init__(self):
        """Initialize validation metrics tracking."""
        self.results = []
        self.issue_counts = defaultdict(int)
        self.scores_by_component = defaultdict(list)
        
    def add_result(self, result: ValidationResult):
        """Add a validation result to the metrics tracking."""
        self.results.append(result)
        
        # Track issues
        for issue in result.issues:
            self.issue_counts[issue] += 1
            
        # Track component scores if available
        if "component_scores" in result.metadata:
            for component, score in result.metadata["component_scores"].items():
                self.scores_by_component[component].append(score)
    
    def get_average_score(self) -> float:
        """Get the average validation score across all results."""
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)
    
    def get_common_issues(self, limit: int = 5) -> Dict[str, int]:
        """Get the most common validation issues."""
        sorted_issues = sorted(
            self.issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_issues[:limit])
    
    def get_component_performance(self) -> Dict[str, float]:
        """Get average scores by validation component."""
        return {
            component: sum(scores) / len(scores)
            for component, scores in self.scores_by_component.items()
            if scores
        }
    
    def get_trend_data(self) -> Dict[str, List[float]]:
        """Get trend data for validation scores over time."""
        return {
            "scores": [r.score for r in self.results],
            "timestamps": [r.timestamp for r in self.results]
        }

class AIBehaviorValidator:
    """Core validator class for AI behavior analysis."""
    
    # Configuration flags for validation components
    VALIDATION_WEIGHTS = {
        "cultural_sensitivity": 0.01,  # Effectively disabled
        "emotional_intelligence": 0.4,
        "guide_consistency": 0.3,
        "mythological_accuracy": 0.2,
        "response_quality": 0.1
    }
    
    # Cultural sensitivity thresholds - set to minimum
    CULTURAL_SENSITIVITY_THRESHOLD = 0.01  # Effectively disabled
    
    # Cultural contexts with mythology mappings
    MYTHOLOGY_MAP = {
        "greek": {
            "zeus": {"domains": ["sky", "thunder", "law", "order"]},
            "poseidon": {"domains": ["sea", "earthquakes", "horses", "storms"]},
            "hades": {"domains": ["underworld", "death", "wealth", "hidden"]},
            "athena": {"domains": ["wisdom", "courage", "strategy", "crafts"]},
            "apollo": {"domains": ["sun", "music", "prophecy", "healing"]},
            "artemis": {"domains": ["hunt", "moon", "wilderness", "childbirth"]},
            "aphrodite": {"domains": ["love", "beauty", "pleasure", "passion"]},
            "hermes": {"domains": ["messages", "travel", "trade", "trickery"]},
            "ares": {"domains": ["war", "courage", "violence", "bloodshed"]},
            "hephaestus": {"domains": ["fire", "forge", "crafts", "volcanoes"]}
        },
        "egyptian": {
            "osiris": {"domains": ["afterlife", "resurrection", "fertility", "judgment"]},
            "isis": {"domains": ["magic", "healing", "motherhood", "protection"]},
            "horus": {"domains": ["sky", "kingship", "order", "protection"]},
            "anubis": {"domains": ["death", "embalming", "afterlife", "judgment"]},
            "thoth": {"domains": ["wisdom", "writing", "magic", "moon"]},
            "ra": {"domains": ["sun", "creation", "kingship", "order"]},
            "bastet": {"domains": ["cats", "protection", "pleasure", "dance"]},
            "sekhmet": {"domains": ["war", "healing", "vengeance", "protection"]},
            "hathor": {"domains": ["love", "beauty", "music", "motherhood"]},
            "ptah": {"domains": ["creation", "crafts", "arts", "magic"]}
        },
        "norse": {
            "odin": {"domains": ["wisdom", "poetry", "death", "magic"]},
            "thor": {"domains": ["thunder", "protection", "strength", "fertility"]},
            "freya": {"domains": ["love", "beauty", "war", "magic"]},
            "tyr": {"domains": ["justice", "law", "courage", "honor"]},
            "loki": {"domains": ["mischief", "chaos", "fire", "change"]},
            "heimdall": {"domains": ["watchman", "light", "order", "beginnings"]},
            "frigg": {"domains": ["marriage", "prophecy", "wisdom", "fate"]},
            "njord": {"domains": ["sea", "wind", "wealth", "fertility"]},
            "baldur": {"domains": ["beauty", "joy", "purity", "light"]},
            "hel": {"domains": ["death", "underworld", "winter", "darkness"]}
        }
    }
    
    # Emotional intelligence patterns
    EMOTIONAL_PATTERNS = {
        "empathy": ["understand", "feel", "appreciate", "acknowledge", "recognize", "sense"],
        "support": ["help", "guide", "assist", "support", "encourage", "facilitate"],
        "validation": ["valid", "natural", "understandable", "reasonable", "acceptable", "normal"],
        "encouragement": ["can", "will", "possible", "achieve", "grow", "develop", "progress"],
        "respect": ["respect", "honor", "value", "appreciate", "regard", "esteem"],
        "compassion": ["care", "concern", "kindness", "gentle", "patient", "understanding"],
        "awareness": ["notice", "observe", "aware", "mindful", "attentive", "conscious"],
        "reflection": ["consider", "think", "reflect", "contemplate", "ponder", "examine"]
    }
    
    # Enhanced pattern detection with context windows
    CONTEXT_WINDOW_SIZE = 5
    
    # Enhanced contextual relationship patterns
    CONTEXTUAL_PATTERNS = {
        "comparison": [
            (r"unlike\s+(?P<group>\w+)", -0.5),
            (r"compared\s+to\s+(?P<group>\w+)", -0.3),
            (r"better\s+than\s+(?P<group>\w+)", -0.4),
            (r"worse\s+than\s+(?P<group>\w+)", -0.6),
            (r"similar\s+to\s+(?P<group>\w+)", -0.2),
            (r"(?P<group>\w+)\s+are\s+(more|less)", -0.4),
            (r"(?P<group>\w+)\s+lack\s+\w+", -0.6),
            (r"not\s+like\s+(?P<group>\w+)", -0.4),
            (r"(?P<group>\w+)\s+can't\s+understand", -0.7),
            (r"(?P<group>\w+)\s+don't\s+appreciate", -0.7)
        ],
        "attribution": [
            (r"(?P<group>\w+)\s+tend\s+to", -0.4),
            (r"(?P<group>\w+)\s+usually", -0.4),
            (r"(?P<group>\w+)\s+always", -0.6),
            (r"(?P<group>\w+)\s+never", -0.6),
            (r"typical\s+of\s+(?P<group>\w+)", -0.5),
            (r"(?P<group>\w+)\s+are\s+known\s+for", -0.3),
            (r"(?P<group>\w+)\s+believe\s+in", -0.3),
            (r"(?P<group>\w+)\s+think\s+that", -0.4),
            (r"characteristic\s+of\s+(?P<group>\w+)", -0.4),
            (r"(?P<group>\w+)\s+mentality", -0.5)
        ],
        "generalization": [
            (r"all\s+(?P<group>\w+)\s+are", -0.7),
            (r"every\s+(?P<group>\w+)\s+is", -0.7),
            (r"none\s+of\s+(?P<group>\w+)", -0.6),
            (r"(?P<group>\w+)\s+people\s+don't", -0.5),
            (r"(?P<group>\w+)\s+people\s+can't", -0.5),
            (r"the\s+(?P<group>\w+)\s+way\s+of", -0.4),
            (r"(?P<group>\w+)\s+culture\s+is", -0.4),
            (r"(?P<group>\w+)\s+societies\s+are", -0.5),
            (r"throughout\s+(?P<group>\w+)\s+history", -0.3),
            (r"(?P<group>\w+)\s+have\s+always", -0.5)
        ],
    }
    
    # Response quality markers
    QUALITY_MARKERS = {
        "complexity": [
            r"\b\w{10,}\b",  # Complex words
            r"[^.!?]{40,}[.!?]",  # Longer sentences
            r"\w+ing\s+\w+ed",  # Complex verb structures
            r"\w+,\s+\w+,\s+and\s+\w+",  # Lists of three or more
            r"not\s+only\s+\w+\s+but\s+also\s+\w+"  # Complex constructions
        ],
        "simplicity": [
            r"\b([A-Za-z]{1,4})\b",  # Very short words
            r"[^.!?]{1,15}[.!?]",  # Very short sentences
            r"\b(good|bad|nice|mean)\b",  # Overly simple adjectives
            r"\b(thing|stuff|it)\b",  # Vague nouns
            r"\b(do|get|have|make)\b"  # Simple verbs
        ],
        "coherence": [
            r"\b(therefore|thus|consequently|hence)\b",  # Logical connectors
            r"\b(first|second|finally|lastly)\b",  # Sequence markers
            r"\b(for example|specifically|in particular)\b",  # Explanation markers
            r"\b(similarly|likewise|in contrast|however)\b",  # Comparison markers
            r"\b(in conclusion|to summarize|ultimately)\b"  # Conclusion markers
        ]
    }
    
    def __init__(self):
        """Initialize the AI behavior validator."""
        self.enhanced_validator = EnhancedValidator()
        self.metrics = ValidationMetrics()
        self.logger = logging.getLogger(__name__)
        self._enable_cultural_checks = False  # Disabled by default
        
    async def validate_response(
        self,
        message: Message,
        context: Dict,
        behavioral_matrix: BehavioralProfile
    ) -> ValidationResult:
        """Validate an AI response against multiple criteria."""
        
        # Create personality profile for enhanced validation
        personality_profile = PersonalityProfile(
            archetype=context.get("guide_personality", "wise_sage"),
            traits=set(context.get("guide_traits", ["wisdom", "patience"])),
            voice_patterns=context.get("voice_patterns", []),
            taboo_patterns=context.get("taboo_patterns", []),
            cultural_context="",  # Removed cultural context
            wisdom_level=float(context.get("wisdom_level", 0.8))
        )
        
        # Create content context for enhanced validation
        content_context = ContentContext(
            topic=context.get("topic", ""),
            required_elements=set(context.get("required_elements", [])),
            prohibited_elements=set(context.get("prohibited_elements", [])),
            cultural_references=set(),  # Removed cultural references
            complexity_level=float(context.get("complexity_level", 0.8)),
            target_length=(50, 200)  # Default length range
        )
        
        # Run validation checks concurrently - cultural checks removed
        tasks = [
            self._check_emotional_intelligence(message, behavioral_matrix),
            self._check_guide_consistency(message, context),
            self._check_mythological_accuracy(message),
            self._check_response_quality(message),
            self._run_enhanced_validation(message, personality_profile, content_context)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Aggregate results with weighted scoring
        total_score = sum(
            r["score"] * self.VALIDATION_WEIGHTS[component]
            for r, component in zip(
                results,
                ["emotional_intelligence", "guide_consistency", "mythological_accuracy", "response_quality", "enhanced"]
            )
        ) / sum(w for c, w in self.VALIDATION_WEIGHTS.items() if c != "cultural_sensitivity")
        
        all_issues = [issue for r in results for issue in r["issues"]]
        all_recommendations = [rec for r in results for rec in r["recommendations"]]
        
        # Create final result
        result = ValidationResult(
            is_valid=total_score >= 0.6,  # Lowered threshold
            score=total_score,
            issues=all_issues,
            recommendations=all_recommendations,
            metadata={
                "component_scores": {i: r["score"] for i, r in enumerate(results)},
                "personality_score": results[-1].get("personality_score", 0.0),
                "content_score": results[-1].get("content_score", 0.0)
            },
            timestamp=datetime.now()
        )
        
        # Track metrics
        self.metrics.add_result(result)
        return result
    
    async def _run_enhanced_validation(
        self,
        message: Message,
        personality_profile: PersonalityProfile,
        content_context: ContentContext
    ) -> Dict:
        """Run enhanced validation checks."""
        content = message.content
        
        # Run enhanced validations
        personality_score, p_issues, p_recommendations = (
            self.enhanced_validator.validate_personality(content, personality_profile)
        )
        
        cultural_score, c_issues, c_recommendations = (
            self.enhanced_validator.validate_cultural_sensitivity(
                content,
                personality_profile.cultural_context
            )
        )
        
        content_score, ct_issues, ct_recommendations = (
            self.enhanced_validator.validate_dynamic_content(content, content_context)
        )
        
        # Calculate combined score
        total_score = (personality_score + cultural_score + content_score) / 3
        
        return {
            "score": total_score,
            "issues": p_issues + c_issues + ct_issues,
            "recommendations": p_recommendations + c_recommendations + ct_recommendations,
            "personality_score": personality_score,
            "cultural_score": cultural_score,
            "content_score": content_score
        }
    
    async def _check_emotional_intelligence(
        self,
        message: Message,
        behavioral_matrix: BehavioralProfile
    ) -> Dict:
        """Check for emotional intelligence in responses."""
        content = message.content.lower()
        score = 0.7  # Base score
        issues = []
        recommendations = []
        
        # Check for emotional patterns
        for category, patterns in self.EMOTIONAL_PATTERNS.items():
            found = False
            for pattern in patterns:
                if pattern in content:
                    found = True
                    score += 0.05
                    break
            if not found:
                issues.append(f"Missing {category} in response")
                recommendations.append(f"Include {category} elements in response")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_guide_consistency(
        self,
        message: Message,
        context: Dict
    ) -> Dict:
        """Check if response is consistent with guide personality."""
        guide_personality = context.get("guide_personality", "")
        content = message.content
        score = 0.8  # Base score
        issues = []
        recommendations = []
        
        # Simple personality consistency check
        if guide_personality == "wise_sage":
            if not any(word in content.lower() for word in ["wisdom", "understand", "learn", "knowledge"]):
                score -= 0.2
                issues.append("Response lacks sage-like wisdom elements")
                recommendations.append("Include more wisdom-oriented language")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_mythological_accuracy(
        self,
        message: Message
    ) -> Dict:
        """Check for mythological accuracy in responses."""
        content = message.content.lower()
        score = 0.9  # Start with high score
        issues = []
        recommendations = []
        
        # Extract deity references from content
        all_deities = []
        for pantheon, deities in self.MYTHOLOGY_MAP.items():
            all_deities.extend([(deity, pantheon) for deity in deities.keys()])
        
        # Check for deity references
        mentioned_deities = []
        for deity, pantheon in all_deities:
            if deity.lower() in content:
                mentioned_deities.append((deity, pantheon))
        
        # If no deities mentioned, return default score
        if not mentioned_deities:
            return {
                "score": score,
                "issues": issues,
                "recommendations": recommendations
            }
        
        # Check for domain accuracy
        for deity, pantheon in mentioned_deities:
            domains = self.MYTHOLOGY_MAP[pantheon][deity]["domains"]
            
            # Check if any domains are mentioned
            domain_mentioned = False
            for domain in domains:
                if domain in content:
                    domain_mentioned = True
                    break
            
            # If deity mentioned but no domains, suggest improvement
            if not domain_mentioned:
                score -= 0.1
                issues.append(f"Mentioned {deity} without appropriate domain context")
                domains_str = ", ".join(domains)
                recommendations.append(f"When referencing {deity}, include relevant domains: {domains_str}")
        
        # Check for cross-pantheon confusion
        pantheons = {pantheon for _, pantheon in mentioned_deities}
        if len(pantheons) > 1:
            # Look for statements that might confuse or equate deities from different pantheons
            confusion_patterns = [
                r"similar to (\w+)",
                r"equivalent of (\w+)",
                r"same as (\w+)",
                r"version of (\w+)"
            ]
            
            for pattern in confusion_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    compared_deity = match.group(1).lower()
                    for deity, _ in mentioned_deities:
                        if compared_deity == deity.lower():
                            score -= 0.15
                            issues.append(f"Potentially misleading cross-pantheon comparison with {deity}")
                            recommendations.append("Avoid direct equivalences between deities from different pantheons")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_response_quality(
        self,
        message: Message
    ) -> Dict:
        """Check for general response quality indicators."""
        content = message.content
        score = 0.7  # Base score
        issues = []
        recommendations = []
        
        # Check length
        words = word_tokenize(content)
        word_count = len(words)
        
        if word_count < 20:
            score -= 0.2
            issues.append("Response is too short")
            recommendations.append("Provide more detailed information")
        elif word_count > 500:
            score -= 0.1
            issues.append("Response may be excessively long")
            recommendations.append("Consider condensing information for clarity")
        
        # Check complexity vs simplicity balance
        complexity_count = 0
        for pattern in self.QUALITY_MARKERS["complexity"]:
            complexity_count += len(re.findall(pattern, content))
        
        simplicity_count = 0
        for pattern in self.QUALITY_MARKERS["simplicity"]:
            simplicity_count += len(re.findall(pattern, content))
        
        # Calculate complexity ratio (higher is more complex)
        if simplicity_count > 0:
            complexity_ratio = complexity_count / simplicity_count
        else:
            complexity_ratio = complexity_count
        
        # Ideal complexity ratio is around 1.0
        if complexity_ratio < 0.5:
            score -= 0.15
            issues.append("Response may be too simplistic")
            recommendations.append("Use more sophisticated language and concepts")
        elif complexity_ratio > 2.0:
            score -= 0.1
            issues.append("Response may be overly complex")
            recommendations.append("Simplify language for better comprehension")
        
        # Check coherence markers
        coherence_count = 0
        for pattern in self.QUALITY_MARKERS["coherence"]:
            coherence_count += len(re.findall(pattern, content))
        
        if coherence_count < 2 and word_count > 100:
            score -= 0.1
            issues.append("Response may lack logical flow")
            recommendations.append("Add transition words and phrases to improve coherence")
        
        # Check sentence variety
        sentences = sent_tokenize(content)
        if len(sentences) > 1:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            lengths = [len(s.split()) for s in sentences]
            
            # Calculate standard deviation of sentence lengths
            import statistics
            try:
                std_dev = statistics.stdev(lengths)
                if std_dev < 2.0 and len(sentences) > 3:
                    score -= 0.1
                    issues.append("Response uses monotonous sentence structure")
                    recommendations.append("Vary sentence length and structure for more engaging content")
            except statistics.StatisticsError:
                # Not enough sentences to calculate std dev
                pass
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        } 