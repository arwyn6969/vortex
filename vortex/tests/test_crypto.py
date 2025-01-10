"""Tests for Bitcoin wallet implementation."""

import pytest
from datetime import datetime
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.crypto.wallet import BitcoinWallet, AddressType, KeyFormat, WalletInfo
from src.core.crypto.keys import HDWallet, generate_native_segwit_address, wif_to_private_key
from src.core.crypto.taproot import verify_taproot_address

# Test vectors from BIP39 and known Bitcoin addresses
TEST_VECTORS = {
    "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
    "seed": "5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4",
    "private_key": "L4rK1yDtCWekvXuE6oXD9jCYfFNV2cWRpVuPLBcCU2z8TrisoyY1",
    "address": "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu",
    "taproot_address": "bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr"
}

# Known valid and invalid WIF private keys for testing
VALID_KEYS = {
    "wif_compressed": "L4rK1yDtCWekvXuE6oXD9jCYfFNV2cWRpVuPLBcCU2z8TrisoyY1",
    "wif_uncompressed": "5KYZdUEo39z3FPrtuX2QbbwGnNP5zTd7yyr2SC1j299sBCnWjss",
    "hex": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}

INVALID_KEYS = {
    "too_short": "L4p2b9VAf8k5aU",
    "invalid_checksum": "L4p2b9VAf8k5aUahF1JCJUzZkgNEAqLfq8DDdQiyAprQAKSbu8h0",
    "testnet": "cVt4o7BGAig1UXywgGSmARhxMdzP5qvQsxKkSsc1XEkw3tDTQFpy",
    "invalid_hex": "1234567890abcdef"
}

@pytest.fixture
def wallet():
    """Create a BitcoinWallet instance for testing."""
    return BitcoinWallet(debug_mode=True)

def test_create_new_wallet(wallet):
    """Test creating a new wallet."""
    info, recovery = wallet.create_new_wallet()
    
    assert isinstance(info, WalletInfo)
    assert info.address.startswith(("bc1q", "bc1p"))  # Native SegWit or Taproot
    assert info.address_type in [AddressType.SEGWIT_NATIVE, AddressType.TAPROOT]
    assert info.mnemonic is not None
    assert len(info.mnemonic.split()) in [12, 24]  # Valid mnemonic length
    assert info.derivation_path in ["m/84'/0'/0'/0/0", "m/86'/0'/0'/0/0"]  # BIP84 or BIP86
    
    assert "mnemonic" in recovery
    assert "backup_instructions" in recovery
    assert len(recovery["backup_instructions"]) > 0

def test_validate_private_keys(wallet):
    """Test private key validation."""
    # Test valid keys
    for key_type, key in VALID_KEYS.items():
        is_valid, error, format = wallet.validate_private_key(key)
        assert is_valid, f"Failed to validate {key_type}: {error}"
        assert format is not None
        
    # Test invalid keys
    for key_type, key in INVALID_KEYS.items():
        is_valid, error, format = wallet.validate_private_key(key)
        assert not is_valid, f"Invalid key {key_type} was accepted"
        assert error is not None

def test_address_type_detection(wallet):
    """Test Bitcoin address type detection."""
    test_addresses = {
        # Legacy addresses (P2PKH)
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa": AddressType.LEGACY,  # Genesis block address
        "12c6DSiU4Rq3P4ZxziKxzrL5LmMBrzjrJX": AddressType.LEGACY,  # Block 1 mining reward
        
        # Nested SegWit addresses (P2SH)
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy": AddressType.SEGWIT_NESTED,
        "3BMEXxSvJqiD3JSZjsQXYkA9CCXBf4HeQR": AddressType.SEGWIT_NESTED,
        
        # Native SegWit addresses (P2WPKH)
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4": AddressType.SEGWIT_NATIVE,
        "bc1q34aq5drpuwy3wgl9lhup9892qp6svr8ldzyy7c": AddressType.SEGWIT_NATIVE
    }
    
    for address, expected_type in test_addresses.items():
        addr_type, error = wallet.detect_address_type(address)
        assert addr_type == expected_type, f"Failed to detect {expected_type} for {address}"
        assert error is None, f"Unexpected error for {address}: {error}"

def test_invalid_addresses(wallet):
    """Test detection of invalid addresses."""
    invalid_addresses = [
        "",  # Empty string
        "invalid",  # Invalid format
        "123456",  # Too short for any address type
        "bc1inv",  # Too short for bech32
        "bc1qinvalidchecksum",  # Invalid checksum
        "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",  # Testnet address
        "1",  # Too short for P2PKH
        "3",  # Too short for P2SH
        "bc",  # Too short for any type
    ]
    
    for address in invalid_addresses:
        addr_type, error = wallet.detect_address_type(address)
        assert addr_type is None, f"Should not detect type for invalid address: {address}"
        assert error is not None, f"Should return error for invalid address: {address}"
        assert any(msg in error.lower() for msg in ["invalid", "not supported", "unknown"]), \
            f"Unexpected error message: {error}"

