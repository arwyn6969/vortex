"""Test Bitcoin token functionality."""

import asyncio
import pytest
from decimal import Decimal
from uuid import uuid4
import unittest
from unittest.mock import Mock, patch

from vortex.src.core.finance.bitcoin_tokens import BitcoinTokenService
from ..src.core.finance.token_config import calculate_token_multipliers

TEST_ADDRESS = "1AwS3wRFNCoymKs69BXjAA4VfgWvuKvx4j"

async def test_bitcoin_tokens():
    """Test fetching and processing Bitcoin tokens."""
    service = BitcoinTokenService()
    
    try:
        # Fetch balances
        balances = await service.get_combined_balances(TEST_ADDRESS)
        
        print("\n=== Bitcoin Token Test Results ===")
        print(f"Address: {TEST_ADDRESS}")
        print("\nFound Tokens:")
        
        # Group by type
        src20_tokens = set()
        stamps = set()
        
        for token in balances:
            print(f"\nToken Type: {token.token_type.name}")
            print(f"Token ID: {token.token_id}")
            print(f"Balance: {token.balance}")
            print(f"Metadata: {token.metadata}")
            
            if token.balance > 0:
                if token.token_type.name == "SRC20":
                    src20_tokens.add(token.token_id)
                else:
                    stamps.add(token.token_id)
        
        # Calculate multipliers
        multiplier = calculate_token_multipliers(src20_tokens, stamps)
        
        print("\n=== Multiplier Results ===")
        print(f"Total Multiplier: {multiplier}x")
        print(f"Base Rate: {Decimal('0.001')} tokens per keystroke")
        print(f"Effective Rate: {Decimal('0.001') * multiplier} tokens per keystroke")
        
    finally:
        await service.close()

if __name__ == "__main__":
    asyncio.run(test_bitcoin_tokens()) 