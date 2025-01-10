#!/usr/bin/env python3
"""
Bitcoin address verification tool using message signing.
This tool allows users to verify ownership of a Bitcoin address by signing a message
with their wallet and verifying the signature.
"""

import sys
import os
import argparse
from typing import Optional, Tuple

# Add the src directory to the Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(src_path)

from src.core.crypto.wallet import BitcoinWallet, WalletInfo

def verify_address(address: str, message: str, signature: str) -> Tuple[bool, Optional[str]]:
    """
    Verify a Bitcoin address using a signed message.
    
    Args:
        address: Bitcoin address to verify
        message: Message that was signed
        signature: Base64-encoded signature
        
    Returns:
        (is_valid, error_message)
    """
    wallet = BitcoinWallet(debug_mode=True)
    
    # Process the signed message
    signed_message = {
        'address': address,
        'message': message,
        'signature': signature
    }
    
    info, msg = wallet.process_wallet_input(signed_message=signed_message)
    
    if info.address == address:
        return True, None
    else:
        return False, msg

def main():
    parser = argparse.ArgumentParser(
        description="Verify Bitcoin address ownership using message signing"
    )
    parser.add_argument("address", help="Bitcoin address to verify")
    parser.add_argument("message", help="Message that was signed")
    parser.add_argument("signature", help="Base64-encoded signature")
    
    args = parser.parse_args()
    
    print(f"\nVerifying address: {args.address}")
    print(f"Message: {args.message}")
    print(f"Signature: {args.signature[:32]}...")
    
    is_valid, error = verify_address(args.address, args.message, args.signature)
    
    if is_valid:
        print("\n✅ Address verified successfully!")
        print("The signature proves ownership of the address.")
    else:
        print("\n❌ Address verification failed!")
        if error:
            print(f"Error: {error}")
        print("The signature does not prove ownership of the address.")

if __name__ == "__main__":
    main() 