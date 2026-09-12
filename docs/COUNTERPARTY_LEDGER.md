# Counterparty address ledger

The optional Kingdom ledger reads reported Counterparty balances for an explicitly submitted public address. The address is not assumed to belong to the player. Its result does not alter rites, discoveries, story progress, wallet proofs, or either ending.

All returned Counterparty assets are shown by default. Named tokens, numeric assets and subassets share the same pipeline; Rare Pepe is an optional view. Searching names or identifiers filters the loaded result locally, with no additional request. Numeric identifiers are not automatically classified as Stamps. SRC-20 holdings require a separate protocol/indexer and are excluded.

## Protocol and sources

Implementation checked 12 September 2026 against:

- [Counterparty Core API reference](https://apidocs.counterparty.io/) and its [OpenAPI document](https://apidocs.counterparty.io/openapi.json), version 11.3.0.
- [Official address-balance query implementation](https://github.com/CounterpartyXCP/counterparty-core/blob/master/counterparty-core/counterpartycore/lib/api/queries.py): `type=all` selects positive address balances and balances whose `utxo_address` matches.
- [Counterparty UTXO specification](https://docs.counterparty.io/docs/advanced/specifications/utxo-support/): balances may contain `utxo` and `utxo_address`.

Requests go only to `https://api.counterparty.io:4000/v2/`. The root JSON provides mainnet, readiness, ledger state and node heights. The balance route uses `limit=100`, `verbose=true`, `type=all`, and the exact returned cursor. No sort or offset is supplied, because those override cursor pagination. No compose, signing, send, price or transaction endpoints are used.

The public service exposed wildcard CORS but did not expose its custom readiness headers to browser JavaScript during inspection. Therefore readiness uses the root response body before and after pagination; a visible false readiness header is also rejected. The service advertised a 60-second edge-cache lifetime. A requested browser cache bypass cannot guarantee that upstream responses are uncached or represent one atomic ledger state.

## Correctness boundaries

- Quantities above JavaScript's safe integer limit are preserved from raw JSON tokens as decimal strings. JSON syntax is checked before transformation. Arithmetic and formatting use BigInt; normalized floating-point quantities are not trusted.
- Address and UTXO rows are validated against the submitted address and combined by asset. Duplicate asset/location rows, repeated cursors, changed row counts, incomplete pages, conflicting metadata and changed node height reject the result.
- Missing divisibility displays raw units instead of an assumed decimal scale. Unknown token descriptions and image URLs are not rendered or fetched. Subasset names are escaped as text; asset links use a fixed xcp.io origin.
- A lookup has a 30-second overall request deadline, 20-page maximum and a 1 MB decoded limit per response. Large collections can be inspected in xcp.io; a partial sum is not shown as a complete balance.
- The lookup reports address and attached-output token balances. It excludes BTC, escrow and unconfirmed changes. Public-node reports are not proof of address control, market valuations, anti-cheat evidence or guaranteed snapshots of a specific block.

## Data lifetime

Submitting the form is the only network trigger. Address checksum validation happens locally first. Fetches use GET with omitted credentials, no referrer, no browser caching and no redirects. There are no background refreshes or automatic retries. The browser-agent tools cannot initiate a lookup or read its results.

Results exist only in memory. Editing the address, cancellation, closing the ledger, changing seekers or leaving the page cancels outstanding work and invalidates its sequence number. A late response cannot repopulate cleared results. The game save remains byte-for-byte unchanged by a lookup or by following a character link from the result.

## Validation evidence

A public example returned by the official THOTHPEPE holder list (`1GQhaWqejcGJ4GhQar7SjcCfadxvf5DNBD`) was used only for a read-only adapter smoke check. The adapter retrieved five pages, 428 entries and 428 distinct assets; the response included one THOTHPEPE. The node reported height 966719. This is dated integration evidence, not a persistent assertion about that address's holdings or owner.

Automated tests exercise exact quantities, attached outputs, missing metadata, unsafe text, full pagination, malformed and duplicate pages, wrong addresses, readiness failures, rate limits, deadlines, oversized responses and cancellation. An emulated interface test verifies opt-in fetching, view switching, character links, unchanged saves, clearing on close and offline error handling. A native browser and assistive-technology audit remains a separate roadmap item.
