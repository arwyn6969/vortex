# Architecture

The maintained game is a static Vite/TypeScript application. Rendering, saved state, art, dialogue, and proof verification run in the browser. A server is only needed to deliver static files. The default Python command is a small standard-library static server, not the old simulation engine.

## Source of truth

`vortex/src/mythology/correspondences.py` and `paths.py` own the ten offices and twenty-two edges. `tools/generate_lattice.py` exports a deterministic JSON table. `npm run check:lattice` fails when that export drifts. Change the Python canon first, regenerate, and commit the JSON.

`vortex/web/lattice.ts` provides typed graph helpers. `session.ts` is a pure transition reducer: validate an action, clone the world, advance its revision, and apply its effects. An invalid move cannot consume a turn or modify the original state. Content does not control movement, wallet verification, or rewards.

`content.ts` owns the authored scenes, guide voices, and rites. `rares.ts` assigns verified assets to temples as fictional associations. The original asset metadata lives in `rarepepe-data.json`; provenance and original-image checksums live in `docs/references/`. The map's underlying Egyptian and other cultural correspondences are unchanged.

## State and persistence

A version-3 world holds the shared clock, temporary edge darkness, selected seeker, and up to twelve seekers. Each seeker has their own visited/looked/rested offices, rites, crossings, Harmony, sigil, journal, and optional proof. One rest per office provides a pillar increase; rites cannot be farmed. The Watcher only dims an edge when another legal exit remains. Sit clears the shared darkness.

`storage.ts` reconstructs validated data instead of trusting arbitrary imported objects. It bounds files, records and strings, verifies saved signatures, rejects duplicate identities and conflicting histories, and preserves unreadable data. Writes compare revisions, while the UI uses the Web Locks API to serialize cooperating tabs when available. Browsers without Web Locks still detect stale revisions, but localStorage alone cannot provide a transaction across a simultaneous read/write race. Use one active tab on those browsers.

The save is local and user-editable. It is not an anti-cheat system or proof of ownership. No encryption or account recovery is claimed. Export/import is the migration path between browsers; unverified older schemas remain untouched.

## Wallet boundary

`wallet.ts` accepts an address and externally produced signature. The game has no key input or transaction submission path. The challenge binds purpose, Bitcoin mainnet, seeker identity, sigil, address, nonce, issue time and expiry. Changing a sigil removes the old proof. Imported proofs are reverified.

The verifier dependency is loaded on demand. The adapter understands finalized BIP-322 `smp` prefixes and compatible unprefixed simple signatures; it deliberately excludes full transactions, PSBTs, multisig and Taproot script paths. Legacy recoverable signatures are limited to P2PKH. Known valid/invalid vectors come from the [Bitcoin BIPs repository](https://github.com/bitcoin/bips/blob/master/bip-0322/basic-test-vectors.json). Specification: [BIP 322](https://bips.dev/322/).

A stored proof says a message verified for an address at the recorded time. It does not prove current control of funds, token holdings, real-world identity, or exclusive possession of a key. No blockchain request occurs during play. The real-token gallery uses a documented build-time snapshot; it never guesses a live balance or price.

## Delivery and accessibility

The main game is a small initial JavaScript bundle; signature code loads separately. Images are local, compressed, and dimensioned. There are no remote font calls. A generated service worker caches the production application and artwork, with cache versions based on emitted file names and public-file content. It leaves cross-origin and non-GET requests alone. An update waits for old tabs to close before taking over, avoiding changes to a running game.

The interface uses native buttons/forms/dialogs, keyboard-operated map nodes, visible focus, text exits equivalent to the map, a skip link, reduced-motion support, and sound that starts only after a deliberate choice. Tests run reducers, persistence, cryptographic fixtures, and an emulated DOM journey. They are not a claim of a manual accessibility audit or a real-wallet interoperability audit.

## Boundaries for further development

Use adapters for any future live Counterparty data or AI dialogue. Never let a model award a rite, change the graph, certify a proof, or claim token ownership. Network errors must leave offline play intact. Keep pending external requests separate from durable game state, and verify live-data readiness, exact quantities and pagination before displaying results.
