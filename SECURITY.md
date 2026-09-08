# Security

## Ledger floor

Vortex may bind a seeker to a Bitcoin *address* at Kingdom Pond (Malkhut).
It must never take custody of a private key.

Do not:

- Prompt for WIF, hex private keys, or seed phrases
- Log, cache, or write keys into `saves/`, Redis, or SQL
- Call `BitcoinWallet.process_wallet_input` with a raw key from player chat
- Treat a guide transcript as a place to paste secrets

Do:

- Ask for an address
- Ask the player to sign a one-time challenge with their own wallet
- Verify the signature locally
- Read public holdings (SRC-20 / STAMPS / Counterparty) from that address

`IntroSequence.handle_crypto_integration` follows this rule.
`Lattice.assert_ledger_floor` blocks ledger calls off Malkhut.

## Watcher data

The Watcher records in-game events and profile dimensions.
That is enough. Do not attach GPS, biometrics, social graphs, or
government identity to the silent director.

## LLM

Face-guides stream. The Watcher does not.
Neither role should echo secrets from the player.
If a player pastes a key anyway, drop the turn and warn them.
