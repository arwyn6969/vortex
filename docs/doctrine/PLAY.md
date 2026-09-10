# The playable lattice

This is the living game of the doctrine in [THE_LATTICE.md](THE_LATTICE.md).
The CLI still exists. The web layer is how a seeker actually walks.
Suggestions for what to build next live in [NEXT.md](NEXT.md).

## What a session is

1. **Gate** — “Would you like to play a game?” Name. Optional Bitcoin *address* (never a key).
2. **Who arrived** — six questions. They seat you: mercy → Wisdom, severity → Zen, balance → Vibe Temple.
3. **Walk** — only along the 22 streams. Each stream has a Hebrew letter and a title (Aleph, Beth, … Tav). A second walk of the same letter reveals its meaning.
4. **Guides** — classical or folk. They remember rites, sigils, pillars. The Watcher never speaks.
5. **Watcher** — silent director. A stream may go dark for haste (three walks without Sit or Look), pillar tilt, thin presence, or the fourth pond. Sit reopens darkness.
6. **Work** — Look / Sit / a rite in each pond. Hod holds a sigil (language, not a key). Kingdom notes an address.
7. **Harmony** — if Mercy and Severity both stand when you are in Tiferet, the heart records a meeting and **Crown opens**.
8. **Qoph** — Netzach–Malkhut, the back of the head. Veiled until you Look at Boundaries Pond. Tav (Yesod–Malkhut) is the honest descent.
9. **Bound** — sigil + six ponds + four rites + a *signed* address at Kingdom. Suggested next: prove the noted address with a wallet signature. See [NEXT.md](NEXT.md).

## Veils (the lattice doing work)

The graph is not the same as the walk.

| Gate | Stream | Opens when |
|---|---|---|
| Crown | any path *to* Keter | Harmony: both pillars ≥ 0.25 in Tiferet |
| Qoph | Netzach–Malkhut | Look at Netzach |
| Watcher-dark | a neighbor, 2 walks | Sit, or wait it out |

Code: `vortex/src/mythology/veils.py`. Topology stays in `paths.py`. The CLI `Lattice.can_travel` is topological; the playable session applies veils.

## Correspondences (the link)

| Sefirah | Pond | Pillar | Permission |
|---|---|---|---|
| Keter | Crown Pond | balance | look |
| Chokmah | Wisdom Pond | mercy | look |
| Binah | Zen Zone | severity | look |
| Chesed | Mercy Pond | mercy | look |
| Gevurah | Severity Pond | severity | look |
| Tiferet | Vibe Temple | balance | look |
| Netzach | Boundaries Pond | mercy | look |
| Hod | Meme Studio | severity | create |
| Yesod | Harmony Pond | balance | create |
| Malkhut | Kingdom Pond | balance | ledger |

Streams: `vortex/src/mythology/paths.py` (22 letters). Ledger floor: Kingdom only.

## Staircase still open

Full suggestions: [NEXT.md](NEXT.md). Short list:

- Sign the Malkhut challenge from a wallet. Never ingest WIF. That completes Bound.
- Mint the Hod sigil as STAMPS / SRC-20 from the player's wallet, then read it back only at Kingdom.
- Watcher as a hidden referee model (no chat surface).
- More than one seeker on the same tree (local profiles, shared veils, personal Harmony).
- Wire the CLI `Game` loop to the lattice, or freeze it and let the web kernel be source of truth.
