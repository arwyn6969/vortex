# Architecture

The maintained game is a static Vite/TypeScript application. Rendering, saved state, art, dialogue, and proof verification run in the browser. A server is only needed to deliver static files. The default Python command is a small standard-library static server, not the old simulation engine.

## Source of truth

`vortex/src/mythology/correspondences.py` and `paths.py` own the ten offices and twenty-two edges. `tools/generate_lattice.py` exports a deterministic JSON table. `npm run check:lattice` fails when that export drifts. Change the Python canon first, regenerate, and commit the JSON.

`vortex/web/lattice.ts` provides typed graph helpers. `session.ts` is a pure transition reducer: validate an action, clone the world, advance its revision, and apply its effects. An invalid move cannot consume a turn or modify the original state. Content does not control movement, wallet verification, or rewards.

`content.ts` owns the authored scenes, guide voices, and rites. `stories.ts` owns ten token-specific errands and their outcomes; `story-view.ts` renders the encounter, persistent story ledger and festival. `navigation.ts` suggests graph-valid next actions using the same veil and darkness rules as the reducer. Suggestions never teleport or mutate state. `rares.ts` assigns verified assets to temples as fictional associations. The original asset metadata lives in `rarepepe-data.json`; provenance and original-image checksums live in `docs/references/`. The map's underlying Egyptian and other cultural correspondences are unchanged.

## State and persistence

A version-5 world holds the shared clock, temporary edge darkness, selected seeker, and up to twelve seekers. Each seeker has their own visited/looked/rested offices, rites, crossings, Harmony, sigil, journal, ten bounded story records, a festival choice, bounded atlas bookmarks and encounter outcomes, and an optional proof. One rest per office provides a pillar increase; rites cannot be farmed. The Watcher only dims an edge when another legal exit remains. Sit clears the shared darkness.

`storage.ts` reconstructs validated data instead of trusting arbitrary imported objects. It bounds files, records and strings, verifies saved signatures, rejects duplicate identities and conflicting histories, and preserves unreadable data. Writes compare revisions; all UI writers also use `journey-lock.ts` to serialize cooperating tabs with Web Locks. Browsers without Web Locks are read/export-only. Before replacing a valid primary save, persistence writes its previous value to `vortex-last-good`; a quota failure leaves the primary intact. Explicit recovery verifies both primary and backup against the confirmation snapshot, revalidates proofs, preserves the replaced original and advances the revision. Unknown future schemas cannot be downgraded through recovery.

The save is local and user-editable. It is not an anti-cheat system or proof of ownership. No encryption or account recovery is claimed. Export/import is the migration path between browsers; unverified older schemas remain untouched.

## Returning Nile stories and migration

Each story has one source temple and one destination within the existing graph. After the source rite, a seeker chooses one of three approaches. Delivery requires the destination's rite and presence there. A return to the source allows one of three lasting resolutions. The reducer enforces these stages, the three-active-story limit, and one-time completion. Story actions calm hurried walking but do not award pillar points, invent token holdings, or change existing ending requirements.

Return scenes reference rite choices, delivered approaches and completed resolutions; return conversations can quote the meaning of a locally revealed stream. Resolutions persist independently of the eighty-entry journal. Rooted unlocks a second chapter: three resolved stories and four revealed streams allow one of three celebrations at Kingdom. Guest memories derive from the actual resolutions. Later stories remain playable. Changing the sigil clears Rooted, the festival choice and wallet witness while retaining story history.

The storage key stays `vortex-world-v3` to find deployed saves. The parser accepts released schemas 3/4 and current schema 5. Schema 3 gains empty story history and no festival; both older versions gain empty inquiry progress. The app writes schema 5 only on a successful mutation. Missing current fields and impossible encounter prerequisites are errors. Older released clients reject newer payloads instead of stripping unknown history. Unknown old v1 or future formats remain unsupported and are preserved. Fixtures generated from actual releases (`c71650e36e371c2533cfc3baabefd2e230113a14` for v3 and `fe3e6ce43f537422bd5064c0054b8eca096f8098` for v4) verify the original fields survive.

## Living Atlas and inquiries

`atlas.ts` holds bounded entries, source records, aliases, contextual distinctions and separately sourced relationships. Three editorial themes connect figures, texts, practices, narrative archetypes, tarot lenses, real assets and protocols. `atlas-view.ts` renders search, comparison and contextual encounters without a graph-visualization dependency. Search and comparison stay ephemeral; remembered entry IDs persist per seeker.

