# Next — suggestions, not doctrine

Doctrine stays in [THE_LATTICE.md](THE_LATTICE.md).
How a session walks is [PLAY.md](PLAY.md).
How the old CLI climbs is [STAIRCASE.md](STAIRCASE.md).

This file is the living backlog after the 2026 lattice review.
Items here are suggestions. They must still obey the four stacked worlds
and the ledger floor. Do not add ponds. Make the existing 22 streams
and the ten offices do more work.

## Where the game actually is

| Layer | State |
|---|---|
| Doctrine | Written. Correspondences, veils, Watcher silence, Malkhut floor. |
| Kernel (Python) | 22 letters in `paths.py`. Crown / Qoph / haste in `veils.py`. `Lattice` is topological. |
| Kernel (web) | `vortex/web/paths.ts` + `lattice.ts` must stay twins of the Python tables. |
| Playable face | Grok-hosted web session: Gate, seating quiz, 22-letter walk, Codex, crossing overlay, silent Watcher. Save `vortex-save-v1` in localStorage. |
| CLI `Game.start()` | Still a different temple. Wire it to the lattice or freeze it. Do not let it invent a third map. |

The greatest game in this project is not more rooms. It is the
**correspondence engine**: the same ten offices spoken in two dialects,
with veils that change what a second walk means.

## Build next (in this order)

### 1. Bound — name on the floor of the world

Play already *notes* an address at Kingdom. Bound is the rite that
proves it.

- At Malkhut only, issue a one-time challenge phrase.
- Player signs that phrase in their own wallet. Vortex verifies the
  signature. Address + signature live in the save. The key never does.
- Bound condition already written in PLAY: sigil + six ponds + four
  rites + a noted (now signed) address.
- Reuse `tools/sign_bitcoin_message.py`. Do not invent a custodian.

See `SECURITY.md`. If Bound cannot be done without ingesting WIF, skip
the feature.

### 2. Hod sigil as language that touches the chain

Hod creates. Malkhut records.

- The in-game sigil stays language, not a private key.
- Optional outer step: mint that mark as STAMPS / SRC-20 from the
  *player's* wallet, then read the inscription back as a multiplier
  only while the seeker stands at Kingdom.
- Failure mode is a quiet "unread" — never a paste-your-seed dialog.

### 3. Watcher as hidden referee

The Watcher already darkens streams for haste, pillar tilt, and thin
presence. That is the whole public surface.

- A second model may score the turn and emit `WatcherDirective`
  objects. It has no chat UI, no welcome line, no "the Watcher says".
- Face-guides (classical or folk) must obey those directives without
  quoting them.
- Do not merge guide-call and referee-call. Different models, different
  prompts, different logs.

### 4. More than one seeker on the same tree

The graph is shared. Saves are not.

- Two local profiles can occupy different ponds on one tree.
- Streams another seeker darkened stay dark for both until Sit.
- Harmony is personal until Bound; a second seeker cannot open Crown
  for the first by standing in Tiferet.
- No accounts, no server, no social graph. localStorage keys per
  seeker name is enough for the next increment.

### 5. CLI: wire or freeze

`STAIRCASE.md` still lists Game-loop wiring. Pick one:

- **Wire**: `assign_guide` → `Lattice.place` + `GuideFactory.create_for_placement`;
  every turn emits to the Watcher; Pepe constructors match `Guide.__init__`
  before they are registered.
- **Freeze**: keep `run_game.py` as a museum path. The web kernel is the
  playable source of truth. Document that in the CLI banner.

Do not grow a second correspondence table inside the CLI.

## Improve if we continue (play quality)

These are the review notes that are not new features.

- **Save merge** — never rewind Gate progress on rehydrate. Version
  the save (`v3` and up). Reject unknown versions rather than silently
  drop fields.
- **Audio** — unlock on first gesture only. Catch iframe autoplay
  failures. The drone is atmosphere, not a gate.
- **Tree map** — labels must not sit on streams. Veiled Crown is
  unnamed, not missing.
- **Codex** — 22 dashes until walked; meaning only on the second walk
  of that letter. Do not spoil Qoph.
- **Guides** — short. They remember rites and pillars. They do not
  explain the rules. Hospitality copy stays: this is play, not
  priesthood.
- **Harmony math** — keep the threshold readable (both pillars ≥ 0.25
  in Tiferet). Resist adding a dozen hidden stats.

## Potential against the original goals

Read `docs/planning/GOALS.md` as a 2024 wishlist, not as current law.

| Original wish | Lattice reading | Do this? |
|---|---|---|
| Pond / zone / questionnaire | Gate + seating + ten offices | Done. Deepen, do not replace. |
| LLM dialogue | Face-guides in the middle world | Yes, dialect-bound. |
| Bitcoin tokens | Malkhut record, Hod work written down | Yes, as Bound + optional stamp. |
| Community / multiplayer | Several seekers, one tree | Yes, local first. |
| Watcher / HR-shaped director | Hidden referee | Yes, never as a chatbot. |
| Federated learning, GPS, HealthKit, gov ID | Different temple | No. See STAIRCASE non-goals. |
| AR/VR, biometrics, gesture OS | Outer decoration at best | Not until Bound exists. |
| More myth systems as new maps | Dialects of the same ten offices | Translate in, do not fork the graph. |

The original intent that still has the most game in it:

1. One cosmology you can walk.
2. Guides as mouths, not dungeon masters.
3. A silent director that changes the world instead of lecturing.
4. A public name at the bottom of the tree, held without surrendering
   the key.

Everything else is costume.

## Non-goals that stay out

GPS, HealthKit, government ID, social-graph scrape, federated learning,
AR/VR as a prerequisite, purple/gold UI, Watcher chat, pasted private
keys, a twelfth pond.

If a suggestion needs one of those to work, it does not belong here.
