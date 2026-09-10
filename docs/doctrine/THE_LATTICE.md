# The Lattice

Vortex is one engine wearing several liturgies.

The engine is the Tree of Life. Ponds are sefirot. Streams are the 22 paths.
Guides are dialects of the same office. The Watcher is the unspoken director.
Bitcoin is Malkhut: the place spirit becomes a public record.

This document is doctrine, not a feature backlog. Code should obey it.

## Four stacked worlds

```
Inner   psyche, questionnaire, authenticity, pillars
Middle  guides (classical + folk), challenges, teaching
Hidden  The Watcher, directives, auditors (never chatty)
Outer   names, signatures, stamps, SRC-20, sacred sites, sky
```

A player walks the inner world. A guide speaks in the middle world.
The Watcher retunes from the hidden world. The chain remembers in the outer world.

Do not let Crown ask for a key. Do not let Meme Studio pretend to be Keter.
Do not let a talking guide also be the rules engine.

## The tree is the map

Three pillars:

- Mercy: Chokmah, Chesed, Netzach
- Severity: Binah, Gevurah, Hod
- Balance: Keter, Tiferet, Yesod, Malkhut

Canonical zone assignments live in `vortex/src/mythology/correspondences.py`.
The 22 undirected streams live in `vortex/src/mythology/paths.py`.
`go` may only travel a defined path. Streams *are* those paths.

## Veils

The graph is not the same as the walk.

- **Crown** is unnamed until Mercy and Severity both stand in Tiferet. Then Gimel (and Aleph, Beth) may be walked.
- **Qoph** (Netzach–Malkhut) is the back of the head. It lights when the seeker Looks at Netzach. Tav (Yesod–Malkhut) remains the honest descent.
- The Watcher may **darken** a stream for haste, pillar tilt, or thin presence. Sit reopens darkness. Veils are unread, not closed.

Session gates: `vortex/src/mythology/veils.py`. Playable walk: [PLAY.md](PLAY.md).

## Dialects

Each sefirah has at least two mouths:

- Classical: Egyptian, Norse, Hopi, etc.
- Folk: Pepe court and internet egregores

Same office. Different register. Profile + player choice picks the dialect,
not a random mashup.

Meme-space is treated as a living mythos seated on Hod / Tiferet / Netzach,
not as trash glued onto Kabbalah.

## The gate

The Voight-Kampff sequence does not decide if the visitor is human.
It asks who arrived.

Humans, bots, and alternate personas are welcome.
Authentic participation is rewarded.
`is_human_probability` is an authenticity organ for The Watcher,
not a banhammer.

## The Watcher

Silent. Universal. No welcome line.

- Records interactions
- Scores pillar drift and authenticity
- Emits directives the face-guide must obey
- Never speaks to the player
- May close a stream. Never chats about why. The world simply changes.

The HR-shaped agent chart is this function in costume.
Clearance is initiation grade. Secret visibility means "does not incarnate as NPC."

## Malkhut / the ledger

Binding to Bitcoin is optional and happens at Kingdom, not at Keter.

Allowed:

- Prove an address by **message signature**
- Read SRC-20 / STAMPS / Counterparty as traces and multipliers
- Treat created stamps as Hod-work written into Malkhut

Forbidden:

- Ingesting WIF, hex keys, or mnemonics into the game process
- Asking for keys in Crown, Wisdom, or any talking-guide prompt
- Making the chain the whole game

Names hold power. Signatures bind names without surrendering the name's key.

## Correspondences

Outer sacred sites and sky alignments are copies of the same diagram.
They decorate and eventually sync. They do not replace the pond graph.

## Creation rights

`CREATE_SCENE` / `CREATE_CHARACTER` unlock after specific sefirot,
not from a generic admin toggle. New leaves must declare which sefirah
they hang from.

## Hospitality

This is syncretic fiction and play, not initiation into a living priesthood.
Be precise about that in player-facing copy. Do not flatten living traditions
into "same energy as Hod." Guest guides stay guest guides.

## Implementation source of truth

| Concern | Module |
|---|---|
| Sefirah ↔ pond ↔ dialects ↔ ledger floor | `vortex/src/mythology/correspondences.py` |
| Placement, path travel, dialect pick | `vortex/src/core/lattice.py` |
| Watcher directive vocabulary | `vortex/src/core/watcher_directives.py` |
| 22 streams (letter, title, meaning) | `vortex/src/mythology/paths.py` |
| Session veils (Crown, Qoph) | `vortex/src/mythology/veils.py` |
| Path numbers and older intelligences | `vortex/src/mythology/sefirot.py` |
| How to wire the rest of the repo | `docs/doctrine/STAIRCASE.md` |
| Playable session | `docs/doctrine/PLAY.md` |
| Suggestions after the lattice review | `docs/doctrine/NEXT.md` |
