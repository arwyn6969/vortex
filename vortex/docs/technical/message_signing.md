# Bitcoin Message Signing

## Overview
This document outlines the implementation of Bitcoin message signing and verification functionality in the system. This feature allows users to prove ownership of Bitcoin addresses without exposing their private keys, enhancing security and user experience.

## Features

### Message Signing
- Sign messages using Bitcoin private keys (WIF or hex format)
- Standard Bitcoin message format with magic prefix
- Base64-encoded signature output
- Support for compressed and uncompressed keys
- Deterministic signatures (RFC6979)

### Message Verification
- Verify signed messages against Bitcoin addresses
- Support for multiple address formats:
  - Legacy (P2PKH)
  - Nested SegWit (P2SH-P2WPKH)
  - Native SegWit (P2WPKH)
  - Taproot (P2TR)
- Public key recovery from signatures
- Comprehensive error handling

## Implementation Details

### Message Format
```python
magic_prefix = b"\x18Bitcoin Signed Message:\n"
message_bytes = message.encode('utf-8')
msg = magic_prefix + len(message_bytes).to_bytes(1, 'big') + message_bytes
```

### Signing Process
1. Validate private key format (WIF/hex)
2. Convert to raw private key if needed
3. Format message with Bitcoin prefix
4. Double SHA256 the message
5. Sign using RFC6979 deterministic k
6. Encode signature in base64

### Verification Process
1. Validate address format
2. Decode base64 signature
3. Format message with prefix
4. Recover public key from signature
5. Generate address from public key
6. Compare with provided address

## Usage Examples

### Command-Line Tools

#### Sign Message
```bash
python3 sign_bitcoin_message.py <private_key> "Your message here"
```

#### Verify Message
```bash
python3 verify_bitcoin_address.py <address> "Your message here" <signature>
```

### API Usage

#### Sign Message
```python
wallet = BitcoinWallet()
signature, error = wallet.sign_message("Hello, Bitcoin!", private_key)
if error:
    print(f"Error: {error}")
else:
    print(f"Signature: {signature}")
```

#### Verify Message
```python
wallet = BitcoinWallet()
is_valid, error = wallet.verify_message(address, message, signature)
if error:
    print(f"Error: {error}")
else:
    print(f"Valid: {is_valid}")
```

## Security Considerations

### Private Key Handling
- Never expose private keys in logs or error messages
- Clear private key data from memory after use
- Validate key format before use
- Support only mainnet keys (no testnet)

### Message Validation
- Proper message formatting
- Signature validation
- Address format checking
- Error handling for invalid inputs

### Dependencies
- Uses `coincurve` library for cryptographic operations
- Requires proper dependency management
- Graceful fallback when dependencies unavailable

## Testing

### Test Coverage
- Unit tests for signing and verification
- Test vectors for known message/signature pairs
- Edge cases and error conditions
- Different key and address formats

### Test Cases
- Valid message signing
- Signature verification
- Invalid signatures
- Wrong messages
- Wrong addresses
- Invalid key formats
- Missing dependencies

## Integration Points

### Profile System
- Message signing for profile validation
- Alternative to direct private key input
- Session-based ownership verification
- Dynamic validation challenges

### Security System
- Part of the authentication flow
- Ownership verification mechanism
- Access control validation
- Secure session management

## Future Enhancements

### Planned Features
- Support for custom message prefixes
- Batch signature verification
- Integration with hardware wallets
- Enhanced error messages and user feedback
- Additional address format support

### Integration Points
- Enhanced profile system connection
- Challenge system integration
- Achievement tracking
- Security system enhancements

## References
- [BIP137 - Bitcoin Message Signing](https://github.com/bitcoin/bips/blob/master/bip-0137.mediawiki)
- [BIP322 - Generic Signed Message Format](https://github.com/bitcoin/bips/blob/master/bip-0322.mediawiki)
- [RFC6979 - Deterministic DSA and ECDSA](https://tools.ietf.org/html/rfc6979) 