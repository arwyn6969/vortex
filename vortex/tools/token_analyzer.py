"""Token Analyzer Module

This module provides functionality for analyzing comprehensive token metadata,
including names, descriptions, supply, issuances, ownership patterns, and
creator/collector relationships.
"""

from typing import Dict, List, Set, Tuple, Optional
import re
import logging
from collections import Counter, defaultdict
from functools import lru_cache
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.sentiment import SentimentIntensityAnalyzer
from dataclasses import dataclass
from cachetools import TTLCache, cached

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class IssuanceMetadata:
    """Data class to hold issuance-specific metadata."""
    issuance_id: str
    timestamp: str
    amount: int
    issuer: str
    description: Optional[str] = None
    locked: bool = False
    divisible: bool = False

@dataclass
class OwnershipMetadata:
    """Data class to hold ownership patterns and statistics."""
    total_holders: int
    creator_balance: int
    top_holders: Dict[str, int]  # address -> balance
    holder_distribution: Dict[str, int]  # balance_range -> count
    creator_vs_collector_ratio: float
    ownership_concentration: float  # Gini coefficient

@dataclass
class TokenMetadata:
    """Data class to hold comprehensive token metadata and analysis results."""
    # Basic Info
    name: str
    description: str
    supply: int
    divisible: bool
    locked: bool
    
    # Ownership and Distribution
    ownership: OwnershipMetadata
    issuances: List[IssuanceMetadata]
    
    # Analysis Results
    keywords: Dict[str, float]  # keyword -> importance score
    ngrams: List[Tuple[str, ...]]
    sentiment_scores: Dict[str, float]
    categories: Dict[str, float]  # category -> confidence score
    clusters: Optional[Dict[str, List[str]]] = None  # cluster label -> keywords
    
    # Creator/Collector Metrics
    creator_activity_score: float
    collector_engagement_score: float
    trading_velocity: float

