"""Token Analysis Functions

This module provides specialized analysis functions that build on top of the
Counterparty client to provide deeper insights into token patterns.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from collections import defaultdict

from .counterparty_client import (
    CounterpartyClient, TokenInfo, IssuanceEvent,
    SendEvent, DispenserInfo, DividendEvent
)

@dataclass
class CreatorProfile:
    """Profile information about a token creator."""
    address: str
    total_tokens_created: int
    active_tokens: List[str]
    total_issuance_count: int
    avg_token_lifetime: float
    issuance_frequency: float
    holder_retention_rate: float
    dividend_frequency: float
    dispenser_usage_rate: float

@dataclass
class CollectorProfile:
    """Profile information about a token collector."""
    address: str
    total_tokens_held: int
    unique_tokens: List[str]
    avg_holding_time: float
    trading_frequency: float
    collection_categories: Dict[str, float]
    interaction_score: float

@dataclass
class TokenAnalysis:
    """Comprehensive token analysis results."""
    token_info: TokenInfo
    creator_profile: CreatorProfile
    top_collectors: List[CollectorProfile]
    ownership_distribution: Dict[str, float]
    trading_patterns: Dict[str, Any]
    metadata_analysis: Dict[str, Any]
    community_metrics: Dict[str, float]

def analyze_creator_behavior(
    client: CounterpartyClient,
    creator_address: str,
    start_block: Optional[int] = None
) -> CreatorProfile:
    """Analyze token creator behavior and patterns.
    
    Args:
        client: CounterpartyClient instance
        creator_address: Address of the creator to analyze
        start_block: Optional starting block for analysis
        
    Returns:
        CreatorProfile object with creator metrics
    """
    try:
        # Get all tokens created by this address
        created_tokens = []
        issuance_counts = defaultdict(int)
        token_first_seen = {}
        token_last_seen = {}
        
        # Analyze issuance patterns
        for token in created_tokens:
            issuances = client.get_issuances(token, start_block)
            for issuance in issuances:
                issuance_counts[token] += 1
                if token not in token_first_seen:
                    token_first_seen[token] = issuance.block_time
                token_last_seen[token] = max(
                    token_last_seen.get(token, 0),
                    issuance.block_time
                )
        
        # Calculate metrics
        total_tokens = len(created_tokens)
        total_issuances = sum(issuance_counts.values())
        avg_lifetime = np.mean([
            token_last_seen[t] - token_first_seen[t]
            for t in created_tokens
        ]) if created_tokens else 0
        
        # Get dividend and dispenser activity
        dividend_count = 0
        dispenser_count = 0
        for token in created_tokens:
            dividend_count += len(client.get_dividends(token))
            dispenser_count += len(
                client.get_dispensers(token, status_in=['valid'])
            )
        
        return CreatorProfile(
            address=creator_address,
            total_tokens_created=total_tokens,
            active_tokens=[t for t in created_tokens if not token_last_seen[t]],
            total_issuance_count=total_issuances,
            avg_token_lifetime=avg_lifetime,
            issuance_frequency=total_issuances / total_tokens if total_tokens else 0,
            holder_retention_rate=0.0,  # Needs historical holder analysis
            dividend_frequency=dividend_count / total_tokens if total_tokens else 0,
            dispenser_usage_rate=dispenser_count / total_tokens if total_tokens else 0
        )
    except Exception as e:
        raise Exception(f"Error analyzing creator behavior: {e}")

def analyze_collector_behavior(
    client: CounterpartyClient,
    collector_address: str,
    start_block: Optional[int] = None
) -> CollectorProfile:
    """Analyze token collector behavior and patterns.
    
    Args:
        client: CounterpartyClient instance
        collector_address: Address of the collector to analyze
        start_block: Optional starting block for analysis
        
    Returns:
        CollectorProfile object with collector metrics
    """
    try:
        # Track token holdings and transactions
        held_tokens = set()
        token_hold_times = defaultdict(list)
        token_categories = defaultdict(float)
        
        # Analyze send events (both receiving and sending)
        total_transactions = 0
        for token in held_tokens:
            sends = client.get_sends(token, start_block)
            for send in sends:
                if send.source == collector_address or send.destination == collector_address:
                    total_transactions += 1
                    
                    # Track holding periods
                    if send.destination == collector_address:
                        token_hold_times[token].append(send.block_time)
                    elif send.source == collector_address:
                        if token_hold_times[token]:
                            hold_time = send.block_time - token_hold_times[token][-1]
                            token_hold_times[token].append(hold_time)
        
        # Calculate average holding time
        avg_hold_time = np.mean([
            np.mean(times) for times in token_hold_times.values()
            if times
        ]) if token_hold_times else 0
        
        # Analyze token categories
        for token in held_tokens:
            token_info = client.get_token_info(token)
            # Add category scores based on token metadata
            
        return CollectorProfile(
            address=collector_address,
            total_tokens_held=len(held_tokens),
            unique_tokens=list(held_tokens),
            avg_holding_time=avg_hold_time,
            trading_frequency=total_transactions / len(held_tokens) if held_tokens else 0,
            collection_categories=dict(token_categories),
            interaction_score=0.0  # Needs more complex interaction analysis
        )
    except Exception as e:
        raise Exception(f"Error analyzing collector behavior: {e}")

def analyze_token_lifecycle(
    client: CounterpartyClient,
    token_name: str,
    start_block: Optional[int] = None
) -> TokenAnalysis:
    """Perform comprehensive analysis of a token's lifecycle.
    
    Args:
        client: CounterpartyClient instance
        token_name: Name of the token to analyze
        start_block: Optional starting block for analysis
        
    Returns:
        TokenAnalysis object with comprehensive analysis
    """
    try:
        # Get basic token info
        token_info = client.get_token_info(token_name)
        
        # Analyze creator behavior
        creator_profile = analyze_creator_behavior(
            client, token_info.issuer, start_block
        )
        
        # Get and analyze top holders
        holders = client.get_token_holders(token_name)
        top_holders = sorted(
            holders.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Analyze top collectors
        top_collectors = []
        for address, _ in top_holders:
            if address != token_info.issuer:  # Skip creator
                collector_profile = analyze_collector_behavior(
                    client, address, start_block
                )
                top_collectors.append(collector_profile)
        
        # Calculate ownership distribution
        total_supply = sum(holders.values())
        ownership_dist = {
            'creator': holders.get(token_info.issuer, 0) / total_supply,
            'top_10': sum(amount for _, amount in top_holders) / total_supply,
            'other': 1.0 - (sum(amount for _, amount in top_holders) / total_supply)
        }
        
        # Analyze trading patterns
        market_history = client.get_market_history(token_name, "XCP")
        trading_patterns = {
            'total_orders': len(market_history['orders']),
            'total_matches': len(market_history['matches']),
            'avg_order_size': np.mean([
                order.give_quantity 
                for order in market_history['orders']
            ]) if market_history['orders'] else 0,
            'trading_volume_24h': 0.0,  # Needs time-based filtering
            'price_volatility': 0.0  # Needs price history analysis
        }
        
        # Analyze metadata and community metrics
        metadata_analysis = {
            'description_length': len(token_info.description),
            'has_long_name': bool(token_info.asset_longname),
            'is_divisible': token_info.divisible,
            'is_locked': token_info.locked,
            'issuance_count': len(client.get_issuances(token_name)),
            'dividend_count': len(client.get_dividends(token_name)),
            'dispenser_count': len(client.get_dispensers(token_name))
        }
        
        community_metrics = {
            'unique_holders': len(holders),
            'active_traders': len(set(
                order.source for order in market_history['orders']
            )),
            'holder_growth_rate': 0.0,  # Needs historical analysis
            'community_engagement': 0.0  # Needs more metrics
        }
        
        return TokenAnalysis(
            token_info=token_info,
            creator_profile=creator_profile,
            top_collectors=top_collectors,
            ownership_distribution=ownership_dist,
            trading_patterns=trading_patterns,
            metadata_analysis=metadata_analysis,
            community_metrics=community_metrics
        )
    except Exception as e:
        raise Exception(f"Error analyzing token lifecycle: {e}")

def main():
    """Example usage of token analysis functions."""
    client = CounterpartyClient("http://localhost:4000/api")
    
    try:
        token_name = "MYASSETA"
        
        # Perform comprehensive token analysis
        analysis = analyze_token_lifecycle(client, token_name)
        
        # Print results
        print(f"\nToken Analysis for {token_name}:")
        print("\nCreator Profile:")
        print(f"Total Tokens Created: {analysis.creator_profile.total_tokens_created}")
        print(f"Issuance Frequency: {analysis.creator_profile.issuance_frequency:.2f}")
        
        print("\nOwnership Distribution:")
        for category, percentage in analysis.ownership_distribution.items():
            print(f"{category}: {percentage:.2%}")
        
        print("\nTrading Patterns:")
        print(f"Total Orders: {analysis.trading_patterns['total_orders']}")
        print(f"Total Matches: {analysis.trading_patterns['total_matches']}")
        
        print("\nCommunity Metrics:")
        print(f"Unique Holders: {analysis.community_metrics['unique_holders']}")
        print(f"Active Traders: {analysis.community_metrics['active_traders']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 