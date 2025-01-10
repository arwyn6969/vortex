"""Taproot support module implementing BIP341."""

import hashlib
from typing import Tuple, Optional, List
from .bech32m import encode_segwit_address, decode_segwit_address
import coincurve
from coincurve.context import GLOBAL_CONTEXT
from coincurve.utils import int_to_bytes
from .keys import HDWallet

def tagged_hash(tag: str, msg: bytes) -> bytes:
    """BIP340 tagged hash."""
    tag_hash = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(tag_hash + tag_hash + msg).digest()

def lift_x(x: bytes) -> Tuple[bytes, bool]:
    """
    Lift an x coordinate to a point on the curve.
    Returns (pubkey_bytes, is_odd).
    """
    pubkey = coincurve.PublicKey(b'\x02' + x)
    pubkey_bytes = pubkey.format(compressed=True)
    return pubkey_bytes[1:], pubkey_bytes[0] == 3

def tweak_pubkey(pubkey: bytes, merkle_root: Optional[bytes] = None) -> Tuple[bytes, bool]:
    """
    Compute tweaked public key for Taproot output.
    Returns (tweaked_pubkey, parity).
    """
    # Convert to x-only pubkey format if needed
    if len(pubkey) == 33:
        pubkey = pubkey[1:]
    
    # Compute tweak
    if merkle_root:
        tweak = tagged_hash("TapTweak", pubkey + merkle_root)
    else:
        tweak = tagged_hash("TapTweak", pubkey)
    
    # Add tweak to public key
    try:
        # Lift x coordinate to curve point
        point_bytes, is_odd = lift_x(pubkey)
        
        # Create tweaked point
        tweak_int = int.from_bytes(tweak, 'big')
        tweak_bytes = int_to_bytes(tweak_int)
        
        # Create public key from original point
        original = coincurve.PublicKey(b'\x02' + point_bytes)
        
        # Create public key from tweak
        tweak_point = coincurve.PublicKey.from_secret(tweak_bytes)
        
        # Add points using the context
        tweaked = original.combine([coincurve.PublicKey(tweak_point.format())])
        tweaked_bytes = tweaked.format(compressed=True)
        
        return tweaked_bytes[1:], tweaked_bytes[0] == 2
    except Exception as e:
        raise ValueError(f"Invalid public key for tweaking: {str(e)}")

def encode_bech32m(hrp: str, witver: int, witprog: bytes) -> str:
    """Encode a segwit address with bech32m."""
    ret = encode_segwit_address(hrp, witver, witprog)
    if ret is None:
        raise ValueError("Invalid segwit program")
    return ret

def decode_bech32m(addr: str) -> Tuple[str, int, bytes]:
    """Decode a segwit address with bech32m."""
    try:
        witver, witprog = decode_segwit_address("bc", addr)
        if witver is None or witprog is None:
            raise ValueError("Invalid segwit address")
        return "bc", witver, witprog
    except Exception as e:
        raise ValueError(f"Invalid segwit address: {str(e)}")

def generate_taproot_address(pubkey: bytes, merkle_root: Optional[bytes] = None) -> str:
    """
    Generate Taproot address from public key and optional script tree.
    Follows BIP341 specification.
    """
    # Get tweaked key
    output_key, _ = tweak_pubkey(pubkey, merkle_root)
    
    # Convert to bech32m
    program = output_key
    witver = 0x01  # Taproot witness version
    return encode_bech32m("bc", witver, program)

def verify_taproot_address(address: str) -> bool:
    """Verify a Taproot address."""
    try:
        hrp, version, program = decode_bech32m(address)
        if hrp != "bc" or version != 0x01:
            return False
        if len(program) != 32:  # P2TR output key is 32 bytes
            return False
        return True
    except Exception:
        return False

def derive_taproot_keys(wallet: HDWallet, path: str = "m/86'/0'/0'/0/0") -> Tuple[bytes, bytes]:
    """
    Derive Taproot keys using BIP86 derivation path.
    Returns (private_key, public_key).
    """
    # Derive key pair
    private_key, public_key = wallet.derive_key_pair(path)
    
    # Convert to x-only public key format
    if len(public_key) == 33:
        public_key = public_key[1:]
        
    return private_key, public_key 