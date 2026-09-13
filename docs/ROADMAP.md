# Improvement plan and release status

The current forward plan is [VORTEX: hardening, the Living Atlas, and a larger mythic world](NEXT_PHASE_PLAN.md), reviewed against Enduring Mark on 12 September 2026. It includes code findings, research sources, cultural-pack scope and release gates.

The subsequent [game/UI review](GAME_REVIEW_2026-09-12.md) compares the implemented Living Atlas release with the original plans, records new defects and local fixes, and orders the remaining completion work. Its changes are verified locally and await release.

## Local review improvements awaiting release

The [host backup follow-up](GROK_HOST_FOLLOWUP_2026-09-13.md) recovers all ten temple stills into the shared game and fixes host-only optional feedback and request boundaries. Both repositories are ready for the final Grok build/republish step; the public URL still served an older schema-4 build at the latest check.

The [13 September repository/hosting review](REPOSITORY_REVIEW_2026-09-13.md) integrates Grok's authored water, contextual map labels and movement/audio feedback, with fixes for audio restarting after Off, delayed highlights and feedback leaking between seekers. A shared mount/cleanup API supports the Grok wrapper without duplicate startup code. Verification passes 76 browser/game tests and 22 Python tests, plus native Chromium and production offline checks. See [the current handoff](CONTINUE.md) for the unexported Grok-only assets and server code. GitHub integration does not publish either hosted copy.

Chapter progress beside the next action; temple-specific scene framing and original cards; visible choice inscriptions; earlier rite controls; optional encounter disclosure; reduced duplicate aftermath; seeker draft isolation; complete/consistent Atlas results; onboarding and keyboard-focus repairs; tablet/narrow-screen reflow; and content-sensitive offline cache versions. Verification reached both chapters in Chromium, passed 55 browser/game and 22 Python tests, checked 48 view/width combinations and exercised production offline save/resume. See the review for limits and acceptance criteria.

The follow-on [gameplay pass](GAMEPLAY_PASS_2026-09-12.md) adds the solar boarding puzzle, a returning cook's help, saved-choice scene props, one compass route, persistent session reading places and a compact sticky navigation. Verification now passes 62 browser/game tests, all 48 boarding arrangements, released-v5 compatibility in both directions and an offline production puzzle journey. A [five-player worksheet](PLAYTEST_WORKSHEET.md) is ready; human observations and the remaining browser/release checks are still pending.

## Delivered in the Nile edition

1. **A complete playable release.** Browser entry, six-question placement, connected movement, ten authored rites, named/revealed streams, Harmony, Qoph, sigil creation, wallet-free completion, continued exploration.
2. **The Egyptian Rare Pepe world.** Ten verified Counterparty assets and original artworks; a populated Nile scene and six illustrated guide interpretations based on actual token references; a more playful script with distinct temple problems. No fabricated tokens or pretend ownership.
3. **Reliable personal journeys.** Twelve local seekers, personal rites and discoveries, shared temporary darkness, bounded journals, strict saves, export/import, conflict handling, corrupt-save recovery, and production offline caching.
4. **An optional verified witness.** Context-bound, expiring wallet challenges; local signature checks; saved-proof verification; no private-key collection or chain transactions.
5. **A maintainable baseline.** Generated graph data, strict TypeScript, interface and full-journey tests, Bitcoin reference vectors, CI, a small Python launcher, and corrected legacy engine/placement/alias defects. The old scientific/AI experiments are explicitly outside the release runtime.

## Delivered in Returning Nile (0.3)

1. **Ten token-specific adventures.** Every verified asset now has a distinct errand with three outward choices, a delivery at another temple and three lasting return decisions. The original token art remains inspectable; no invented token or token transfer is involved.
2. **Places remember.** Earlier rite choices shape the encounter text, deliveries change the destination, and return decisions change the home temple. Revealed local streams echo in the return conversation. The Stories ledger keeps these consequences after the bounded journal rolls over.
3. **A second chapter and three endings.** Rooted seekers prepare a Nile festival by resolving three stories and revealing four streams. The long table, river of lanterns and unfinished chorus each include memories of the choices made. Further exploration stays open.
4. **Practical player guidance.** A next-step guide offers a useful action or one legal crossing. Players can follow a chosen story; the guide handles Crown, Qoph and temporary darkness. Story tracking, topical guide prompts, focus restoration, live action announcements and a mobile navigation overflow treatment reduce friction.
5. **A tested save upgrade.** The actual prior release supplies the v3 compatibility fixture. Schema 4 retains old progress and rejects missing or impossible story data; old clients cannot silently strip new story history. Tests cover all 729 guided two-chapter journeys, all 90 story branch pairs, each festival, save/import boundaries and an emulated interface journey.