class TokenAnalyzer:
    """Analyzes comprehensive token metadata including supply, issuances, and ownership."""
    
    def __init__(self, cache_ttl: int = 3600):
        """Initialize the TokenAnalyzer with required resources."""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.error(f"Failed to download NLTK resources: {e}")
            raise
        
        self.stop_words = set(stopwords.words('english'))
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.token_cache = TTLCache(maxsize=1000, ttl=cache_ttl)
        
        # Enhanced domain-specific categories with weighted keywords
        self.category_keywords = {
            'collectible': {
                'rare': 1.0, 'unique': 0.9, 'limited': 0.8, 'edition': 0.7,
                'collectible': 1.0, 'exclusive': 0.9, 'special': 0.7
            },
            'cultural': {
                'meme': 1.0, 'art': 0.9, 'culture': 0.8, 'iconic': 0.9,
                'viral': 0.8, 'trending': 0.7, 'popular': 0.6
            },
            'gaming': {
                'game': 1.0, 'player': 0.9, 'score': 0.8, 'level': 0.8,
                'achievement': 0.9, 'quest': 0.8, 'reward': 0.7
            },
            'financial': {
                'coin': 1.0, 'token': 1.0, 'value': 0.9, 'market': 0.8,
                'trade': 0.9, 'investment': 0.8, 'asset': 0.8
            },
            'utility': {
                'use': 0.8, 'utility': 1.0, 'function': 0.8, 'purpose': 0.7,
                'application': 0.8, 'service': 0.7
            },
            'creator': {
                'artist': 1.0, 'creator': 1.0, 'author': 0.9, 'designer': 0.9,
                'original': 0.8, 'authentic': 0.8
            },
            'collector': {
                'collector': 1.0, 'collection': 0.9, 'portfolio': 0.8,
                'curated': 0.8, 'preserved': 0.7
            }
        }

    def analyze_ownership_patterns(
        self, holders: Dict[str, int], creator_address: str, total_supply: int
    ) -> OwnershipMetadata:
        """Analyze token ownership patterns and distribution."""
        try:
            # Sort holders by balance
            sorted_holders = dict(sorted(holders.items(), key=lambda x: x[1], reverse=True))
            
            # Calculate creator balance
            creator_balance = holders.get(creator_address, 0)
            
            # Get top holders (excluding creator if in top)
            top_holders = {
                addr: bal for addr, bal in list(sorted_holders.items())[:10]
                if addr != creator_address
            }
            
            # Calculate holder distribution ranges
            ranges = {
                "1-10": 0,
                "11-100": 0,
                "101-1000": 0,
                "1001+": 0
            }
            for balance in holders.values():
                if balance <= 10:
                    ranges["1-10"] += 1
                elif balance <= 100:
                    ranges["11-100"] += 1
                elif balance <= 1000:
                    ranges["101-1000"] += 1
                else:
                    ranges["1001+"] += 1
            
            # Calculate creator vs collector ratio
            total_balance = sum(holders.values())
            creator_ratio = creator_balance / total_balance if total_balance > 0 else 0
            
            # Calculate Gini coefficient for ownership concentration
            if len(holders) > 1:
                balances = sorted(holders.values())
                n = len(balances)
                index = np.arange(1, n + 1)
                gini = ((np.sum((2 * index - n - 1) * balances)) / 
                       (n * np.sum(balances)))
            else:
                gini = 0.0
            
            return OwnershipMetadata(
                total_holders=len(holders),
                creator_balance=creator_balance,
                top_holders=top_holders,
                holder_distribution=ranges,
                creator_vs_collector_ratio=creator_ratio,
                ownership_concentration=gini
            )
        except Exception as e:
            logger.error(f"Error analyzing ownership patterns: {e}")
            return OwnershipMetadata(
                total_holders=0,
                creator_balance=0,
                top_holders={},
                holder_distribution={},
                creator_vs_collector_ratio=0.0,
                ownership_concentration=0.0
            )

    def analyze_issuance_patterns(
        self, issuances: List[IssuanceMetadata]
    ) -> Tuple[float, float, float]:
        """Analyze issuance patterns to calculate activity scores."""
        try:
            if not issuances:
                return 0.0, 0.0, 0.0
            
            # Sort issuances by timestamp
            sorted_issuances = sorted(issuances, key=lambda x: x.timestamp)
            
            # Calculate creator activity score based on issuance frequency and amounts
            time_diffs = []
            amounts = []
            for i in range(1, len(sorted_issuances)):
                time_diffs.append(
                    float(sorted_issuances[i].timestamp) - 
                    float(sorted_issuances[i-1].timestamp)
                )
                amounts.append(sorted_issuances[i].amount)
            
            if time_diffs:
                avg_time_between_issuances = np.mean(time_diffs)
                std_time_between_issuances = np.std(time_diffs)
                creator_activity = 1.0 / (1.0 + avg_time_between_issuances)
            else:
                creator_activity = 0.0
            
            # Calculate collector engagement based on issuance descriptions and locks
            collector_engagement = sum(
                1 for i in issuances 
                if i.description and len(i.description) > 0
            ) / len(issuances)
            
            # Calculate trading velocity (rate of issuance relative to supply)
            total_issuance_amount = sum(i.amount for i in issuances)
            trading_velocity = len(issuances) * total_issuance_amount / len(issuances)
            
            return creator_activity, collector_engagement, trading_velocity
        except Exception as e:
            logger.error(f"Error analyzing issuance patterns: {e}")
            return 0.0, 0.0, 0.0

    def analyze_token(
        self,
        name: str,
        description: str,
        supply: int,
        divisible: bool,
        locked: bool,
        holders: Dict[str, int],
        creator_address: str,
        issuances: List[IssuanceMetadata]
    ) -> TokenMetadata:
        """Analyze comprehensive token metadata."""
        try:
            # Cache key for this token
            cache_key = f"{name}:{description}:{supply}:{creator_address}"
            if cache_key in self.token_cache:
                return self.token_cache[cache_key]

            # Analyze text content
            combined_text = f"{name} {description}"
            texts = [combined_text]
            keywords = self.extract_keywords_with_importance(texts)
            bigrams = self.generate_ngrams(combined_text, 2)
            sentiment_scores = self.analyze_sentiment(description)
            categories = self.categorize_token_with_confidence(keywords)
            clusters = self.cluster_keywords(keywords) if len(keywords) >= 2 else None
            
            # Analyze ownership patterns
            ownership = self.analyze_ownership_patterns(
                holders, creator_address, supply
            )
            
            # Analyze issuance patterns
            creator_activity, collector_engagement, trading_velocity = (
                self.analyze_issuance_patterns(issuances)
            )
            
            # Create comprehensive metadata
            metadata = TokenMetadata(
                name=name,
                description=description,
                supply=supply,
                divisible=divisible,
                locked=locked,
                ownership=ownership,
                issuances=issuances,
                keywords=keywords,
                ngrams=bigrams,
                sentiment_scores=sentiment_scores,
                categories=categories,
                clusters=clusters,
                creator_activity_score=creator_activity,
                collector_engagement_score=collector_engagement,
                trading_velocity=trading_velocity
            )
            
            # Cache the result
            self.token_cache[cache_key] = metadata
            
            return metadata
        except Exception as e:
            logger.error(f"Error analyzing token: {e}")
            return TokenMetadata(
                name=name,
                description=description,
                supply=0,
                divisible=False,
                locked=False,
                ownership=OwnershipMetadata(
                    total_holders=0,
                    creator_balance=0,
                    top_holders={},
                    holder_distribution={},
                    creator_vs_collector_ratio=0.0,
                    ownership_concentration=0.0
                ),
                issuances=[],
                keywords={},
                ngrams=[],
                sentiment_scores={},
                categories={},
                clusters=None,
                creator_activity_score=0.0,
                collector_engagement_score=0.0,
                trading_velocity=0.0
            )

    def batch_analyze_tokens(
        self, token_data: List[Tuple[str, str, int, bool, bool, Dict[str, int], str, List[IssuanceMetadata]]]
    ) -> List[TokenMetadata]:
        """Analyze multiple tokens in batch."""
        try:
            return [
                self.analyze_token(
                    name, description, supply, divisible, locked,
                    holders, creator_address, issuances
                )
                for (
                    name, description, supply, divisible, locked,
                    holders, creator_address, issuances
                ) in token_data
            ]
        except Exception as e:
            logger.error(f"Error in batch analysis: {e}")
            return []

