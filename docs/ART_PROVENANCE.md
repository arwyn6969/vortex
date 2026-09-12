# Artwork and token provenance

VORTEX uses existing Rare Pepe token names and original artworks. It also uses new AI-assisted scene and character interpretations anchored to those references, as requested by the project owner. These game illustrations are not newly issued Rare Pepe cards.

## Verification

On 2026-09-12, each archive entry was checked with the official [Counterparty Core API](https://apidocs.counterparty.io/) at `/v2/assets/{asset}/`. The responses reported Counterparty height 966706. Collection membership and original image filenames were checked against the Rare Pepe section of [TokenScan's collection index](https://tokenscan.io/js/nfts.js), containing 1774 entries.

[The source manifest](references/counterparty-assets.json) records exact string asset IDs, raw supply, divisibility, first-issuance blocks, source URLs, snapshot date/height, and SHA-256 digests of the unchanged original image bytes. The UI displays supply as a dated snapshot, never as a live quote. A locked issuance does not prevent later token destruction, so current supply can change.

| Original asset | Counterparty asset ID | Original-art reference |
| --- | --- | --- |
| THOTHPEPE | 4028490930754 | [Token record](https://tokenscan.io/asset/THOTHPEPE) |
| GODDESSISIS | 923667659956618 | [Token record](https://tokenscan.io/asset/GODDESSISIS) |
| GODANUBIS | 1366340770358 | [Token record](https://tokenscan.io/asset/GODANUBIS) |
| SPHINXPEPE | 100922331422722 | [Token record](https://tokenscan.io/asset/SPHINXPEPE) |
| PEPEPHARAON | 2142393699931329 | [Token record](https://tokenscan.io/asset/PEPEPHARAON) |
| LORDKEK | 3572240994 | [Token record](https://tokenscan.io/asset/LORDKEK) |
| KEKET | 4646947 | [Token record](https://tokenscan.io/asset/KEKET) |
| RAREPEPE | 136744851026 | [Token record](https://tokenscan.io/asset/RAREPEPE) |
| ZAZENPEPE | 5228453241730 | [Token record](https://tokenscan.io/asset/ZAZENPEPE) |
| PEPEZENMSTR | 2142396759310071 | [Token record](https://tokenscan.io/asset/PEPEZENMSTR) |

Original images live under `vortex/web/public/rarepepe/`. Their visible credits and text are preserved. Original artwork and Pepe character rights remain with their respective creators; the code's license does not relicense those works. No artist endorsement is implied. Reliable artist attribution was not returned for every image, so none has been invented.

## New game illustrations

- `vortex/web/public/nile-world.jpg`: Egyptian temple market with six figures derived from THOTHPEPE, GODDESSISIS, GODANUBIS, SPHINXPEPE, PEPEPHARAON, and LORDKEK.
- `vortex/web/public/nile-guides.jpg`: 3×2 sprite sheet in that same order. The portraits retain the source characters' characteristic beak, wings, jackal head, sphinx anatomy, pharaoh costume, and seated-frog headdress respectively.

Both were generated with the built-in image tool. Five original images were attached; SPHINXPEPE was inspected and described because the tool permits five references. The final scene's chest emblem was changed to a plain jewel. The PNG outputs were encoded as JPEG for delivery; the composition was not changed by that encoding.

[Exact prompts and reference mapping](references/art-prompts.json) make the derivation reviewable. New scenes, dialogue, temple associations and story roles are VORTEX fiction. Original token images are presented separately in the archive with source links. The game does not sell, mint, award, or represent possession of these tokens.
