"""Bitcoin wallet integration for the game."""

import re
import logging
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
import hashlib
import base58
import requests
from enum import Enum
from datetime import datetime
from .keys import (
    HDWallet,
    create_new_wallet,
    generate_native_segwit_address,
    wif_to_private_key,
    private_key_to_wif,
    check_dependencies,
    COINCURVE_AVAILABLE,
    sign_message,
    verify_message
)
from .taproot import generate_taproot_address, verify_taproot_address, derive_taproot_keys

if COINCURVE_AVAILABLE:
    import coincurve

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KeyFormat(Enum):
    """Supported Bitcoin private key formats."""
    WIF_UNCOMPRESSED = "WIF Uncompressed"
    WIF_COMPRESSED = "WIF Compressed"
    HEX = "Hexadecimal"

class AddressType(Enum):
    """Supported Bitcoin address types."""
    LEGACY = "Legacy (P2PKH)"  # 1...
    SEGWIT_NESTED = "Nested SegWit (P2SH-P2WPKH)"  # 3...
    SEGWIT_NATIVE = "Native SegWit (P2WPKH)"  # bc1q...
    TAPROOT = "Taproot (P2TR)"  # bc1p...

@dataclass
class WalletInfo:
    """Information about a Bitcoin wallet."""
    address: str
    address_type: AddressType
    private_key: Optional[str] = None
    balance: float = 0.0
    network: str = "mainnet"  # mainnet or testnet
    last_balance_check: Optional[datetime] = None
    transaction_history: Optional[List[Dict]] = None
    mnemonic: Optional[str] = None
    derivation_path: Optional[str] = None