## Delivered in Address Ledger (0.4)

1. **Opt-in real balances at Kingdom.** An address-only lookup reads the official Counterparty API, with a game-token view, all-token view, original artwork for archive matches and links into the existing stories. Looking up an address grants no ownership claim or progress and is never required for either chapter.
2. **Exact, bounded data.** Cursor pagination includes address and attached-output balances. Raw integer values stay exact, missing metadata stays explicit, and errors, response limits, changing pages and unready nodes never produce a pretend zero or partial total.
3. **An ephemeral network boundary.** Requests omit cookies/referrer and have a deadline. Editing, closing, cancelling or changing seekers invalidates older responses. Addresses and holdings never enter saved journeys, exports, guide questions or browser-agent snapshots. A live public example confirmed five-page retrieval of 428 entries; automated checks cover failure and privacy boundaries.

## Delivered in Enduring Mark (0.5)

1. **An open Counterparty archive.** All reported assets are visible by default, with local name/identifier/subasset search and an optional Rare Pepe filter. Any asset can be followed into xcp.io from the archive; no ownership is required. All current asset and address links use xcp.io, including source-record links.
2. **Bitcoin Stamps in the doctrine's own places.** A three-reading chamber at Hod, Yesod and Malkhut links making, foundation and public memory. Classical and folk voices, optional reflections and contextual guide replies preserve the Egyptian frog setting. The chamber is also available from the archive.
3. **KEVIN with attributed lore and protocol clarity.** The Saga's community narrative is linked and distinguished from technical evidence. Classic Counterparty Stamps and modern SRC-20 holdings stay distinct. Source notes explain the boundaries of immutability and the limits of the current ledger.

## Delivered in Living Atlas (0.6)

1. **A connected mythology atlas.** Forty-five sourced or explicitly interpretive entries, fifty-one relationships, name/alias search, tradition/theme filters, three-way comparison, source explanations and a saved personal notebook. Includes six archetypes, six tarot lenses, Egyptian and Sumerian material, specifically contextualized Maya entries, a bounded Dogon reading room and authentic Counterparty references.
2. **Two consequential encounters.** The Disputed Tablet and The Gate That Remembers offer different routes, conditional help and lasting scenes at other temples and Kingdom. Choices survive reload and journal rollover while the ten-office/twenty-two-stream movement rules stay stable.
3. **Recovery and migration.** Schema 5 preserves released v3/v4 journeys. A previous-save copy, explicit restore, retained damaged originals and write serialization improve resilience. Unsupported browsers are read/export-only instead of risking concurrent writes.
4. **Specific hardening.** Benign prose no longer fails word-count-only secret checks. Production document policy, explicit update activation, pinned CI actions and dependency-review configuration tighten delivery boundaries.
5. **Native checks.** In-app Chromium exercised the new encounters, reload, recovery, small-screen reflow and same-revision two-tab actions. Native atlas reading and valid/stale action handling were verified. See [the implementation and editorial record](LIVING_ATLAS.md) for exact scope and remaining checks.

## Next work, informed by this release

| Priority | Improvement | Acceptance condition |
| --- | --- | --- |
| 1 | Observed play and broader browser/accessibility evidence | Watch fresh players and test assistive technology, Safari/Firefox/Android, interrupted writes and an update from an open released client. Preserve released v5 progress. |
| 2 | Consequence clarity and cultural review | Test whether players notice the new later scenes and understand source/interpretation labels. Obtain specialist feedback for broader Maya/Dogon adaptation; the current reference notes explicitly lack that review. |
| 3 | Deeper culture packs and tarot | Expand the contextualized Sumerian/Maya encounters and tarot toward twenty-two entries after feedback. Keep disputed claims attributed and the ten-office/twenty-two-stream travel map stable. |
| 4 | Open asset curation and world response | Any Counterparty asset remains eligible. Distinguish balance discovery, reviewed atlas membership and authored stories. Keep xcp.io links, verified identifiers and art provenance; add selected props and reactions that make choices visible. |
| 5 | Delivery verification | Native reading and mutation/conflict handling are verified in the in-app browser. Broaden browser coverage and inspect effective hosting headers; test update/rollback behavior without downgrading newer saves. |

Deeper authored guide memory comes before external AI dialogue. If a model is later introduced, require explicit privacy choices, bounded cost/time, an authored fallback and evaluations; the reducer retains game authority.

Minting, trading, shared online worlds and external AI calls remain outside the release. Curated token references are a recorded mainnet snapshot; the optional address ledger reads balances, not a market feed. Genuine older `vortex-save-v1` examples are still needed before that unrelated schema can be migrated safely.
