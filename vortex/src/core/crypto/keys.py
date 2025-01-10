"""Bitcoin key generation and derivation module."""

import os
import hmac
import hashlib
from typing import Tuple, List, Optional
import base58
from mnemonic import Mnemonic
import bech32
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging
import base64

logger = logging.getLogger(__name__)

try:
    import coincurve
    COINCURVE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"coincurve not available, some features will be limited: {str(e)}")
    COINCURVE_AVAILABLE = False

# Bitcoin's curve order (SECP256k1)
CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def check_dependencies() -> Tuple[bool, Optional[str]]:
    """Check if all required dependencies are available."""
    if not COINCURVE_AVAILABLE:
        return False, "coincurve library not available - some features will be limited"
    return True, None

class HDWallet:
    """
    Hierarchical Deterministic Wallet implementation following BIP32/39/44/84.
    Supports BIP39 mnemonic generation and BIP84 derivation paths for native SegWit.
    """
    
    BITCOIN_SEED_KEY = b"Bitcoin seed"
    HARDENED_INDEX = 0x80000000
    
    def __init__(self, seed: bytes):
        """Initialize HD wallet with a seed."""
        # Generate master key pair
        hmac_obj = hmac.new(self.BITCOIN_SEED_KEY, seed, hashlib.sha512)
        il, ir = hmac_obj.digest()[:32], hmac_obj.digest()[32:]
        self.master_private_key = il
        self.master_chain_code = ir
        
    @classmethod
    def from_mnemonic(cls, mnemonic: str, passphrase: str = "") -> 'HDWallet':
        """Create HD wallet from BIP39 mnemonic."""
        # Validate mnemonic
        if not Mnemonic("english").check(mnemonic):
            raise ValueError("Invalid mnemonic phrase")
            
        # Generate seed
        seed = Mnemonic.to_seed(mnemonic, passphrase)
        return cls(seed)
    
    @classmethod
    def generate_new(cls, strength: int = 256) -> Tuple['HDWallet', str]:
        """Generate new wallet with random mnemonic."""
        # Generate mnemonic
        mnemonic = Mnemonic("english").generate(strength)
        return cls.from_mnemonic(mnemonic), mnemonic
    
    def derive_key_pair(self, path: str) -> Tuple[bytes, bytes]:
        """
        Derive private and public keys from derivation path.
        Example path: "m/84'/0'/0'/0/0" for first native SegWit address.
        """
        if not path.startswith("m/"):
            raise ValueError("Invalid derivation path")
            
        # Start with master key
        key = self.master_private_key
        chain_code = self.master_chain_code
        
        # Process each level
        components = path.split("/")[1:]
        for comp in components:
            hardened = comp.endswith("'")
            index = int(comp[:-1] if hardened else comp)
            
            if hardened:
                index += self.HARDENED_INDEX
                
            # Derive key
            key, chain_code = self._derive_key(key, chain_code, index)
            
        # Generate public key using coincurve
        privkey = coincurve.PrivateKey(key)
        public_key = privkey.public_key.format(compressed=True)
        
        return key, public_key
    
    def _derive_key(self, key: bytes, chain_code: bytes, index: int) -> Tuple[bytes, bytes]:
        """Derive child key at index."""
        if index >= self.HARDENED_INDEX:
            # Hardened derivation
            data = b"\x00" + key + index.to_bytes(4, "big")
        else:
            # Normal derivation
            privkey = coincurve.PrivateKey(key)
            public_key = privkey.public_key.format(compressed=True)
            data = public_key + index.to_bytes(4, "big")
            
        # Calculate HMAC-SHA512
        hmac_obj = hmac.new(chain_code, data, hashlib.sha512)
        il, ir = hmac_obj.digest()[:32], hmac_obj.digest()[32:]
        
        # Calculate child key
        child_key = (int.from_bytes(il, "big") + int.from_bytes(key, "big")) % CURVE_ORDER
        child_key = child_key.to_bytes(32, "big")
        
        return child_key, ir

def generate_native_segwit_address(public_key: bytes, network: str = "mainnet") -> str:
    """Generate native SegWit (bech32) address from public key."""
    # Hash public key
    sha256_hash = hashlib.sha256(public_key).digest()
    h = hashlib.new("ripemd160")
    h.update(sha256_hash)
    pubkey_hash = h.digest()
    
    # Convert to bech32
    hrp = "bc" if network == "mainnet" else "tb"
    witver = 0x00
    witprog = pubkey_hash
    return bech32.encode(hrp, witver, witprog)

def create_new_wallet() -> Tuple[HDWallet, str, dict]:
    """
    Create new wallet with mnemonic and first address.
    Returns (wallet, mnemonic, wallet_info).
    """
    try:
        if not COINCURVE_AVAILABLE:
            raise ImportError("coincurve required for wallet creation")
            
        # Generate new wallet
        wallet, mnemonic = HDWallet.generate_new()
        
        # Derive first native SegWit key pair
        private_key, public_key = wallet.derive_key_pair("m/84'/0'/0'/0/0")
        
        # Generate address
        address = generate_native_segwit_address(public_key)
        
        wallet_info = {
            "derivation_path": "m/84'/0'/0'/0/0",
            "address": address,
            "private_key_wif": private_key_to_wif(private_key, compressed=True),
            "backup_instructions": [
                "Write down your mnemonic phrase in a secure location",
                "Never share your mnemonic phrase or private keys",
                "Keep multiple secure backups of your mnemonic"
            ]
        }
        
        return wallet, mnemonic, wallet_info
        
    except Exception as e:
        logger.error(f"Error creating wallet: {str(e)}")
        raise

