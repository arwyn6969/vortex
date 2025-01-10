#!/usr/bin/env python3
"""Enhanced Bitcoin message signing tool."""

import sys
import argparse
import json
from datetime import datetime
from typing import Optional, Dict, Any

from vortex.src.core.crypto.wallet import BitcoinWallet
from vortex.src.core.crypto.keys import is_message_safe

def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with all options."""
    parser = argparse.ArgumentParser(description="Sign messages with Bitcoin private keys")
    
    parser.add_argument("--private-key", "-k", help="Bitcoin private key (WIF or hex format)")
    parser.add_argument("--message", "-m", help="Message to sign")
    parser.add_argument("--template", "-t", choices=['profile', 'session', 'challenge', 'token'],
                       help="Use a predefined message template")
    parser.add_argument("--template-vars", "-v", type=json.loads,
                       help="JSON string of template variables")
    parser.add_argument("--output", "-o", choices=['text', 'json'], default='text',
                       help="Output format (default: text)")
    parser.add_argument("--qr", action="store_true", help="Generate QR codes for outputs")
    
    return parser

def generate_qr(data: str) -> None:
    """Generate and display QR code."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii()
    except ImportError:
        print("Warning: qrcode package not installed. QR code generation skipped.")

def format_output(result: Dict[str, Any], format: str = 'text', show_qr: bool = False) -> None:
    """Format and display the output."""
    if format == 'json':
        print(json.dumps(result, indent=2))
    else:
        print("\n=== Bitcoin Message Signing ===")
        print(f"\nAddress: {result['address']}")
        print(f"Message: {result['message']}")
        print(f"\nSignature: {result['signature']}")
        print(f"\nTimestamp: {result['timestamp']}")
        
        if result.get('error'):
            print(f"\nError: {result['error']}")
            
    if show_qr and result.get('signature'):
        print("\nSignature QR Code:")
        generate_qr(result['signature'])
        
        print("\nFull Data QR Code:")
        generate_qr(json.dumps(result))

def main() -> None:
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()
    
    wallet = BitcoinWallet(debug_mode=True)
    result: Dict[str, Any] = {
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        # Handle template-based message generation
        if args.template:
            if not args.template_vars:
                args.template_vars = {}
            message, error = wallet.generate_verification_message(args.template, **args.template_vars)
            if error:
                result['error'] = error
                format_output(result, args.output, args.qr)
                return
            args.message = message
            
        # Validate inputs
        if not args.private_key:
            result['error'] = "Private key is required"
            format_output(result, args.output, args.qr)
            return
            
        if not args.message:
            result['error'] = "Message is required"
            format_output(result, args.output, args.qr)
            return
            
        # Check message safety
        is_safe, error = is_message_safe(args.message)
        if not is_safe:
            result['error'] = f"Unsafe message: {error}"
            format_output(result, args.output, args.qr)
            return
            
        # Get wallet info
        wallet_info, error = wallet.process_wallet_input(args.private_key)
        if error:
            result['error'] = error
            format_output(result, args.output, args.qr)
            return
            
        result['address'] = wallet_info.address
        result['message'] = args.message
        
        # Sign message
        signature, error = wallet.sign_message(args.message, args.private_key)
        if error:
            result['error'] = error
            format_output(result, args.output, args.qr)
            return
            
        result['signature'] = signature
        format_output(result, args.output, args.qr)
        
    except Exception as e:
        result['error'] = f"Error: {str(e)}"
        format_output(result, args.output, args.qr)
        return

if __name__ == "__main__":
    main() 