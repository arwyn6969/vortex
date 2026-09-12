# The enduring mark: research and integration

Reviewed 12 September 2026. This is the source record for the teaching in `vortex/web/stamps.ts`, not a new spiritual doctrine or a claim about token value.

## Place in VORTEX

The existing [lattice doctrine](doctrine/THE_LATTICE.md) explicitly places stamps and SRC-20 in the outer world, creation at Hod, and the Bitcoin ledger at Malkhut. The chamber follows **Hod → Yesod → Malkhut**: a mark is made, given a foundation, then witnessed. This is VORTEX's fictional correspondence. The chamber changes neither the ten offices nor their twenty-two streams.

Each reading separates the authored guide voice, a sourced ledger passage and an optional reflection. The KEVIN reading treats an egregore as a shared story sustained by attention within the fiction. No claim of supernatural agency is presented as a Bitcoin fact. No new token, collectible card or achievement is fabricated.

## Primary sources and limits

- [Mikeinspace's Bitcoin Stamps specification](https://github.com/mikeinspace/stamps/blob/main/BitcoinStamps.md) describes Classic Stamps, their Counterparty numerical assets, original output encoding and reconstruction. It also documents the rule associating the first valid Stamp with an asset and distinguishes OLGA encoding. An ordinary asset description update should not be mistaken for replacement of the original indexed artwork.
- [Reference indexer protocol documentation](https://github.com/stampchain-io/btc_stamps/blob/main/docs/PROTOCOLS.md) distinguishes Classic Stamps, SRC-20 and their activation boundaries. Direct-Bitcoin SRC-20 began at block 793068; Counterparty SRC-20 recognition ended after block 796000. Those are different milestones. The [indexer overview](https://github.com/stampchain-io/btc_stamps) identifies KEVIN as the first SRC-20 token. Current SRC-20 balances therefore require a separate indexer; this release's Counterparty address ledger cannot report them.
- [Stamps storage and security analysis](https://github.com/stampchain-io/btc_stamps/blob/main/docs/whitepaper/security.md) discusses both UTXO retention and the spending exception. The chamber explains resistance to pruning without promising unconditional eternity, guaranteed truth, or perpetual availability of a particular website. It distinguishes stored records from an indexer's interpretation.
- [KEVIN Stamp Saga](https://kevinstamp.com/) supplies the community narrative: 104 matching images beginning with Stamp #4258, described as a ghost in the machine. Its public HTML and referenced frontend content were read because the text-only browser did not expose the rendered story. We attribute this account to the Saga; we did not independently verify the 104 images or their alleged mechanism. The image Stamps and the SRC-20 ticker are not interchangeable asset identifiers.

The original artwork remains untouched. No Kevin image was copied, generated or presented as an original in this release. The chamber links to its source instead.

## All Counterparty assets

The address ledger defaults to all returned assets, retains exact quantities and searches both canonical identifiers and subasset longnames. Rare Pepe is a thematic filter rather than an eligibility list. Classic Stamps can appear under their Counterparty identifiers, but a numeric identifier alone is not enough to label an asset a Stamp.

The archive also prepares explorer links without making network requests. Named assets are normalized to uppercase; complete subasset names preserve case. Existence is checked by xcp.io when a player follows a link. This is a routing aid, not local issuance validation or ownership verification.

The [xcp.io asset-link helper](https://github.com/XCP/explorer/blob/main/apps/web/src/lib/asset-link.ts) and its [asset route](https://github.com/XCP/explorer/blob/main/apps/web/src/app/asset/%5Basset%5D/page.tsx) establish `/asset/{encoded-name}` and case-sensitive longname routing. The explorer's address route is `/address/{encoded-address}`. All current token and address links use xcp.io. Historical artwork-source URLs remain in the provenance records because changing them would misrepresent where those files were obtained.

## Verification

Automated checks cover explorer routing and escaping, numeric and subasset ledger rows, the all-asset default, local filtering without requests, contextual Stamps dialogue, lesson selection and focus, source links, unchanged achievements, and unchanged saves while browsing. The chamber needs no new storage schema. Protocol passages are authored offline content, not a live protocol feed. A native preview inspection also checked the archive, chamber, lesson selection and visible focus without performing game actions or altering the player’s journey. This is a focused UI check, not a full assistive-technology audit.