`inquiries.ts` owns encounter prerequisites and durable outcomes for the tablet, waterline testimony and gate. `session.ts` applies study/inquiry actions through the existing reducer. Reading advances the revision without spending a turn; encounters consume a turn without awarding pillars or changing the ending rules. Persistent memory appears in later scenes independently of the bounded journal. The legacy cultural tables are not imported into this atlas. Editorial scope and remaining cultural review are documented in [LIVING_ATLAS.md](LIVING_ATLAS.md).

## Wallet boundary

`wallet.ts` accepts an address and externally produced signature. The game has no key input or transaction submission path. The challenge binds purpose, Bitcoin mainnet, seeker identity, sigil, address, nonce, issue time and expiry. Changing a sigil removes the old proof. Imported proofs are reverified.

The verifier dependency is loaded on demand. The adapter understands finalized BIP-322 `smp` prefixes and compatible unprefixed simple signatures; it deliberately excludes full transactions, PSBTs, multisig and Taproot script paths. Legacy recoverable signatures are limited to P2PKH. Known valid/invalid vectors come from the [Bitcoin BIPs repository](https://github.com/bitcoin/bips/blob/master/bip-0322/basic-test-vectors.json). Specification: [BIP 322](https://bips.dev/322/).

A stored proof says a message verified for an address at the recorded time. It does not prove current control of funds, token holdings, real-world identity, or exclusive possession of a key. Ordinary play makes no blockchain requests. The separate optional address ledger queries the official Counterparty API only after the user submits an address. The real-token gallery remains a documented build-time snapshot; it never guesses a current balance or price.

## Delivery and accessibility

The main game loads separately from the on-demand signature verifier. Images are local, compressed, and dimensioned. There are no remote font calls. A generated service worker caches the production application and artwork, with cache versions based on emitted file names and public-file content. It leaves cross-origin and non-GET requests alone. An update waits by default; an explicit Update and return action activates it and reloads the requesting tab. The production document's CSP limits script and connection origins and blocks objects, base changes and cross-origin form actions. Inline styles remain allowed for the existing renderer.

The interface uses native buttons/forms/dialogs, keyboard-operated map nodes, visible focus, text exits equivalent to the map, a skip link, reduced-motion support, and sound that starts only after a deliberate choice. Focus is restored after routine redraws and dialog dismissal, the questionnaire and arrivals move focus to their heading, and a persistent live region announces the results of game actions. Mobile navigation can scroll horizontally. Tests run reducers, persistence, cryptographic fixtures, and emulated DOM journeys. They are not a claim of a manual accessibility audit or a real-wallet interoperability audit.

## Read-only address ledger

`counterparty.ts` owns a bounded adapter for Counterparty Core v2 and an ephemeral `CollectionLookup` controller. It validates a mainnet address locally, requests root readiness, pages `addresses/{address}/balances?type=all&verbose=true`, and checks readiness again. Fixed-origin GET requests omit credentials and referrer, reject redirects and bypass the browser cache. A 30-second total deadline, 20-page/2,000-entry cap and 1 MB decoded response cap bound the work. Only full, internally consistent results are published to the interface.

Large JSON integer tokens retain their original decimal digits; quantities are added using BigInt. Address and attached-output rows are keyed independently to detect duplicate pages without omitting UTXO balances. Unknown divisibility remains explicit raw units. Root JSON checks work even when CORS hides the custom readiness headers. Node-height changes, count drift, repeats and incomplete pages ask for a fresh lookup. This is not an atomic blockchain snapshot; upstream caches and reorgs remain possible.

`collection-view.ts` renders balances with source-specific wording and only the existing local artwork for known tokens. Remote metadata is treated as text, never fetched as images or HTML. A character link stages the normal route; it does not create a discovery, rite or token claim. Results are cleared on edit, close, seeker change and page exit. Serial request IDs prevent delayed responses from restoring cleared data. No balance state is added to the World or WebMCP snapshots, and no save-schema migration is needed for 0.4.

## Boundaries for further development

Extend the existing bounded Counterparty adapter for any further chain data; use a separate adapter for future AI dialogue. Never let a model award a rite, change the graph, certify a proof, or claim token ownership. Network errors must leave offline play intact. Keep pending external requests separate from durable game state, and verify live-data readiness, exact quantities and pagination before displaying results.

## Optional browser agent surface

`webmcp.ts` feature-detects `document.modelContext`. It registers a read-only journey snapshot, a public atlas-entry reader and one typed game-action tool. Mutations use the same reducer and save path as the visible UI and require the current seeker and revision. Wallet operations, identity management, journal contents and free-form inputs are excluded. Registration is cleaned up on hot reload and failures do not affect normal play. Contract and integration tests use an emulated registration context. Living Atlas verification also invoked the native tools in the in-app Chromium browser, including valid actions, atlas reads, rejected stale actions and a two-tab same-revision race. Broader native browser interoperability remains unverified. This optional surface does not affect ordinary play.
