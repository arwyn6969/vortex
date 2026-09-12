# Improvement plan and release status

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

## Next releases, in order

| Priority | Improvement | Acceptance condition |
| --- | --- | --- |
| 1 | Observed player and accessibility sessions | Watch fresh players on phone and desktop, including keyboard and screen-reader users. Record where they hesitate, verify the new focus and announcement behavior in real browsers, and adjust pacing using those observations. Automated interface coverage is not a substitute for these sessions. |
| 2 | More involved story consequences | Build on the current authored errands with two or three interdependent problems, distinct destination decisions, and a choice-history viewer. Preserve reachable endings and migration from released v4 fixtures. Test combinations rather than relying on one happy path. |
| 3 | Deeper guide conversations | If a server-side model is introduced, require a clear privacy choice, budget/timeout limits, an authored fallback, and evaluations against invented ownership, secret handling, rule manipulation and repetition. Keep game authority in the reducer. |
| 4 | Archive expansion and credits | Add new verified assets only with recorded IDs, source art and verified attribution. Expand the world through encounters inside the ten-office/twenty-two-stream canon. Never guess an artist credit. |
| 5 | Native browser-agent verification | Validate the optional WebMCP registration and action tools in a browser that supports the API. Current tests cover the integration contract in an emulated context only. |

Minting, trading, shared online worlds and external AI calls remain outside the release. The archive is a recorded mainnet snapshot, not a market feed. Genuine older `vortex-save-v1` examples are still needed before that unrelated schema can be migrated safely.
