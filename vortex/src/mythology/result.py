"""
Mythology Validation Result Data Structures

This module defines the ValidationResult dataclass for use across the mythology package.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    """Results of a validation check."""
    is_valid: bool
    issues: List[str]
    suggestions: List[str]
    confidence_score: float  # 0.0 to 1.0
    source_references: List[str]  