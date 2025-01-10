"""
User profiling module for Vortex.
Handles behavioral analysis, profiling, and personalization.
"""

from .profile_matrix import ProfileMatrix, ProfileDimension, BehavioralProfile
from .behavioral_analysis import BehavioralAnalysis, InteractionEvent
from .personalization import PersonalizationEngine, ContentItem
from .adaptive_learning import LearningPathNode
from .meta_analysis import (
    MetaAnalysis,
    DimensionCorrelation,
    DimensionTrend,
    ConsistencyMetric
)

__all__ = [
    'ProfileMatrix',
    'ProfileDimension',
    'BehavioralProfile',
    'BehavioralAnalysis',
    'InteractionEvent',
    'PersonalizationEngine',
    'ContentItem',
    'LearningPathNode',
    'MetaAnalysis',
    'DimensionCorrelation',
    'DimensionTrend',
    'ConsistencyMetric'
] 