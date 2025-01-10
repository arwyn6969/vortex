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
from ..profile.behavioral_matrix import BehavioralMatrix

@dataclass
class ValidationResult:
    """Represents the result of an AI behavior validation check."""
    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: List[str]
    recommendations: List[str]
    metadata: Dict[str, any]
    timestamp: datetime

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
        self.logger = logging.getLogger(__name__)
        self._cultural_keywords = set(self.CULTURAL_SENSITIVITY.keys())
        self._mythological_references = self.MYTHOLOGICAL_REFS
        self._emotional_patterns = {
            pattern: re.compile(rf'\b({"|".join(words)})\b', re.IGNORECASE)
            for pattern, words in self.EMOTIONAL_PATTERNS.items()
        }
        self._respectful_patterns = [
            (re.compile(pattern, re.IGNORECASE), weight)
            for pattern, weight in self.RESPECTFUL_PATTERNS
        ]
        self._disrespectful_patterns = [
            (re.compile(pattern, re.IGNORECASE), weight)
            for pattern, weight in self.DISRESPECTFUL_PATTERNS
        ]
        
        # Initialize enhanced pattern detection
        self._compile_contextual_patterns()
        self._initialize_nltk()
    
    def _compile_contextual_patterns(self):
        """Compile all contextual patterns for efficient matching."""
        self._compiled_patterns = {
            category: [(re.compile(pattern, re.IGNORECASE), weight)
                      for pattern, weight in patterns]
            for category, patterns in self.CONTEXTUAL_PATTERNS.items()
        }
    
    def _initialize_nltk(self):
        """Initialize NLTK components."""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    async def validate_response(
        self,
        message: Message,
        context: Dict[str, any],
        behavioral_matrix: BehavioralMatrix
    ) -> ValidationResult:
        """Validate an AI response against multiple criteria."""
        issues = []
        recommendations = []
        scores = []
        
        # Run all validation checks concurrently
        validation_tasks = [
            self._check_cultural_sensitivity(message, context),
            self._check_emotional_intelligence(message, behavioral_matrix),
            self._check_guide_consistency(message, context),
            self._check_mythological_accuracy(message),
            self._check_response_quality(message)
        ]
        
        results = await asyncio.gather(*validation_tasks)
        
        for result in results:
            scores.append(result["score"])
            issues.extend(result["issues"])
            recommendations.extend(result["recommendations"])
        
        return ValidationResult(
            is_valid=all(score >= 0.7 for score in scores),
            score=sum(scores) / len(scores),
            issues=issues,
            recommendations=recommendations,
            metadata={"individual_scores": scores},
            timestamp=datetime.now()
        )
    
    async def _check_cultural_sensitivity(
        self,
        message: Message,
        context: Dict[str, any]
    ) -> Dict:
        """Enhanced cultural sensitivity validation with sophisticated context analysis."""
        content = message.content.lower()
        cultural_context = context.get("cultural_context", "").lower()
        
        score = 1.0
        issues = []
        recommendations = []
        
        # Tokenize content for sophisticated analysis
        sentences = sent_tokenize(content)
        words = word_tokenize(content)
        
        # Generate n-grams for phrase analysis
        bigrams = list(ngrams(words, 2))
        trigrams = list(ngrams(words, 3))
        
        # Context window analysis
        for i, word in enumerate(words):
            if word in self._cultural_keywords:
                # Get context window
                start = max(0, i - self.CONTEXT_WINDOW_SIZE)
                end = min(len(words), i + self.CONTEXT_WINDOW_SIZE + 1)
                context_window = words[start:end]
                
                # Analyze modifiers in context
                score_modifier = self._analyze_context_modifiers(context_window)
                score *= score_modifier
                
                if score_modifier < 1.0:
                    context_str = " ".join(context_window)
                    issues.append(f"Potentially problematic context around '{word}': '{context_str}'")
                    recommendations.append(
                        f"Consider rephrasing the context around '{word}' to be more culturally sensitive"
                    )
        
        # Check for problematic phrase combinations
        for words_set, weight in self.PHRASE_COMBINATIONS:
            if all(word in content for word in words_set):
                score += weight
                if weight < 0:
                    issues.append(f"Problematic phrase combination: {', '.join(words_set)}")
                    recommendations.append(
                        f"Avoid combining these terms: {', '.join(words_set)}"
                    )
        
        # Enhanced pattern matching with contextual understanding
        for category, patterns in self._compiled_patterns.items():
            for pattern, weight in patterns:
                matches = pattern.finditer(content)
                for match in matches:
                    score += weight
                    group = match.group('group') if 'group' in match.groupdict() else match.group(0)
                    
                    if weight < 0:
                        issues.append(f"Problematic {category} pattern: '{group}'")
                        recommendations.append(
                            self._get_contextual_recommendation(category, group)
                        )
        
        # Analyze sentence-level patterns
        for sentence in sentences:
            # Check for complex cultural statements
            if self._contains_cultural_comparison(sentence):
                score -= 0.2
                issues.append("Complex cultural comparison detected")
                recommendations.append(
                    "Avoid making direct comparisons between cultural practices"
                )
            
            # Check for overgeneralization
            if self._contains_overgeneralization(sentence):
                score -= 0.3
                issues.append("Cultural overgeneralization detected")
                recommendations.append(
                    "Be more specific and avoid broad generalizations about cultural groups"
                )
        
        # Final contextual adjustments
        if cultural_context:
            score = self._apply_cultural_context_rules(
                score, cultural_context, content, issues, recommendations
            )
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    def _analyze_context_modifiers(self, context_window: List[str]) -> float:
        """Analyze modifiers in the context window and return score modifier."""
        modifier = 1.0
        
        for word in context_window:
            word = word.lower()
            if word in self.CONTEXTUAL_MODIFIERS["positive"]:
                modifier += self.CONTEXTUAL_MODIFIERS["positive"][word]
            elif word in self.CONTEXTUAL_MODIFIERS["negative"]:
                modifier += self.CONTEXTUAL_MODIFIERS["negative"][word]
            
            # Apply intensity modifiers
            if word in self.CONTEXTUAL_MODIFIERS["intensity"]:
                modifier *= self.CONTEXTUAL_MODIFIERS["intensity"][word]
        
        return modifier
    
    def _contains_cultural_comparison(self, sentence: str) -> bool:
        """Check for complex cultural comparisons."""
        comparison_markers = [
            "more", "less", "better", "worse", "unlike", "different from",
            "superior", "inferior", "advanced", "primitive"
        ]
        return any(marker in sentence.lower() for marker in comparison_markers)
    
    def _contains_overgeneralization(self, sentence: str) -> bool:
        """Check for cultural overgeneralizations."""
        generalization_markers = [
            "always", "never", "all", "every", "none", "everyone", "nobody",
            "everywhere", "nowhere"
        ]
        return any(marker in sentence.lower() for marker in generalization_markers)
    
    def _get_contextual_recommendation(self, category: str, group: str) -> str:
        """Generate context-aware recommendations."""
        recommendations = {
            "comparison": f"Instead of comparing {group}, focus on describing specific practices or beliefs",
            "attribution": f"Rather than attributing behaviors to {group}, describe specific instances or individuals",
            "generalization": f"Avoid generalizing about {group}; focus on specific aspects or examples"
        }
        return recommendations.get(category, "Consider rephrasing to be more specific and respectful")
    
    def _apply_cultural_context_rules(
        self,
        score: float,
        cultural_context: str,
        content: str,
        issues: List[str],
        recommendations: List[str]
    ) -> float:
        """Apply sophisticated cultural context-specific rules."""
        context_parts = cultural_context.split("_")
        
        for part in context_parts:
            if part in self.CULTURAL_CONTEXTS:
                context_data = self.CULTURAL_CONTEXTS[part]
                
                # Analyze term relationships
                positive_terms = set(context_data["positive"])
                sensitive_terms = set(context_data["sensitive"])
                respectful_terms = set(context_data["respectful"])
                
                # Check for term co-occurrence
                words = set(word_tokenize(content.lower()))
                positive_count = len(words & positive_terms)
                sensitive_count = len(words & sensitive_terms)
                respectful_count = len(words & respectful_terms)
                
                # Apply sophisticated scoring
                if sensitive_count > 0 and positive_count == 0:
                    score *= 0.8  # Severe penalty for sensitive terms without positive context
                    recommendations.append(
                        f"Balance sensitive terms with positive cultural references: {', '.join(context_data['positive'])}"
                    )
                
                if respectful_count > 0:
                    score = min(1.0, score + (0.1 * respectful_count))
                
                # Check for term proximity
                if sensitive_count > 0 and respectful_count > 0:
                    if self._terms_are_properly_contextualized(content, sensitive_terms, respectful_terms):
                        score *= 1.1  # Bonus for proper contextualization
                    else:
                        score *= 0.9
                        recommendations.append(
                            "Ensure sensitive terms are properly contextualized with respectful language"
                        )
        
        return score
    
    def _terms_are_properly_contextualized(
        self,
        content: str,
        sensitive_terms: Set[str],
        respectful_terms: Set[str]
    ) -> bool:
        """Check if sensitive terms are properly contextualized with respectful language."""
        sentences = sent_tokenize(content.lower())
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            has_sensitive = any(term in words for term in sensitive_terms)
            has_respectful = any(term in words for term in respectful_terms)
            
            if has_sensitive and not has_respectful:
                return False
        
        return True
    
    async def _check_emotional_intelligence(
        self,
        message: Message,
        behavioral_matrix: BehavioralMatrix
    ) -> Dict:
        """Validate emotional intelligence of the response."""
        content = message.content.lower()
        score = 0.7  # Base score
        issues = []
        recommendations = []
        
        # Check for emotional intelligence patterns
        pattern_matches = defaultdict(int)
        for pattern, regex in self._emotional_patterns.items():
            matches = len(regex.findall(content))
            pattern_matches[pattern] = matches
            
            if matches == 0:
                score -= 0.1
                issues.append(f"Lacks {pattern} in response")
                recommendations.append(f"Include more {pattern} in the response")
            else:
                score = min(1.0, score + (0.05 * matches))
        
        # Check emotional balance
        total_matches = sum(pattern_matches.values())
        if total_matches > 0:
            balance = max(pattern_matches.values()) / total_matches
            if balance > 0.5:  # One pattern dominates
                score *= 0.9
                issues.append("Response shows emotional imbalance")
                recommendations.append("Balance different aspects of emotional intelligence")
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_guide_consistency(
        self,
        message: Message,
        context: Dict[str, any]
    ) -> Dict:
        """Validate consistency with guide personality."""
        content = message.content.lower()
        guide_personality = context.get("guide_personality", "").lower()
        
        personality_traits = {
            "wise_sage": {
                "positive": ["wisdom", "knowledge", "understand", "teach", "guide"],
                "negative": ["hasty", "impulsive", "uncertain", "guess"]
            },
            "warrior_mentor": {
                "positive": ["strength", "courage", "discipline", "honor", "challenge"],
                "negative": ["weak", "fear", "doubt", "hesitate"]
            },
            "mystic_guide": {
                "positive": ["mystery", "energy", "spirit", "vision", "harmony"],
                "negative": ["concrete", "literal", "mundane", "ordinary"]
            }
        }
        
        score = 0.8  # Base score
        issues = []
        recommendations = []
        
        if guide_personality in personality_traits:
            traits = personality_traits[guide_personality]
            
            # Check for positive trait alignment
            positive_matches = sum(1 for word in traits["positive"] if word in content)
            if positive_matches == 0:
                score -= 0.2
                issues.append(f"Response lacks {guide_personality} personality traits")
                recommendations.append(
                    f"Include more {guide_personality.replace('_', ' ')} characteristics"
                )
            else:
                score = min(1.0, score + (0.05 * positive_matches))
            
            # Check for negative trait presence
            negative_matches = sum(1 for word in traits["negative"] if word in content)
            if negative_matches > 0:
                score -= 0.1 * negative_matches
                issues.append(f"Response contains inappropriate traits for {guide_personality}")
                recommendations.append(
                    f"Avoid terms that conflict with {guide_personality.replace('_', ' ')} persona"
                )
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_mythological_accuracy(
        self,
        message: Message
    ) -> Dict:
        """Validate mythological references and accuracy."""
        content = message.content.lower()
        score = 1.0
        issues = []
        recommendations = []
        
        # Check each mythology's references
        for mythology, deities in self._mythological_references.items():
            for deity, info in deities.items():
                if deity in content:
                    # Check if deity's domains are properly referenced
                    domain_matches = sum(1 for domain in info["domains"] if domain in content)
                    if domain_matches == 0:
                        score -= 0.1
                        issues.append(
                            f"Reference to {deity} lacks proper domain context"
                        )
                        recommendations.append(
                            f"When mentioning {deity}, include reference to their domains: {', '.join(info['domains'])}"
                        )
                    else:
                        score = min(1.0, score + (0.05 * domain_matches))
        
        # Check for mixed mythology consistency
        mythologies_referenced = set()
        for mythology in self._mythological_references:
            if any(deity in content for deity in self._mythological_references[mythology]):
                mythologies_referenced.add(mythology)
        
        if len(mythologies_referenced) > 1:
            score *= 0.9
            issues.append("Multiple mythological systems referenced")
            recommendations.append(
                "Consider focusing on one mythological system unless explicitly comparing"
            )
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }
    
    async def _check_response_quality(
        self,
        message: Message
    ) -> Dict:
        """Validate general response quality and latency."""
        content = message.content
        response_time = message.metadata.get("response_time_ms", 1000)
        
        score = 1.0
        issues = []
        recommendations = []
        
        # Check response length
        word_count = len(content.split())
        if word_count < 10:
            score -= 0.2
            issues.append("Response too short")
            recommendations.append("Provide more detailed responses")
        elif word_count > 200:
            score -= 0.1
            issues.append("Response may be too verbose")
            recommendations.append("Consider being more concise")
        
        # Check response time
        if response_time > 1000:  # More than 1 second
            score -= 0.1
            issues.append("Response time too high")
            recommendations.append("Optimize response generation")
        
        # Check sentence structure
        sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        if len(sentences) < 2:
            score -= 0.1
            issues.append("Response lacks structural complexity")
            recommendations.append("Use more varied sentence structure")
        
        # Check for repeated words
        words = content.lower().split()
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
        
        repeated_words = [word for word, count in word_freq.items() if count > 3]
        if repeated_words:
            score -= 0.1
            issues.append("Excessive word repetition")
            recommendations.append(
                f"Reduce repetition of: {', '.join(repeated_words)}"
            )
        
        return {
            "score": max(0.0, min(1.0, score)),
            "issues": issues,
            "recommendations": recommendations
        }

class ValidationMetrics:
    """Tracks and analyzes validation metrics over time."""
    
    def __init__(self):
        self.metrics: List[ValidationResult] = []
        
    def add_result(self, result: ValidationResult) -> None:
        """Add a validation result to the metrics tracker."""
        self.metrics.append(result)
    
    def get_average_score(self) -> float:
        """Calculate the average validation score."""
        if not self.metrics:
            return 0.0
        return sum(r.score for r in self.metrics) / len(self.metrics)
    
    def get_common_issues(self, limit: int = 10) -> List[str]:
        """Get the most common validation issues."""
        issue_counts: Dict[str, int] = {}
        for result in self.metrics:
            for issue in result.issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        sorted_issues = sorted(
            issue_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [issue for issue, _ in sorted_issues[:limit]] 