def test_hd_wallet_derivation():
    """Test HD wallet derivation from mnemonic."""
    # Create wallet from test vector
    wallet = HDWallet.from_mnemonic(TEST_VECTORS["mnemonic"])
    
    # Derive first address
    private_key, public_key = wallet.derive_key_pair("m/84'/0'/0'/0/0")
    address = generate_native_segwit_address(public_key)
    
    assert address == TEST_VECTORS["address"], "Derived address doesn't match test vector"

def test_wif_conversion():
    """Test WIF private key conversion."""
    # Test WIF to private key
    private_key, is_compressed, is_testnet = wif_to_private_key(VALID_KEYS["wif_compressed"])
    assert is_compressed
    assert not is_testnet
    
    private_key, is_compressed, is_testnet = wif_to_private_key(VALID_KEYS["wif_uncompressed"])
    assert not is_compressed
    assert not is_testnet
    
    # Test invalid WIF
    with pytest.raises(ValueError):
        wif_to_private_key(INVALID_KEYS["invalid_checksum"])

def test_wallet_input_processing(wallet):
    """Test wallet input processing."""
    # Test with valid private key
    info, msg = wallet.process_wallet_input(VALID_KEYS["wif_compressed"])
    assert isinstance(info, WalletInfo)
    assert info.address.startswith("bc1q")
    assert "validated" in msg.lower()
    
    # Test with invalid private key
    info, msg = wallet.process_wallet_input(INVALID_KEYS["invalid_checksum"])
    assert isinstance(info, WalletInfo)
    assert "invalid" in msg.lower()
    
    # Test with no private key (new wallet creation)
    info, msg = wallet.process_wallet_input()
    assert isinstance(info, WalletInfo)
    assert "created" in msg.lower()

def test_balance_checking(wallet):
    """Test balance checking functionality."""
    # Test with known address (Bitcoin genesis address)
    balance, error, history = wallet.get_balance("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    assert error is None
    assert isinstance(balance, float)
    assert balance >= 0
    
    # Test with invalid address
    balance, error, history = wallet.get_balance("invalid_address")
    assert error is not None
    assert balance == 0.0

def test_debug_info(wallet):
    """Test debug info generation."""
    info, _ = wallet.create_new_wallet()
    debug = wallet.debug_info(info)
    
    assert "address" in debug
    assert "address_type" in debug
    assert "network" in debug
    assert "has_private_key" in debug
    assert "has_mnemonic" in debug
    assert "balance" in debug
    assert isinstance(debug["has_mnemonic"], bool)
    assert isinstance(debug["has_private_key"], bool)

def test_error_handling(wallet):
    """Test error handling in various scenarios."""
    # Test with None input
    with pytest.raises(Exception):
        wallet.validate_private_key(None)
    
    # Test with empty string
    is_valid, error, _ = wallet.validate_private_key("")
    assert not is_valid
    assert error is not None
    
    # Test with invalid hex
    is_valid, error, _ = wallet.validate_private_key("not_hex")
    assert not is_valid
    assert error is not None 

def test_taproot_wallet():
    """Test Taproot wallet creation and functionality."""
    print("\n=== Testing Taproot Wallet ===")
    wallet = BitcoinWallet(debug_mode=True)
    info, recovery = wallet.create_new_wallet()
    
    # Verify Taproot address format
    assert info.address.startswith("bc1p"), "Not a Taproot address"
    assert info.address_type == AddressType.TAPROOT
    assert info.derivation_path == "m/86'/0'/0'/0/0"  # BIP86
    
    # Verify address detection
    addr_type, error = wallet.detect_address_type(info.address)
    assert addr_type == AddressType.TAPROOT
    assert error is None
    
    # Test with known Taproot address
    addr_type, error = wallet.detect_address_type(TEST_VECTORS["taproot_address"])
    assert addr_type == AddressType.TAPROOT
    assert error is None

def test_taproot_address_validation():
    """Test Taproot address validation."""
    valid_addresses = [
        "bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr",
        "bc1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqzk5jj0"
    ]
    
    invalid_addresses = [
        "",  # Empty
        "bc1invalid",  # Invalid format
        "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4",  # SegWit v0
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # Legacy
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # P2SH
    ]
    
    # Test valid addresses
    for address in valid_addresses:
        assert verify_taproot_address(address), f"Failed to validate Taproot address: {address}"
    
    # Test invalid addresses
    for address in invalid_addresses:
        assert not verify_taproot_address(address), f"Should not validate invalid address: {address}" 