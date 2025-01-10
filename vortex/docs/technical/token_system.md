# Token System Technical Specification

## Overview
The token system integrates multiple Bitcoin-based token standards to provide a comprehensive rewards and multiplier system. This document outlines the technical implementation and mechanics of token handling within the system.

## Supported Token Types

### 1. SRC-20 Tokens
- Native support for SRC-20 token standard
- Balance tracking and verification
- Special multiplier effects for specific tokens
- Creator attribution and verification

### 2. STAMPS
- Full STAMPS protocol integration
- Balance and ownership verification
- Special multiplier effects for rare stamps
- Creator verification support

### 3. Counterparty Tokens
- Complete Counterparty protocol support
- Asset metadata parsing and validation
- Social media link extraction
- Detailed portfolio analysis
- Category-based token classification

## Message Signing

### Overview
The system supports Bitcoin message signing for secure ownership verification:
- Sign messages using private keys (WIF/hex format)
- Verify signatures against Bitcoin addresses
- Support for multiple address formats
- Command-line tools for signing and verification

### Supported Features
- Standard Bitcoin message format
- Base64-encoded signatures
- Compressed and uncompressed keys
- Deterministic signatures (RFC6979)
- Public key recovery
- Comprehensive error handling

### Integration Points
- Profile validation alternative
- Session-based ownership verification
- Dynamic validation challenges
- Security system integration

### Command-Line Tools
- `sign_bitcoin_message.py` for message signing
- `verify_bitcoin_address.py` for signature verification
- Interactive and non-interactive modes
- Detailed error reporting

## Token Categories

### Category System
```python
CATEGORIES = {
    "PEPE": {"keywords": ["PEPE"], "score_weight": 1.0},
    "BOSHI": {"keywords": ["BOSHI"], "score_weight": 1.0},
    "DANK": {"keywords": ["DANK"], "score_weight": 1.0},
    "FAKE": {"keywords": ["FAKE"], "score_weight": 1.0}
}
```

### Scoring Mechanics
- Each category tracks unique token count
- Progressive status levels based on collection size
- Special titles and achievements for high scores
- Category-specific bonuses and effects

## Multiplier System

### Base Mechanics
- Base rate: 0.001 per keystroke
- Multipliers stack additively
- Special token bonuses
- Creator bonuses for self-issued tokens

### Special Token Multipliers
```python
SPECIAL_SRC20_MULTIPLIERS = {
    "$BALD": 0.42,
    "$VIVA": 0.21,
    "KEVIN": 0.42,
    "DEVIN": 0.33,
    "WOOL": 0.33,
    "LOG": 6.42,
    "MANDY": 1.42,
    "SPICE": 1.42
}

SPECIAL_STAMPS_MULTIPLIERS = {
    "A5433937813514022010": 0.69
}
```

### Creator Bonus System
- +0.33x multiplier per self-created token
- Verified through on-chain creator attribution
- Applies across all supported token types

## Portfolio Analysis

### Asset Information
- Detailed balance tracking
- Historical issuance data
- Holder statistics
- Creation timestamps
- Social media presence

### Metadata Processing
- JSON metadata extraction and parsing
- Media link normalization (IPFS, Arweave, Imgur)
- Social media link extraction
- Description analysis

### Social Platform Support
- Twitter/X handle extraction
- Discord server links
- Telegram groups
- GitHub repositories
- Instagram profiles
- Medium articles

## Implementation Details

### Token Balance Retrieval
```python
async def get_token_balances(address: str) -> List[BitcoinTokenBalance]:
    """
    Fetches comprehensive token balances from multiple sources:
    - SRC-20 endpoints
    - STAMPS network
    - Counterparty API
    Returns normalized balance objects with metadata.
    """
```

### Multiplier Calculation
```python
def calculate_token_multipliers(
    src20_tokens: Set[str],
    stamps: Set[str],
    counterparty_tokens: List[BitcoinTokenBalance],
    creator_token_count: int = 0
) -> Decimal:
    """
    Calculates total multiplier effect from:
    - Special token bonuses
    - Creator bonuses
    - Category achievements
    Returns final multiplier as Decimal.
    """
```

### Category Scoring
```python
def calculate_category_scores(
    counterparty_tokens: List[BitcoinTokenBalance]
) -> TokenCategoryScores:
    """
    Analyzes token portfolio for category scores:
    - PEPE score
    - BOSHI score
    - DANK score
    - FAKE score
    Returns comprehensive scoring object.
    """
```

## API Integration

### Endpoints
- SRC-20: `https://stampchain.io/api/v2/`
- STAMPS: `https://api.stamps.network/v2/`
- Counterparty: `http://api.counterparty.io:4000/api/`

### Rate Limiting
- Implement appropriate backoff strategies
- Cache frequently accessed data
- Batch queries where possible

### Error Handling
- Graceful fallback for API failures
- Multiple endpoint support
- Retry mechanisms for transient failures

## Security Considerations

### Address Validation
- Proper Bitcoin address format validation
- Support for multiple address formats
- Checksums and error detection

### API Security
- HTTPS enforcement
- API key management
- Request signing where required

### Data Validation
- Input sanitization
- Balance verification
- Creator attribution verification

## Future Enhancements

### Planned Features
- Additional token standard support
- Enhanced metadata processing
- Advanced portfolio analytics
- Real-time price feeds
- Achievement system integration

### Integration Points
- Pond system connection
- Profile system integration
- Achievement tracking
- Reward distribution
``` 