def private_key_to_wif(private_key: bytes, compressed: bool = True, testnet: bool = False) -> str:
    """Convert private key to Wallet Import Format (WIF)."""
    # Add version byte and compression flag
    version = b"\xef" if testnet else b"\x80"
    extended_key = version + private_key
    if compressed:
        extended_key += b"\x01"
        
    # Double SHA256 for checksum
    double_sha256 = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()
    checksum = double_sha256[:4]
    
    # Encode in base58
    wif = base58.b58encode(extended_key + checksum).decode()
    return wif

def wif_to_private_key(wif: str) -> Tuple[bytes, bool, bool]:
    """
    Convert WIF to private key.
    Returns (private_key, is_compressed, is_testnet).
    """
    try:
        # Decode base58
        decoded = base58.b58decode(wif)
        
        # Extract components
        version = decoded[0]
        is_testnet = version == 0xef
        
        if len(decoded) == 38:
            private_key = decoded[1:33]
            is_compressed = True
        else:
            private_key = decoded[1:33]
            is_compressed = False
            
        # Verify checksum
        checksum = decoded[-4:]
        extended_key = decoded[:-4]
        double_sha256 = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()
        if checksum != double_sha256[:4]:
            raise ValueError("Invalid checksum")
            
        return private_key, is_compressed, is_testnet
        
    except Exception as e:
        logger.error(f"Error decoding WIF: {str(e)}")
        raise ValueError("Invalid WIF format") 

def sign_message(private_key: bytes, message: str) -> str:
    """
    Sign a message using Bitcoin's message signing format.
    Returns base64-encoded signature.
    """
    if not COINCURVE_AVAILABLE:
        raise ImportError("coincurve required for message signing")
        
    # Format message according to Bitcoin's standard
    magic_prefix = b"\x18Bitcoin Signed Message:\n"
    message_bytes = message.encode('utf-8')
    msg = magic_prefix + len(message_bytes).to_bytes(1, 'big') + message_bytes
    
    # Double SHA256 the message
    msg_hash = hashlib.sha256(hashlib.sha256(msg).digest()).digest()
    
    # Sign using coincurve (which handles RFC6979 deterministic k)
    privkey = coincurve.PrivateKey(private_key)
    signature = privkey.sign_recoverable(msg_hash, hasher=None)  # We already hashed the message
    
    # Clear private key from memory
    privkey._secret = None
    del privkey
    
    # Encode in base64
    return base64.b64encode(signature).decode('ascii')

def verify_message(address: str, message: str, signature: str, max_message_length: int = 10000) -> bool:
    """
    Verify a signed message.
    Returns True if the signature is valid for the given address and message.
    """
    if not COINCURVE_AVAILABLE:
        raise ImportError("coincurve required for message verification")
        
    try:
        # Validate message length
        if len(message) > max_message_length:
            raise ValueError(f"Message too long (max {max_message_length} characters)")
            
        # Check for common XSS/injection patterns
        if any(pattern in message.lower() for pattern in ['<script>', 'javascript:', 'data:', 'vbscript:']):
            raise ValueError("Message contains potentially malicious content")
            
        # Decode signature
        try:
            sig_bytes = base64.b64decode(signature)
        except Exception:
            raise ValueError("Invalid signature format")
        
        # Format message
        magic_prefix = b"\x18Bitcoin Signed Message:\n"
        message_bytes = message.encode('utf-8')
        msg = magic_prefix + len(message_bytes).to_bytes(1, 'big') + message_bytes
        
        # Double SHA256 the message
        msg_hash = hashlib.sha256(hashlib.sha256(msg).digest()).digest()
        
        # Recover public key from signature
        try:
            pubkey = coincurve.PublicKey.from_signature_and_message(
                sig_bytes,
                msg_hash,
                hasher=None  # We already hashed the message
            )
        except Exception:
            raise ValueError("Invalid signature or message")
        
        # Generate address from public key
        pubkey_bytes = pubkey.format(compressed=True)
        recovered_address = generate_native_segwit_address(pubkey_bytes)
        
        return recovered_address == address
        
    except Exception as e:
        logger.error(f"Error verifying message: {str(e)}")
        return False

def is_message_safe(message: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a message is safe to process.
    Returns (is_safe, error_message).
    """
    try:
        # Check length
        if len(message) > 10000:
            return False, "Message too long"
            
        # Check for potentially malicious content
        if any(pattern in message.lower() for pattern in [
            '<script>', 'javascript:', 'data:', 'vbscript:',
            'onload=', 'onerror=', 'onclick=', 'alert(', 'eval('
        ]):
            return False, "Message contains potentially malicious content"
            
        # Check character set
        if not all(ord(c) < 128 for c in message):
            return False, "Message contains non-ASCII characters"
            
        return True, None
        
    except Exception as e:
        return False, f"Error checking message safety: {str(e)}" 