class BitcoinWallet:
    """Handles Bitcoin wallet operations."""
    
    # Network-specific constants
    MAINNET_PREFIXES = {
        "WIF_UNCOMPRESSED": "5",
        "WIF_COMPRESSED": "K",
        "P2PKH": "1",
        "P2SH": "3",
        "BECH32": "bc1q",
        "BECH32M": "bc1p"  # Taproot prefix
    }
    
    TESTNET_PREFIXES = {
        "WIF_UNCOMPRESSED": "9",
        "WIF_COMPRESSED": "c",
        "P2PKH": "m",
        "P2SH": "2",
        "BECH32": "tb1q"
    }
    
    # Bitcoin-specific constants
    SATOSHIS_PER_BTC = 100000000
    MAX_PRIVATE_KEY = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    
    # Message templates for common verification scenarios
    MESSAGE_TEMPLATES = {
        'profile': "I own the Bitcoin address {address} at {timestamp}",
        'session': "Verifying session ownership of {address} at {timestamp}",
        'challenge': "Completing challenge {challenge_id} from address {address} at {timestamp}",
        'token': "Verifying ownership of token {token_id} at address {address}"
    }
    
    def __init__(self, debug_mode: bool = False):
        """Initialize the wallet handler with optional debug mode."""
        self.debug_mode = debug_mode
        if debug_mode:
            logger.setLevel(logging.DEBUG)
        
        # Check dependencies
        deps_ok, error = check_dependencies()
        if not deps_ok:
            logger.error(f"Wallet initialization failed: {error}")
            self.deps_error = error
        else:
            self.deps_error = None

    @classmethod
    def detect_address_type(cls, address: str) -> Tuple[Optional[AddressType], Optional[str]]:
        """
        Detect the type of Bitcoin address.
        Returns (address_type, error_message).
        """
        try:
            # Basic validation
            if not address:
                return None, "Invalid address: empty string"
            
            # Minimum lengths for different address types
            MIN_LENGTHS = {
                "P2PKH": 26,  # Legacy
                "P2SH": 34,   # Nested SegWit
                "BECH32": 42,  # Native SegWit
                "BECH32M": 62  # Taproot
            }
            
            # Check testnet first
            if any(address.startswith(prefix) for prefix in cls.TESTNET_PREFIXES.values()):
                return None, "Testnet addresses not supported"
            
            # Check each address type with length validation
            if address.startswith(cls.MAINNET_PREFIXES["P2PKH"]):
                return (AddressType.LEGACY, None) if len(address) >= MIN_LENGTHS["P2PKH"] else (None, "Invalid address: too short for P2PKH")
            elif address.startswith(cls.MAINNET_PREFIXES["P2SH"]):
                return (AddressType.SEGWIT_NESTED, None) if len(address) >= MIN_LENGTHS["P2SH"] else (None, "Invalid address: too short for P2SH")
            elif address.startswith(cls.MAINNET_PREFIXES["BECH32"]):
                return (AddressType.SEGWIT_NATIVE, None) if len(address) >= MIN_LENGTHS["BECH32"] else (None, "Invalid address: too short for Native SegWit")
            elif address.startswith(cls.MAINNET_PREFIXES["BECH32M"]):
                return (AddressType.TAPROOT, None) if len(address) >= MIN_LENGTHS["BECH32M"] else (None, "Invalid address: too short for Taproot")
            
            return None, "Invalid address format"
        except Exception as e:
            return None, f"Invalid address: {str(e)}"
    
    @classmethod
    def validate_private_key(cls, key: str) -> Tuple[bool, Optional[str], Optional[KeyFormat]]:
        """
        Validate a Bitcoin private key format.
        Returns (is_valid, error_message, key_format).
        """
        logger.debug(f"Validating private key format: {key[:8]}...")
        
        # Check hex format (64 characters)
        if re.match(r'^[0-9a-fA-F]{64}$', key):
            # Verify the key is within valid range
            value = int(key, 16)
            if value <= 0 or value >= cls.MAX_PRIVATE_KEY:
                return False, "Invalid private key range", None
            logger.debug("Valid hex format private key")
            return True, None, KeyFormat.HEX
            
        # Check WIF format
        try:
            private_key, is_compressed, is_testnet = wif_to_private_key(key)
            if is_testnet:
                return False, "Testnet keys not supported", None
            key_format = KeyFormat.WIF_COMPRESSED if is_compressed else KeyFormat.WIF_UNCOMPRESSED
            return True, None, key_format
        except ValueError as e:
            return False, str(e), None
    
    @staticmethod
    def get_balance(address: str) -> Tuple[float, Optional[str], Optional[List[Dict]]]:
        """
        Get the balance and transaction history of a Bitcoin address using multiple public APIs.
        Returns (balance, error_message, transaction_history).
        """
        logger.debug(f"Fetching balance for address: {address}")
        
        apis = [
            {
                "name": "blockchain.info",
                "url": f"https://blockchain.info/balance?active={address}",
                "parser": lambda data: data[address]["final_balance"] / BitcoinWallet.SATOSHIS_PER_BTC
            },
            {
                "name": "blockcypher",
                "url": f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance",
                "parser": lambda data: data["balance"] / BitcoinWallet.SATOSHIS_PER_BTC
            }
        ]
        
        # Try to get transaction history
        try:
            txn_response = requests.get(
                f"https://blockchain.info/rawaddr/{address}",
                params={"limit": 10},
                timeout=5
            )
            if txn_response.status_code == 200:
                txn_data = txn_response.json()
                txn_history = txn_data.get("txs", [])
            else:
                txn_history = None
        except Exception as e:
            logger.error(f"Error fetching transaction history: {str(e)}")
            txn_history = None
        
        errors = []
        for api in apis:
            try:
                logger.debug(f"Trying {api['name']} API...")
                response = requests.get(api["url"], timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    balance = api["parser"](data)
                    logger.debug(f"Balance from {api['name']}: {balance} BTC")
                    return balance, None, txn_history
                else:
                    errors.append(f"{api['name']}: HTTP {response.status_code}")
            except Exception as e:
                errors.append(f"{api['name']}: {str(e)}")
                continue
                
        error_msg = f"Failed to fetch balance: {'; '.join(errors)}"
        logger.error(error_msg)
        return 0.0, error_msg, None
    
    @staticmethod
    def create_new_wallet() -> Tuple[WalletInfo, Dict[str, str]]:
        """
        Create a new Bitcoin wallet with BIP39 mnemonic.
        Returns (wallet_info, recovery_info).
        """
        try:
            # Create new HD wallet
            wallet, mnemonic, wallet_info = create_new_wallet()
            
            # Generate Taproot address
            private_key, public_key = derive_taproot_keys(wallet)
            taproot_address = generate_taproot_address(public_key)
            
            # Create WalletInfo object
            info = WalletInfo(
                address=taproot_address,
                address_type=AddressType.TAPROOT,
                private_key=private_key_to_wif(private_key, compressed=True),
                balance=0.0,
                last_balance_check=datetime.now(),
                mnemonic=mnemonic,
                derivation_path="m/86'/0'/0'/0/0"  # BIP86 for Taproot
            )
            
            recovery_info = {
                "mnemonic": mnemonic,
                "derivation_path": "m/86'/0'/0'/0/0",
                "backup_instructions": [
                    "Write down your mnemonic phrase in a secure location",
                    "Never share your mnemonic phrase or private keys",
                    "Keep multiple secure backups of your mnemonic",
                    "This is a Taproot-enabled wallet using BIP86 derivation"
                ]
            }
            
            logger.info("New Taproot wallet created successfully")
            return info, recovery_info
            
        except Exception as e:
            logger.error(f"Error creating wallet: {str(e)}")
            raise
    
    @classmethod
    def process_wallet_input(cls, private_key: Optional[str] = None, signed_message: Optional[Dict] = None) -> Tuple[WalletInfo, str]:
        """
        Process wallet input and return wallet info with status message.
        
        Args:
            private_key: Optional private key in WIF or hex format
            signed_message: Optional dict containing {
                'address': str,
                'message': str,
                'signature': str
            }
        """
        wallet = cls()
        if wallet.deps_error:
            return cls.create_new_wallet()[0], f"Error: {wallet.deps_error}"
            
        if private_key:
            logger.info("Processing provided private key...")
            is_valid, error_msg, key_format = cls.validate_private_key(private_key)
            
            if not is_valid:
                logger.warning(f"Invalid private key: {error_msg}")
                return cls.create_new_wallet()[0], f"Invalid private key: {error_msg}. Creating new wallet..."
                
            try:
                # Convert to raw private key if WIF
                if key_format in [KeyFormat.WIF_COMPRESSED, KeyFormat.WIF_UNCOMPRESSED]:
                    raw_private_key, is_compressed, _ = wif_to_private_key(private_key)
                else:
                    raw_private_key = bytes.fromhex(private_key)
                    is_compressed = True
                
                # Generate public key
                deps_ok, error = check_dependencies()
                if not deps_ok:
                    raise ImportError(error)
                    
                public_key = coincurve.PublicKey.from_secret(raw_private_key).format(compressed=is_compressed)
                
                # Generate native SegWit address
                address = generate_native_segwit_address(public_key)
                
                # Get balance and history
                balance, balance_error, txn_history = cls.get_balance(address)
                
                if balance_error:
                    logger.error(f"Balance check failed: {balance_error}")
                    return WalletInfo(
                        address=address,
                        address_type=AddressType.SEGWIT_NATIVE,
                        private_key=private_key,
                        balance=0.0,
                        last_balance_check=datetime.now()
                    ), f"Wallet validated ({key_format.value}). {balance_error}"
                    
                return WalletInfo(
                    address=address,
                    address_type=AddressType.SEGWIT_NATIVE,
                    private_key=private_key,
                    balance=balance,
                    last_balance_check=datetime.now(),
                    transaction_history=txn_history
                ), f"Wallet validated ({key_format.value}). Current balance: {balance} BTC"
                
            except Exception as e:
                logger.error(f"Error processing private key: {str(e)}")
                return cls.create_new_wallet()[0], f"Error processing private key: {str(e)}. Creating new wallet..."
                
        elif signed_message:
            logger.info("Processing signed message verification...")
            try:
                address = signed_message['address']
                message = signed_message['message']
                signature = signed_message['signature']
                
                # Verify signature
                is_valid, error = wallet.verify_message(address, message, signature)
                if not is_valid:
                    error_msg = error or "Invalid signature"
                    logger.warning(f"Invalid signature: {error_msg}")
                    return cls.create_new_wallet()[0], f"Invalid signature: {error_msg}. Creating new wallet..."
                
                # Get balance and history
                balance, balance_error, txn_history = cls.get_balance(address)
                
                # Detect address type
                addr_type, addr_error = cls.detect_address_type(address)
                if addr_error:
                    logger.error(f"Error detecting address type: {addr_error}")
                    addr_type = AddressType.SEGWIT_NATIVE  # Default to SegWit
                
                return WalletInfo(
                    address=address,
                    address_type=addr_type,
                    private_key=None,  # No private key for signature verification
                    balance=balance if not balance_error else 0.0,
                    last_balance_check=datetime.now(),
                    transaction_history=txn_history
                ), f"Address verified via signed message. Current balance: {balance if not balance_error else 0.0} BTC"
                
            except Exception as e:
                logger.error(f"Error processing signed message: {str(e)}")
                return cls.create_new_wallet()[0], f"Error processing signed message: {str(e)}. Creating new wallet..."
        else:
            logger.info("No wallet credentials provided, creating new wallet...")
            wallet, recovery_info = cls.create_new_wallet()
            return wallet, "New wallet created. Keep your recovery information safe!"
            
    @staticmethod
    def debug_info(wallet: WalletInfo) -> Dict[str, str]:
        """Return debug information about a wallet."""
        return {
            "address": wallet.address,
            "address_type": wallet.address_type.value,
            "network": wallet.network,
            "has_private_key": bool(wallet.private_key),
            "has_mnemonic": bool(wallet.mnemonic),
            "derivation_path": wallet.derivation_path or "N/A",
            "balance": f"{wallet.balance} BTC",
            "last_balance_check": str(wallet.last_balance_check) if wallet.last_balance_check else "Never",
            "transaction_count": len(wallet.transaction_history) if wallet.transaction_history else 0
        } 

    def sign_message(self, message: str, private_key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Sign a message using a private key.
        Returns (signature, error_message).
        """
        try:
            # Validate private key first
            is_valid, error_msg, key_format = self.validate_private_key(private_key)
            if not is_valid:
                return None, f"Invalid private key: {error_msg}"

            # Convert to raw private key
            if key_format in [KeyFormat.WIF_COMPRESSED, KeyFormat.WIF_UNCOMPRESSED]:
                raw_private_key, _, _ = wif_to_private_key(private_key)
            else:
                raw_private_key = bytes.fromhex(private_key)

            # Sign message
            signature = sign_message(raw_private_key, message)
            return signature, None

        except Exception as e:
            error_msg = f"Error signing message: {str(e)}"
            logger.error(error_msg)
            return None, error_msg

    def verify_message(self, address: str, message: str, signature: str) -> Tuple[bool, Optional[str]]:
        """
        Verify a signed message.
        Returns (is_valid, error_message).
        """
        try:
            # Validate address format first
            addr_type, error = self.detect_address_type(address)
            if error:
                return False, f"Invalid address: {error}"

            # Verify signature
            is_valid = verify_message(address, message, signature)
            return is_valid, None

        except Exception as e:
            error_msg = f"Error verifying message: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def verify_messages_batch(self, verifications: List[Dict[str, str]]) -> List[Tuple[bool, Optional[str]]]:
        """
        Verify multiple signed messages in batch.
        
        Args:
            verifications: List of dicts, each containing:
                {
                    'address': str,
                    'message': str,
                    'signature': str
                }
                
        Returns:
            List of (is_valid, error_message) tuples
        """
        results = []
        for v in verifications:
            try:
                address = v.get('address')
                message = v.get('message')
                signature = v.get('signature')
                
                if not all([address, message, signature]):
                    results.append((False, "Missing required fields"))
                    continue
                    
                is_valid, error = self.verify_message(address, message, signature)
                results.append((is_valid, error))
                
            except Exception as e:
                results.append((False, f"Error processing verification: {str(e)}"))
                
        return results

    async def verify_token_ownership(self, address: str, token_id: str, signature: str) -> Tuple[bool, Optional[str]]:
        """
        Verify token ownership through message signing.
        
        Args:
            address: Bitcoin address claiming ownership
            token_id: Token ID to verify
            signature: Signature of the verification message
            
        Returns:
            (is_valid, error_message)
        """
        try:
            # Generate token verification message
            message, error = self.generate_verification_message('token', 
                address=address, token_id=token_id)
            if error:
                return False, error
                
            # Verify signature
            is_valid, error = self.verify_message(address, message, signature)
            if not is_valid:
                return False, error
                
            # Check if address owns the token
            from vortex.tools.check_bitcoin_tokens import check_address
            token_data = await check_address(address, show_all=True)
            
            # Verify token ownership
            if token_id in token_data.get('owned_src20_ticks', set()):
                return True, None
            if token_id in token_data.get('owned_stamps', set()):
                return True, None
                
            return False, "Address does not own the specified token"
            
        except Exception as e:
            error_msg = f"Error verifying token ownership: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    async def verify_token_ownership_batch(self, verifications: List[Dict[str, str]]) -> List[Tuple[bool, Optional[str]]]:
        """
        Verify multiple token ownerships in batch.
        
        Args:
            verifications: List of dicts, each containing:
                {
                    'address': str,
                    'token_id': str,
                    'signature': str
                }
                
        Returns:
            List of (is_valid, error_message) tuples
        """
        results = []
        for v in verifications:
            try:
                address = v.get('address')
                token_id = v.get('token_id')
                signature = v.get('signature')
                
                if not all([address, token_id, signature]):
                    results.append((False, "Missing required fields"))
                    continue
                    
                is_valid, error = await self.verify_token_ownership(address, token_id, signature)
                results.append((is_valid, error))
                
            except Exception as e:
                results.append((False, f"Error processing verification: {str(e)}"))
                
        return results

    def generate_verification_message(self, template_type: str, **kwargs) -> Tuple[str, Optional[str]]:
        """
        Generate a standardized verification message using templates.
        
        Args:
            template_type: Type of message template to use
            **kwargs: Template variables to fill
            
        Returns:
            (message, error)
        """
        try:
            if template_type not in self.MESSAGE_TEMPLATES:
                return None, f"Unknown template type: {template_type}"
                
            # Add timestamp if not provided
            if 'timestamp' not in kwargs:
                kwargs['timestamp'] = datetime.now().isoformat()
                
            message = self.MESSAGE_TEMPLATES[template_type].format(**kwargs)
            return message, None
            
        except KeyError as e:
            return None, f"Missing required template variable: {str(e)}"
        except Exception as e:
            return None, f"Error generating message: {str(e)}" 