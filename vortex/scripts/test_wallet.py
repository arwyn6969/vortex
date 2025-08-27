#!/usr/bin/env python3
"""Manual testing script for Bitcoin wallet functionality."""

import sys
import os
import pytest

pytest.skip("Manual wallet script - skip under pytest", allow_module_level=True)

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

from core.crypto.wallet import BitcoinWallet
from core.crypto.keys import HDWallet

def test_new_wallet():
    """Test creating a new wallet."""
    print("\n=== Testing New Wallet Creation ===")
    wallet = BitcoinWallet(debug_mode=True)
    info, recovery = wallet.create_new_wallet()
    
    print("\nWallet Info:")
    print(f"Address: {info.address}")
    print(f"Type: {info.address_type.value}")
    print(f"Derivation Path: {info.derivation_path}")
    print(f"Has Private Key: {bool(info.private_key)}")
    
    print("\nRecovery Info:")
    print(f"Mnemonic: {recovery['mnemonic']}")
    print("\nBackup Instructions:")
    for instruction in recovery["backup_instructions"]:
        print(f"- {instruction}")

def test_existing_wallet():
    """Test importing an existing wallet."""
    print("\n=== Testing Existing Wallet Import ===")
    
    # Test with a known private key (WIF format)
    test_key = "5KQNQhZvE9nYYhpxjVoBDrEYgWQjBrMZFtBGkHXunAGAhep5oUk"
    
    wallet = BitcoinWallet(debug_mode=True)
    info, msg = wallet.process_wallet_input(test_key)
    
    print("\nImport Result:")
    print(msg)
    print("\nWallet Info:")
    print(f"Address: {info.address}")
    print(f"Type: {info.address_type.value}")
    print(f"Balance: {info.balance} BTC")
    
    if info.transaction_history:
        print(f"\nLast {len(info.transaction_history)} transactions:")
        for tx in info.transaction_history:
            print(f"- Hash: {tx.get('hash', 'N/A')}")
            print(f"  Time: {tx.get('time', 'N/A')}")

def test_address_detection():
    """Test address type detection."""
    print("\n=== Testing Address Type Detection ===")
    
    test_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Legacy
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # SegWit
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4",  # Native SegWit
        "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0",  # Taproot
    ]
    
    wallet = BitcoinWallet()
    for address in test_addresses:
        addr_type, error = wallet.detect_address_type(address)
        print(f"\nAddress: {address}")
        print(f"Type: {addr_type.value if addr_type else 'Unknown'}")
        if error:
            print(f"Error: {error}")

def test_balance_check():
    """Test balance checking functionality."""
    print("\n=== Testing Balance Check ===")
    
    # Test with Bitcoin genesis address
    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    
    wallet = BitcoinWallet()
    balance, error, history = wallet.get_balance(address)
    
    print(f"\nAddress: {address}")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Balance: {balance} BTC")
        if history:
            print(f"Transaction Count: {len(history)}")

def main():
    """Run all tests."""
    try:
        test_new_wallet()
        test_existing_wallet()
        test_address_detection()
        test_balance_check()
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main()) 