def main():
    """Example usage of TokenAnalyzer."""
    analyzer = TokenAnalyzer()
    
    # Example token data
    example_issuance = IssuanceMetadata(
        issuance_id="1",
        timestamp="1620000000",
        amount=100,
        issuer="creator_address",
        description="Initial issuance",
        locked=False,
        divisible=True
    )
    
    example_holders = {
        "creator_address": 50,
        "collector1": 25,
        "collector2": 25
    }
    
    tokens = [
        (
            "PEPE_COIN",
            "A rare collectible token featuring the iconic Pepe meme.",
            100,  # supply
            True,  # divisible
            False,  # locked
            example_holders,
            "creator_address",
            [example_issuance]
        ),
    ]
    
    # Batch analyze tokens
    results = analyzer.batch_analyze_tokens(tokens)
    
    # Print results
    for metadata in results:
        print(f"\nToken: {metadata.name}")
        print(f"Supply: {metadata.supply}")
        print(f"Top Keywords: {dict(list(metadata.keywords.items())[:5])}")
        print(f"Categories: {metadata.categories}")
        print(f"Sentiment: {metadata.sentiment_scores}")
        print(f"Creator Activity Score: {metadata.creator_activity_score:.2f}")
        print(f"Collector Engagement: {metadata.collector_engagement_score:.2f}")
        print(f"Trading Velocity: {metadata.trading_velocity:.2f}")
        print(f"Ownership Concentration: {metadata.ownership.ownership_concentration:.2f}")
        print(f"Total Holders: {metadata.ownership.total_holders}")
        if metadata.clusters:
            print(f"Keyword Clusters: {metadata.clusters}")

if __name__ == "__main__":
    main() 