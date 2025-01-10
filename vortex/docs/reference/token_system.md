# Token System Documentation

## Overview
The token system is a hidden game mechanic that rewards players for their interactions within the game. Players earn tokens through various actions, primarily through keystrokes, with the system remaining hidden until they accumulate enough tokens to discover it.

## Core Features

### Token Earning
- **Base Rate**: 0.001 tokens per keystroke
- **Visibility Threshold**: 100 tokens (system reveals itself after this amount)
- **Rate Limiting**: Maximum 300 keystrokes per minute to prevent abuse
- **Multipliers**: Stack multiplicatively for bonus token earnings

### Transaction Types
- `KEYSTROKE`: Earned from keyboard input
- `CHALLENGE`: Earned from completing challenges
- `MULTIPLIER`: Earned from multiplier events
- `PURCHASE`: Tokens purchased
- `SPEND`: Tokens spent on services
- `SYSTEM`: System-level adjustments

### Balance Management
- Secure transaction handling with database locks
- Prevention of negative balances
- Hidden balances until threshold reached
- Full transaction history tracking

## Achievements

### Discovery
- **Token Discovery**: Hidden achievement for discovering the token system
- **Unlocks at**: 100 tokens accumulated

### Milestones
- **Token Collector**: 1,000 tokens accumulated
- **Token Master**: 10,000 tokens accumulated
- **Token Legend**: 100,000 tokens accumulated

### Special Achievements
- **Multiplier Master**: Have 3+ active token multipliers
- **Keystroke King**: Earn tokens from 10,000 keystrokes
- **Spending Spree**: Spend 5,000 tokens in one transaction
- **Token Efficiency**: Maintain 10 tokens/minute for 5 minutes
- **Daily Dedication**: Earn tokens on 7 consecutive days
- **Token Philanthropist**: Help another user earn their first tokens

## Technical Implementation

### Database Models
- `TokenBalance`: Stores user balances
- `TokenTransactionRecord`: Transaction history
- `TokenMultiplierRecord`: Active multipliers

### Security Features
- Transaction locks prevent race conditions
- Rate limiting on token generation
- Validation against negative balances
- Secure multiplier management

### Integration Points
- Terminal UI keystroke tracking
- Achievement system hooks
- Command system for token info
- Profile system integration

## Commands

### Viewing Token Information
```
tokens
```
Displays:
- Current token balance (if above visibility threshold)
- Recent transactions
- Active multipliers

## API Reference

### TokenService Methods

#### `get_balance(user_id: UUID, include_hidden: bool = False) -> Optional[Decimal]`
Get a user's token balance. Returns `None` if below visibility threshold and `include_hidden` is `False`.

#### `record_keystrokes(user_id: UUID, keystroke_count: int) -> TokenTransactionRecord`
Record keystrokes and award tokens. Includes rate limiting and multiplier calculations.

#### `spend_tokens(user_id: UUID, amount: Decimal, description: str, metadata: Dict = None) -> Optional[TokenTransactionRecord]`
Attempt to spend tokens. Returns `None` if insufficient balance.

#### `add_multiplier(user_id: UUID, name: str, value: Decimal, duration_seconds: Optional[int] = None) -> TokenMultiplierRecord`
Add a token earning multiplier for a user. Optional duration for temporary multipliers.

## Best Practices

### Token Generation
- Use appropriate multipliers for special events
- Consider rate limiting for all token generation methods
- Validate and sanitize all inputs

### Token Spending
- Always check balance before spending
- Use transaction locks for atomic operations
- Include descriptive transaction metadata

### Multiplier Management
- Clean up expired multipliers regularly
- Use reasonable multiplier values
- Consider stacking effects

## Error Handling

### Common Errors
- Insufficient balance for spending
- Rate limit exceeded for keystrokes
- Invalid multiplier values
- Transaction conflicts

### Recovery Procedures
- Automatic rollback of failed transactions
- Cleanup of expired multipliers
- Rate limit cooldown periods 