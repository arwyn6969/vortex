# VORTEX · The Nile of Rare Frogs

An Egyptian frog adventure rooted in real Rare Pepe tokens on Counterparty. Consult a questionable ibis, negotiate with a crocodile, tune the solar boat, and carry a mark of your own through ten temples and twenty-two streams.

![The Nile temple, reimagined from existing Rare Pepe artwork](vortex/web/public/nile-world.jpg)

## Play locally

Use Node.js 22.18 or later (Node 22 LTS recommended).

```sh
npm ci
npm run dev
```

Open the local address printed by Vite. Choose a name and answer six short questions. No account, wallet, API key, Python environment, or paid service is needed.

For a production build:

```sh
npm run build
npm run preview
```

Alternatively, after building, Python 3.11+ can serve the game without third-party packages:

```sh
python3 run_game.py --open
```

## The walk

- **Walk** along a connected stream. A first crossing reveals its name; a return reveals its meaning.
- **Look** to uncover each temple's details, rite, and original Rare Pepe artwork.
- **Sit** to clear shared darkness. The first rest at each temple strengthens your pillars.
- **Perform a rite** and choose how your frog responds to a small, strange problem.
- Bring Mercy and Severity to 25% each at Vibe Temple to reveal Crown. Look at Boundaries to reveal Qoph.
- At Meme Studio, complete the rite and write a sigil. Visit six temples and complete four rites, then **Root** your journey at Kingdom.
- **Follow a story.** After a temple rite, its Rare Pepe has an errand for you. Carry it to another temple, complete that local rite, make the delivery, then return and decide what changes. Carry up to three unfinished stories.
- **Celebrate Chapter II.** Bring three stories home and reveal four streams, then return to Kingdom for a Nile festival. Choose the long table, the river of lanterns, or the unfinished chorus. The guests remember your choices.
- The **next-step guide** above the scene suggests a useful action or one legal crossing. Select a story in **Stories** to follow its route; you remain free to explore.

The Returning Nile edition (0.3) includes ten branching token-specific stories, persistent return scenes, three festival endings, ten distinct rites, classical and folk voices, a stream Codex, an illustrated Rare archive, a journal, and up to twelve independent seekers on one local tree. The Watcher changes the water silently; each seeker's rites and Harmony remain their own.

## Real Rare Pepes, honest provenance

The archive uses **THOTHPEPE, GODDESSISIS, GODANUBIS, SPHINXPEPE, PEPEPHARAON, LORDKEK, KEKET, RAREPEPE, ZAZENPEPE, and PEPEZENMSTR**. Their asset IDs, issuance blocks, divisibility, and supply snapshots were checked against the Counterparty mainnet API. The original images are preserved, and every card links to its token record.

The new temple scene and character portraits are interpretations of those existing artworks. VORTEX does not invent or issue Rare Pepe tokens. Finding a card in the game records a discovery; it does not transfer ownership. See [art provenance](docs/ART_PROVENANCE.md) and the [verified records](docs/references/counterparty-assets.json).

## Your saves and optional wallet witness

Journeys are saved in this browser, in the existing `vortex-world-v3` storage slot with a version-4 payload. Saves from the released Nile version 3 load automatically, preserving the original journey; the next successful action saves the upgraded format. Older copies of the game reject version 4 rather than silently deleting its story history. Close older game tabs when updating. Export them from **Journeys** before clearing browser data or moving devices. Imports validate the file and merge new seekers; conflicting histories require an explicit choice instead of silently replacing progress. Unreadable saves can be downloaded before starting over. Older hosted `vortex-save-v1` files are not automatically migrated.

The production build caches the game and its artwork for return visits offline after the first successful load. Clearing site data removes both saves and offline files. Private hosting may still require an online sign-in. Exporting remains the portable backup.

A wallet is optional. At Kingdom, a completed seeker may sign a ten-minute, seeker-specific message in their own wallet and paste back its signature. Verification happens locally. Supported proofs are BIP-322 simple for native SegWit and Taproot key paths, and legacy message signatures for P2PKH. Multisig, script paths, full transactions, and PSBTs are excluded. No keys, seed phrases, payments, minting, transactions, or live balance queries are part of this release.

Guide replies are authored and selected by context. Questions are neither retained nor sent to an AI service. Local saves are not encrypted, and local achievements are not external credentials.

## Development and checks

```sh
npm run check:lattice  # generated browser data matches the Python canon
npm run check          # game, interface, save and signature tests; typecheck; build
python3 -m pip install '.[test]'
python3 -m pytest      # maintained Python kernel and launcher regressions
```

The automated game walk covers both chapters from all **729** questionnaire combinations, all 90 outward/return story-choice combinations, all three festival endings, and a 3,000-turn randomized walk. A fixture produced by the actual prior release checks the save upgrade; emulated interface tests cover tracking, deliveries, return choices, focus, announcements and the festival. Signature tests include Bitcoin's published BIP-322 vectors. GitHub Actions runs the maintained checks on pushes and pull requests.

- [Architecture and maintenance](docs/architecture.md)
- [Improvement plan and release status](docs/ROADMAP.md)
- [The lattice doctrine](docs/doctrine/THE_LATTICE.md)
- [Session doctrine](docs/doctrine/PLAY.md)
- [Original development backlog](docs/doctrine/NEXT.md)
- [Legacy Python experiments](docs/LEGACY.md)

The tree is still ten offices and twenty-two streams. The new Egyptian story and token associations are fiction, not spiritual instruction or claims of utility from the original artists.
