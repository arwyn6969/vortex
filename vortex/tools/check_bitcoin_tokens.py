#!/usr/bin/env python3
"""Command-line tool to check Bitcoin tokens and their multipliers."""

import asyncio
import argparse
from decimal import Decimal
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.finance.bitcoin_tokens import BitcoinTokenService
from src.core.finance.token_config import (
    calculate_token_multipliers,
    SPECIAL_SRC20_MULTIPLIERS,
    SPECIAL_STAMPS_MULTIPLIERS
)

async def check_address(address: str, show_all: bool = False):
    """Check Bitcoin tokens for an address.
    
    Args:
        address: Bitcoin address to check
        show_all: Whether to show all tokens or only those with multipliers
    """
    service = BitcoinTokenService()
    
    try:
        print(f"\nChecking address: {address}")
        print("Fetching balances...")
        
        balances = await service.get_combined_balances(address)
        
        if not balances:
            print("\nNo tokens found for this address.")
            return
            
        # Group tokens
        src20_tokens = []
        stamps = []
        owned_src20_ticks = set()
        owned_stamps = set()
        
        for token in balances:
            if token.token_type.name == "SRC20":
                src20_tokens.append(token)
                if token.balance > 0:
                    owned_src20_ticks.add(token.token_id)
            else:
                stamps.append(token)
                if token.balance > 0:
                    owned_stamps.add(token.token_id)
        
        # Show SRC-20 tokens
        if src20_tokens:
            print("\nSRC-20 Tokens:")
            for token in src20_tokens:
                if show_all or token.token_id in SPECIAL_SRC20_MULTIPLIERS:
                    multiplier = SPECIAL_SRC20_MULTIPLIERS.get(token.token_id)
                    multiplier_text = f" (+{multiplier}x multiplier)" if multiplier else ""
                    print(f"- {token.token_id}: {token.balance}{multiplier_text}")
        
        # Show STAMPS
        if stamps:
            print("\nSTAMPS:")
            for token in stamps:
                if show_all or token.token_id in SPECIAL_STAMPS_MULTIPLIERS:
                    multiplier = SPECIAL_STAMPS_MULTIPLIERS.get(token.token_id)
                    multiplier_text = f" (+{multiplier}x multiplier)" if multiplier else ""
                    print(f"- {token.token_id}: {token.balance}{multiplier_text}")
        
        # Calculate and show multiplier effect
        multiplier = calculate_token_multipliers(owned_src20_ticks, owned_stamps)
        base_rate = Decimal("0.001")
        effective_rate = base_rate * multiplier
        
        print("\nMultiplier Summary:")
        print(f"Total Multiplier: {multiplier}x")
        print(f"Base Token Rate: {base_rate} per keystroke")
        print(f"Effective Token Rate: {effective_rate} per keystroke")
        
        # Show potential multipliers from unowned tokens
        potential_src20 = set(SPECIAL_SRC20_MULTIPLIERS.keys()) - owned_src20_ticks
        potential_stamps = set(SPECIAL_STAMPS_MULTIPLIERS.keys()) - owned_stamps
        
        if potential_src20 or potential_stamps:
            print("\nPotential Additional Multipliers:")
            
            if potential_src20:
                print("\nFrom SRC-20 tokens:")
                for tick in potential_src20:
                    print(f"- {tick}: +{SPECIAL_SRC20_MULTIPLIERS[tick]}x")
            
            if potential_stamps:
                print("\nFrom STAMPS:")
                for stamp_id in potential_stamps:
                    print(f"- {stamp_id}: +{SPECIAL_STAMPS_MULTIPLIERS[stamp_id]}x")
    
    finally:
        await service.close()

def main():
    parser = argparse.ArgumentParser(description="Check Bitcoin tokens and their multipliers")
    parser.add_argument("address", help="Bitcoin address to check")
    parser.add_argument("--all", action="store_true", help="Show all tokens, not just those with multipliers")
    
    args = parser.parse_args()
    asyncio.run(check_address(args.address, args.all))

if __name__ == "__main__":
    main() 