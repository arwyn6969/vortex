# Living Atlas · implementation and editorial record

Released scope: 0.6.0. Source notes reviewed 12 September 2026.

## What is playable

The atlas contains **45 entries and 51 connections**: three exploration themes, six narrative archetypes, six tarot lenses, four Egyptian figures, eight Sumerian figures/texts, three Maya entries, three Dogon reference notes, Bitcoin Stamps, the KEVIN Saga and the ten existing Counterparty assets. These categories overlap through explicit relationships rather than a claim that their subjects are equivalent.

Players can search names and aliases, filter by tradition or theme, compare up to three entries, inspect sources and remember entries in a personal notebook. Historical spelling variants retain separate context. Reading does not require a token or a wallet. Only the previously verified ten assets use local original-token artwork; no new token or purported historical image was invented.

The three themes—word/memory/witness, descent/return, and thresholds/reversals—are VORTEX editorial choices. So are the narrative roles and tarot meanings. A **Source account** label identifies an account in a named source, not proof that a supernatural event happened. **Disputed account** preserves an attributed disagreement. **VORTEX interpretation** identifies authored connections. Sources and locators are attached to entries and relationships separately.

### The Disputed Tablet

At Hod, complete the local rite and remember Nisaba and Bitcoin Stamps. Keep both accounts with attribution, publish a provisional reading, or consult the waterline witness at Yesod before choosing a corroborated account. The witness requires Look at Yesod and remembering the Stamps entry. Decisions persist at Hod, affect a return to Yesod and appear in Kingdom's gathering/festival memory.

This is a fictional problem about context and preservation. It compares an ancient writing tradition with a modern storage format without asserting a historical connection between them. See the [Stamps research record](BITCOIN_STAMPS.md) for protocol boundaries and KEVIN attribution.

### The Gate That Remembers

At Netzach, complete the local rite. Negotiate a duty, ask the guardian to cooperate after remembering Neti or the Hero Twins, or call on a friend after keeping both tablet witnesses or completing Mercy's story. The earlier local rite changes the guardian's framing. The outcome remains visible at Netzach and Kingdom; the friendship route also changes Mercy's return scene.

All routes remain optional. Neither encounter changes movement, awards extra pillar points, requires purchases, or alters the existing Rooted/festival requirements. The gate is new frog fiction, not a reenactment of the Popol Vuh or another ritual.

## Source and culture boundaries

The complete source table and passage/object locators live in [atlas.ts](../vortex/web/atlas.ts). The release draws on the Met's Egyptian gallery descriptions; ORACC's Nisaba/Nidaba entry; Oxford ETCSL's *Inana's descent*; the Morgan Library's tarot history; Christenson's *Popol Vuh* translation; the National Museum of the American Indian's ball-player record, including Edgar Suyuc's contribution; the Met's kanaga record; van Beek's Dogon restudy; and the existing Stamps and Counterparty source records.

The Sumerian pack stays with named texts and participants. K'iche' narrative material and a Classic Maya object have separate entries and contexts. The Dogon material is a small reference room with attributed claims and explicit uncertainty, not a complete culture pack. No specialist Maya or Dogon cultural review is claimed. Broader adaptation and ritual material should await that review and additional community perspectives.

The old Python cultural tables are **not a source for this published atlas**. In particular, the broken `ArchetypeManager` API, the “Mayan” Xiuhtecuhtli/Mictlan entries, Sirius certainty and unsupported numerical confidence scores remain quarantined as legacy research leads. The maintained game imports the generated movement canon and the new reviewed atlas independently; it does not wire those experiments into play. See [LEGACY.md](LEGACY.md).

New entries must have a stable ID, a source/locator or an explicit authored classification, contextual limits and reviewed relationships. An existing name or ticker is insufficient evidence for a new lore claim. Asset IDs remain Counterparty mainnet identifiers and explorer links use xcp.io. SRC-20 requires a separate identity and adapter. No museum imagery or additional token art was downloaded for this edition.

## Saves and recovery

The payload is schema 5; the existing `vortex-world-v3` storage key remains stable. Released schema 3 and 4 saves migrate with empty inquiry progress. Schema 5 requires valid inquiry fields and prerequisites. Earlier clients reject the new version rather than dropping its notebook and decisions.

The v4 fixture was generated with the prior release's `finish()` helper while the checkout still matched `fe3e6ce43f537422bd5064c0054b8eca096f8098`, before modifying the reducer. Migration checks remove only the new fields and recover the original fixture exactly.

Before replacing a valid primary save, the previous record is copied to `vortex-last-good`. Quota failure leaves the previous primary intact. Recovery revalidates structure and saved proofs, verifies that neither the primary nor recovery copy changed since confirmation, preserves the replaced original in `vortex-preserved-original`, and advances the revision. Future schemas cannot be downgraded through recovery. Recovery and originals can be downloaded in Journeys; an unreadable save exposes recovery when a valid copy exists.

All UI writers use the same Web Lock, including import, restore and damaged-save reset. Browsers without Web Locks are explicitly read/export-only; a separate localStorage revision check is not presented as atomic locking. The in-app Chromium check exercised two tabs submitting the same revision: one action succeeded, the other was rejected, and the revision increased once.

The secret guard now checks the official English BIP-39 word list for mnemonic-shaped input instead of treating every twelve-word sentence as a seed. The list is sourced from [bitcoin/bips](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt), under [BIP-39's MIT license](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki). Detection is an aid, not a guarantee; there is still no key collection flow, and guide questions stay out of saved state.

## Delivery and verification

Production HTML includes a CSP limiting scripts and connections to the game and the existing Counterparty endpoint. Object loading, base URL changes and cross-origin form submissions are blocked. Inline styles remain allowed for the current rendered styles. This is an app document policy, not a claim about every hosting response header. The service worker continues to wait by default, with an explicit user action to activate an available update. CI action revisions are pinned; monthly dependency-review PRs are configured.

Automated coverage includes all 729 guided placements, all 90 original story pairs, all nine new encounter pairs, v3/v4 migration, invalid inquiry state, recovery and quota failures, inert search content, atlas relationship/source integrity, the actual atlas interface and the expanded native-tool contract. New atlas tools return published content; action tools use the same reducer and revision checks. Wallet details and journal contents remain excluded.

Native in-app Chromium verification used a separately named local test seeker. It covered first-time creation, source/alias search, comparison, remembered entries, tablet resolution, friendship at the gate, Kingdom consequences after reload, two-tab conflicts, a recovery restore and native atlas/tool calls. Responsive checks at 390px and 320px found no horizontal page overflow; the search button retained keyboard focus after searching. Temporary viewport overrides were reset.

The compiled production build was also loaded in a separate local tab. Its DOM exposed the intended CSP, all four landing images loaded, and Update and return switched the displayed script to the exact newly built bundle and removed the waiting-update notice. Activation now observes the worker's state as well as controller changes, covering initially uncontrolled pages. The final local checks passed 50 browser/game tests, 22 maintained Python tests, canonical graph validation, TypeScript, the production build and generated offline-worker/document-policy checks.

Remaining evidence to collect: observed newcomer sessions; VoiceOver/NVDA and actual Safari/Firefox/Android journeys; interrupted browser-process/storage scenarios beyond emulation; and end-to-end update behavior from an already-open released client. These are tracked in the roadmap and are not implied by the checks above.
