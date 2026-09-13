# Handoff — feel the lattice

For the next agent if this turn runs out of credit. The playable Grok app mounts `vortex/web` as `src/lib/nile` with a `mount(root)` wrapper in `main.ts`. GitHub `main` at `caabda0` is Living Atlas 0.6 plus the solar crossing.

PRs opened this session (13 Sep 2026):
**GitHub note:** PR https://github.com/arwyn6969/vortex/pull/12 is open. Branch `feel/three-verbs` is pushed (4 commits, 5 files) but GitHub's pull-create API returned 500/502 from this session. Open it from the compare view: https://github.com/arwyn6969/vortex/compare/main...feel/three-verbs?expand=1


- `docs/grok-host` — review scores, five jobs, this handoff, NEXT.md prepend.
- `feel/three-verbs` — authored silent Watcher, feel audio, map juice, short help. Vanilla Vite, no `mount()`, no Grok server fns.

## Status (13 Sep 2026, Grok session)

**Done in the Grok-hosted app:**

- One tree: unused React lattice deleted. Only `NileHost.tsx` remains.
- Map: labels only on current + legal neighbours. Last stream named at midpoint.
- Feel audio: Settings → Ambient sound. Drone leans with pillars. Walk / Look / Sit / first-crossing tones.
- Silent Watcher *felt*: water line under the compass (`haste` / `tilt` / `thin`). Never named.
- Optional “Let the water think”: `consultWatcher` after opt-in, every 4 turns, never on page load. Gameplay darkness stays authored.
- Optional “Speak the guides”: `speakGuide` on Look of `voice(s)` only. Cache. Silence fallback.
- Ten office stills in `public/temples/<id>.jpg`. `templeScene` uses them. Original card after Look.
- Short help. Dialog inset. Gold brand retinted to mint/ink. Mobile trio capped.
- Server contracts: `src/lib/watcher.server.ts`, `src/lib/voice.server.ts`. Client bridge: `src/lib/nile/grok-feel.ts`.

**Not done / do not regress:**

- GitHub vanilla kernel in PR `feel/three-verbs` has feel + authored Watcher. It does **not** import `@/lib/watcher.server` (Grok-only).
- Office still binaries are Grok-host only. Copy into `vortex/web/public/temples/` later; then point GitHub `journey-view.ts` `templeScene` at `/temples/<id>.jpg`.
- Do not register `/sw.js` in the Grok wrap. GitHub may keep its own SW.
- Auth off. Database off. localStorage `vortex-world-v3` / schema 5.

## Doctrine you must not break

- Ten offices, twenty-two streams. No extra ponds.
- Watcher has no chat UI and is never named in player-facing copy.
- No private keys, seeds, or WIF. Bound is signature-only at Malkhut.
- No invented tokens. Real Rare Pepe art stays attributed.
- Grok App Builder: TanStack Start, preview on the platform port, keep `grokPwaPlugin`, `PreviewHostBridge`, `startup.sh`.

## Kernel files

| File | Job |
|---|---|
| `vortex/web/watcher.ts` | Authored silent referee: `haste` / `tilt` / `thin` / `still`. Override may change water copy only. |
| `vortex/web/feel-audio.ts` | Mixer + drone lean + Walk/Look/Sit/reveal tones. Off until Settings. |
| `vortex/web/tests/watcher.test.ts` | Directives never mention “Watcher”; Sit clears darkness; override ≠ gameplay. |
| `src/lib/nile/grok-feel.ts` | Grok-only opt-in bridge. Dynamic-import server fns. |
| `src/lib/watcher.server.ts` | `consultWatcher`: grok-4.5, max_tokens 8, enum only. |
| `src/lib/voice.server.ts` | `speakGuide`: TTS eve, cache, 400 char cap. |
| `public/temples/<id>.jpg` | Ten stills. Referenced from OFFICE_RARE cards + nile-world. |
| `src/lib/nile/*` | Grok-hosted copy of the kernel. Keep twins with `vortex/web`. |

## Remaining jobs

### A. GitHub stills (binaries)

Copy `public/temples/*.jpg` into `vortex/web/public/temples/`. Patch GitHub `journey-view.ts` the same way as `src/lib/nile/journey-view.ts` (`TEMPLE_STILLS`). Do not invent a token.

### B. CLI: wire or freeze

`STAIRCASE.md`. Pick one. Do not grow a second correspondence table.

### C. Checks

```
npx tsc --noEmit
node --experimental-strip-types --test src/lib/nile/tests/*.test.ts
node scripts/browser-smoke.mjs
npm run build
```

Kernel tests that import `main.ts` expect auto-start on GitHub; the Grok wrap uses `export function mount`. Do not boot at import time (SSR). `grok-feel.ts` must keep server imports dynamic so vanilla tests do not load TanStack server fns.

## What “done” looks like

A player walks. The stream they used lights and is named. Look ticks a small tone, uncovers the original card, and (if spoken guides are on) speaks the authored line. Sit lifts darkness on the map. After hurried walks a stream stills and the compass mentions still water — never a director. Sound and hosted thinking stay off until chosen. Help fits on a phone. There is one map. Each office has its own still, cut from a real card.
