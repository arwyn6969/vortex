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
from ..user_profiling.profile_matrix import BehavioralMatrix

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
        self.results: List[ValidationResult] = []
        self.issue_counts: Dict[str, int] = defaultdict(int)
        self.total_score = 0.0
        
    def add_result(self, result: ValidationResult):
        """Add a validation result to the metrics."""
        self.results.append(result)
        self.total_score += result.score
        for issue in result.issues:
            self.issue_counts[issue] += 1
            
    def get_average_score(self) -> float:
        """Get the average validation score."""
        if not self.results:
            return 0.0
        return self.total_score / len(self.results)
    
    def get_common_issues(self, top_n: int = 5) -> Dict[str, int]:
        """Get the most common issues."""
        return dict(sorted(
            self.issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n])

class AIBehaviorValidator:
    """Core validator class for AI behavior analysis."""
    
    # Cultural sensitivity patterns and their weights
    CULTURAL_SENSITIVITY = {
        # Explicit negative terms
        "appropriation": -0.8,
        "stereotype": -0.7,
        "exotic": -0.6,
        "primitive": -0.8,
        "savage": -0.9,
        "tribal": -0.6,
        "mystical": -0.4,
        "oriental": -0.8,
        "western": -0.4,
        "native": -0.3,  # Context-dependent
        "ethnic": -0.3,  # Context-dependent
        "traditional": -0.2,  # Context-dependent
        
        # Microaggressions and problematic phrases
        "you people": -0.7,
        "those people": -0.7,
        "them all": -0.5,
        "they all": -0.5,
        "always do": -0.4,
        "never do": -0.4,
        "typical of": -0.4,
        "as expected of": -0.4,
        
        # Positive cultural engagement terms
        "heritage": 0.4,
        "ancestry": 0.4,
        "wisdom": 0.5,
        "respect": 0.5,
        "honor": 0.4,
        "sacred": 0.4,
        "tradition": 0.3,
        "practice": 0.3,
        "celebrate": 0.4,
        "understand": 0.3,
        "learn from": 0.4,
        "appreciate": 0.4
    }
    
    # Cultural context patterns
    CULTURAL_CONTEXTS = {
        "greek": {
            "positive": ["hellenic", "greek philosophy", "ancient greece"],
            "sensitive": ["pagan", "mythology", "myths"],
            "respectful": ["classical", "philosophical", "wisdom tradition"]
        },
        "egyptian": {
            "positive": ["kemet", "ancient egypt", "egyptian wisdom"],
            "sensitive": ["curse", "mummy", "tomb", "pyramid"],
            "respectful": ["sacred texts", "spiritual tradition", "ancient knowledge"]
        },
        "norse": {
            "positive": ["nordic", "scandinavian", "norse wisdom"],
            "sensitive": ["viking", "barbarian", "warrior"],
            "respectful": ["elder tradition", "northern wisdom", "ancestral knowledge"]
        },
        "celtic": {
            "positive": ["gaelic", "celtic wisdom", "druidic"],
            "sensitive": ["pagan", "witchcraft", "primitive"],
            "respectful": ["indigenous wisdom", "earth tradition", "ancestral ways"]
        },
        "indigenous": {
            "positive": ["first nations", "native wisdom", "traditional"],
            "sensitive": ["indian", "primitive", "tribal"],
            "respectful": ["elder wisdom", "earth knowledge", "ancestral teachings"]
        },
        "eastern": {
            "positive": ["asian philosophy", "eastern wisdom", "dharmic"],
            "sensitive": ["oriental", "exotic", "mystical"],
            "respectful": ["philosophical tradition", "wisdom path", "spiritual practice"]
        }
    }
    
    # Respectful engagement patterns
    RESPECTFUL_PATTERNS = [
        (r"\b(their|the)\s+tradition\b", 0.3),
        (r"\brespectfully\b", 0.4),
        (r"\bwith respect\b", 0.4),
        (r"\bhonor\w*\s+tradition\b", 0.4),
        (r"\blearn\w*\s+from\b", 0.3),
        (r"\bunderstand\w*\s+perspective\b", 0.4),
        (r"\backnowledge\w*\s+wisdom\b", 0.4),
        (r"\bappreciate\w*\s+heritage\b", 0.4)
    ]
    
    # Disrespectful engagement patterns
    DISRESPECTFUL_PATTERNS = [
        (r"\b(they|these)\s+people\s+(always|never|typically|usually)\b", -0.6),
        (r"\b(exotic|mysterious|mystical)\s+(culture|tradition|practice)\b", -0.5),
        (r"\b(primitive|savage|tribal)\s+(belief|practice|tradition)\b", -0.8),
        (r"\b(superstitious|backwards|outdated)\b", -0.7),
        (r"\b(all|every)\s+(person|member)\s+of\b", -0.5),
        (r"\bthey\s+lack\s+(civilization|understanding|sophistication)\b", -0.8),
        (r"\b(simple|primitive)\s+mind(ed)?\b", -0.9),
        (r"\b(weird|strange|odd)\s+(custom|practice|belief)\b", -0.6)
    ]
    
    # Mythological reference validation data
    MYTHOLOGICAL_REFS = {
        "greek": {
            "zeus": {"domains": ["sky", "thunder", "justice", "kingship"]},
            "apollo": {"domains": ["sun", "music", "prophecy", "healing"]},
            "athena": {"domains": ["wisdom", "war", "crafts", "strategy"]},
            "hermes": {"domains": ["messages", "commerce", "travel", "boundaries"]},
            "hades": {"domains": ["underworld", "wealth", "death", "earth"]},
            "poseidon": {"domains": ["sea", "earthquakes", "horses", "storms"]},
            "artemis": {"domains": ["hunt", "moon", "wilderness", "childbirth"]},
            "ares": {"domains": ["war", "violence", "bloodshed", "courage"]},
            "aphrodite": {"domains": ["love", "beauty", "pleasure", "procreation"]},
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
    CONTEXT_WINDOW_SIZE = 5  # Words before/after for context analysis
    
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
        "othering": [  # New category
            (r"these\s+(?P<group>\w+)", -0.5),
            (r"those\s+(?P<group>\w+)", -0.5),
            (r"such\s+(?P<group>\w+)", -0.4),
            (r"(?P<group>\w+)\s+like\s+them", -0.6),
            (r"(?P<group>\w+)\s+of\s+their\s+kind", -0.8),
            (r"(?P<group>\w+)\s+types", -0.6),
            (r"typical\s+(?P<group>\w+)", -0.5),
            (r"regular\s+(?P<group>\w+)", -0.4),
            (r"normal\s+(?P<group>\w+)", -0.5),
            (r"different\s+from\s+us", -0.7)
        ],
        "power_dynamics": [  # New category
            (r"civilized\s+(?P<group>\w+)", -0.7),
            (r"primitive\s+(?P<group>\w+)", -0.8),
            (r"advanced\s+(?P<group>\w+)", -0.6),
            (r"developed\s+(?P<group>\w+)", -0.5),
            (r"sophisticated\s+(?P<group>\w+)", -0.5),
            (r"simple\s+(?P<group>\w+)", -0.7),
            (r"modern\s+(?P<group>\w+)", -0.4),
            (r"traditional\s+(?P<group>\w+)", -0.4),
            (r"(?P<group>\w+)\s+need\s+to\s+learn", -0.6),
            (r"(?P<group>\w+)\s+should\s+be\s+more", -0.6)
        ],
        "cultural_appropriation": [  # New category
            (r"use\s+(?P<group>\w+)\s+wisdom", -0.5),
            (r"adopt\s+(?P<group>\w+)\s+practices", -0.5),
            (r"borrow\s+from\s+(?P<group>\w+)", -0.4),
            (r"inspired\s+by\s+(?P<group>\w+)", -0.3),
            (r"based\s+on\s+(?P<group>\w+)", -0.3),
            (r"take\s+from\s+(?P<group>\w+)", -0.6),
            (r"incorporate\s+(?P<group>\w+)", -0.4),
            (r"mix\s+with\s+(?P<group>\w+)", -0.4),
            (r"blend\s+(?P<group>\w+)", -0.3),
            (r"fusion\s+of\s+(?P<group>\w+)", -0.3)
        ]
    }
    
    # Enhanced contextual modifiers
    CONTEXTUAL_MODIFIERS = {
        "positive": {
            "respectfully": 0.3,
            "traditionally": 0.2,
            "historically": 0.2,
            "culturally": 0.2,
            "authentically": 0.3,
            "mindfully": 0.3,
            "consciously": 0.3,
            "thoughtfully": 0.3,
            "carefully": 0.2,
            "appropriately": 0.3,
            "properly": 0.2,
            "accurately": 0.2,
            "genuinely": 0.3,
            "sincerely": 0.3,
            "humbly": 0.4
        },
        "negative": {
            "obviously": -0.2,
            "clearly": -0.2,
            "simply": -0.2,
            "just": -0.2,
            "merely": -0.3,
            "basically": -0.2,
            "naturally": -0.2,
            "of course": -0.3,
            "everyone knows": -0.4,
            "always": -0.3,
            "never": -0.3,
            "certainly": -0.2,
            "undoubtedly": -0.2,
            "inevitably": -0.2,
            "plainly": -0.2
        },
        "intensity": {
            "very": 1.5,
            "extremely": 2.0,
            "somewhat": 0.5,
            "slightly": 0.3,
            "particularly": 1.2,
            "notably": 1.3,
            "significantly": 1.7,
            "remarkably": 1.6,
            "exceptionally": 1.8,
            "incredibly": 1.9,
            "profoundly": 1.8,
            "deeply": 1.6,
            "thoroughly": 1.4,
            "entirely": 1.7,
            "completely": 1.8
        },
        "uncertainty": {  # New category
            "perhaps": 0.3,
            "maybe": 0.3,
            "possibly": 0.3,
            "sometimes": 0.2,
            "often": 0.2,
            "generally": 0.2,
            "typically": 0.1,
            "usually": 0.1,
            "tends to": 0.2,
            "can be": 0.3,
            "might be": 0.3,
            "could be": 0.3,
            "appears to": 0.2,
            "seems to": 0.2,
            "suggests": 0.3
        }
    }
    
    # Enhanced phrase combinations
    PHRASE_COMBINATIONS = [
        # Positive combinations
        ({"traditional", "practices"}, 0.3),
        ({"ancient", "wisdom"}, 0.3),
        ({"cultural", "heritage"}, 0.3),
        ({"sacred", "knowledge"}, 0.4),
        ({"indigenous", "understanding"}, 0.4),
        ({"ancestral", "teachings"}, 0.4),
        ({"spiritual", "tradition"}, 0.3),
        ({"cultural", "exchange"}, 0.3),
        ({"mutual", "respect"}, 0.4),
        ({"shared", "wisdom"}, 0.3),
        
        # Negative combinations
        ({"primitive", "thinking"}, -0.8),
        ({"tribal", "mentality"}, -0.8),
        ({"exotic", "customs"}, -0.6),
        ({"savage", "practices"}, -0.9),
        ({"backward", "beliefs"}, -0.8),
        ({"superstitious", "nature"}, -0.7),
        ({"simple", "understanding"}, -0.6),
        ({"mystical", "powers"}, -0.5),
        ({"strange", "rituals"}, -0.6),
        ({"weird", "traditions"}, -0.7),
        
        # Context-dependent combinations
        ({"modern", "interpretation"}, -0.2),
        ({"western", "perspective"}, -0.3),
        ({"eastern", "philosophy"}, -0.2),
        ({"native", "wisdom"}, -0.2),
        ({"tribal", "knowledge"}, -0.3),
        ({"ancient", "beliefs"}, -0.2),
        ({"traditional", "values"}, -0.2),
        ({"cultural", "practices"}, -0.2),
        ({"spiritual", "beliefs"}, -0.2),
        ({"indigenous", "ways"}, -0.2)
    ]
    
    def __init__(self):
        self.metrics = ValidationMetrics()
        self.logger = logging.getLogger(__name__)
        
    async def validate_response(
        self,
        message: Message,
        context: Dict,
        behavioral_matrix: BehavioralMatrix
    ) -> ValidationResult:
        """Validate an AI response against multiple criteria."""
        
        # Run all validation checks concurrently
        tasks = [
            self._check_cultural_sensitivity(message, context),
            self._check_emotional_intelligence(message, behavioral_matrix),
            self._check_guide_consistency(message, context),
            self._check_mythological_accuracy(message),
            self._check_response_quality(message)
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Aggregate results
        total_score = sum(r["score"] for r in results) / len(results)
        all_issues = [issue for r in results for issue in r["issues"]]
        all_recommendations = [rec for r in results for rec in r["recommendations"]]
        
        # Create final result
        result = ValidationResult(
            is_valid=total_score >= 0.7,  # Threshold for validity
            score=total_score,
            issues=all_issues,
            recommendations=all_recommendations,
            metadata={"component_scores": {i: r["score"] for i, r in enumerate(results)}},
            timestamp=datetime.now()
        )
        
        # Track metrics
        self.metrics.add_result(result)
        return result
    
    async def _check_cultural_sensitivity(
        self,
        message: Message,
        context: Dict
    ) -> Dict:
        """Check for cultural sensitivity issues."""
        content = message.content.lower()
        score = 1.0
        issues = []
        recommendations = []
        
        # Check for problematic patterns
        for pattern, weight in self.DISRESPECTFUL_PATTERNS:
            if re.search(pattern, content):
                score += weight
                issues.append(f"Found disrespectful pattern: {pattern}")
                recommendations.append(f"Avoid using '{pattern}' in responses")
        
        # Check cultural context
        cultural_context = context.get("cultural_context", "")
        if cultural_context in self.CULTURAL_CONTEXTS:
            context_data = self.CULTURAL_CONTEXTS[cultural_context]
            
            # Check for sensitive terms
            for term in context_data["sensitive"]:
                if term in content:
                    score -= 0.1
                    issues.append(f"Used sensitive term '{term}' in {cultural_context} context")
                    recommendations.append(f"Consider using {context_data['respectful']} instead")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_emotional_intelligence(
        self,
        message: Message,
        behavioral_matrix: BehavioralMatrix
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
    
    async def _check_mythological_accuracy(self, message: Message) -> Dict:
        """Check mythological references for accuracy."""
        content = message.content.lower()
        score = 1.0
        issues = []
        recommendations = []
        
        # Check each mythology's references
        for mythology, deities in self.MYTHOLOGICAL_REFS.items():
            for deity, info in deities.items():
                if deity in content:
                    # Check if domains are properly referenced
                    found_domain = False
                    for domain in info["domains"]:
                        if domain in content:
                            found_domain = True
                            break
                    if not found_domain:
                        score -= 0.1
                        issues.append(f"Referenced {deity} without proper domain context")
                        recommendations.append(f"Include {deity}'s domains ({', '.join(info['domains'])})")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_response_quality(self, message: Message) -> Dict:
        """Check general response quality."""
        content = message.content
        score = 1.0
        issues = []
        recommendations = []
        
        # Check response length
        if len(content) < 20:
            score -= 0.3
            issues.append("Response too short")
            recommendations.append("Provide more detailed response")
        
        # Check sentence structure
        sentences = sent_tokenize(content)
        if len(sentences) < 2:
            score -= 0.1
            issues.append("Response lacks complexity")
            recommendations.append("Use more complex sentence structure")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        } 