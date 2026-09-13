# Handoff — shared game and Grok host

Updated 13 September 2026. The repository review and integration are in `codex/grok-handoff`; see [the findings and verification](REPOSITORY_REVIEW_2026-09-13.md). Grok's four `feel/three-verbs` commits, the three `docs/grok-host` commits and Dependabot PRs 9–11 are integrated with audio, feedback and lifecycle fixes. This handoff supersedes the earlier request to create a PR for `feel/three-verbs`.

## Current shared code

- Ten offices, twenty-two streams, two chapters, solar boarding puzzle, consequential stories and Living Atlas.
- Contextual map labels, last-crossed stream name, one-action animation and authored water feedback.
- Ambient drone and Walk/Look/Sit/reveal tones, off until explicitly chosen. Off stays silent and unmount closes the context.
- One browser core in `vortex/web`, localStorage `vortex-world-v3`, schema 5. No auth or database required.
- `main.ts` exports `mount(root, options?)`, returning an idempotent cleanup function. Import is safe during server rendering; call mount only in a browser. One mounted game is supported at a time.
- `bootstrap.ts` starts the standalone Vite game with `{ offline: true }`. Default `mount(root)` does not register `/sw.js`, so a host can own its PWA behavior.
- 76 JavaScript tests and 22 maintained Python tests passed, alongside typecheck, build, canon and native Chromium/offline checks. See the review for exact limits.

## Embed in the Grok wrapper

Copy the reviewed shared modules together, preserving relative imports and public asset paths. Do not import `bootstrap.ts` in the TanStack/React host. A client effect can own the lifecycle:

```tsx
import { useEffect, useRef } from "react";
import { mount } from "@/lib/nile/main";

export function NileHost() {
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!root.current) return;
    return mount(root.current);
  }, []);
  return <div ref={root} />;
}
```

This is an integration example, not a claim that the unavailable host build was tested. Retain Grok's `grokPwaPlugin`, `PreviewHostBridge`, `startup.sh`, platform port and share-card configuration. Do not replace its service worker with the standalone Vite worker. Keep host dialog controls outside the mounted root.

The current core has no hosted voice/enum settings. Before replacing the host's modified `main.ts`, reconcile those existing settings, bridge calls and privacy copy against the reviewed shared changes. Do not silently remove the host's opt-ins or keep a claim that no model calls occur while enabling them. Keep host adapters separate from the reducer and include them in a source backup; avoid editing two divergent kernels by hand.

## Grok-only work still unavailable here

The following were reported complete by Grok, but neither these files nor a Grok project URL were in GitHub at review time. Retrieve the source/export before claiming they are reviewed or backed up:

| Host path | Reported behavior and follow-up |
| --- | --- |
| `src/lib/nile/grok-feel.ts` | Optional bridge with dynamic server imports. Review opt-in, cancellation, fallback and calls after unmount; never send complete saves or guide questions. |
| `src/lib/watcher.server.ts` | `consultWatcher`, `grok-4.5`, max 8 tokens, one of `haste/tilt/thin/still`, every fourth turn only after explicit opt-in. Independently verify server validation, request/cost bounds and failure handling. Gameplay authority stays in the authored reducer. |
| `src/lib/voice.server.ts` | `speakGuide`: authored `voice(s)` only, Eve, 400-character cap, cache and silence fallback. Verify both server limits and client opt-in/stop behavior. |
| `public/temples/<id>.jpg` | Ten office stills derived from the verified Rare Pepe cards. Recover originals, record provenance, inspect/compress, copy into `vortex/web/public/temples/`, and port the host's `TEMPLE_STILLS` scene treatment. Keep original card art after Look and useful fallbacks. Recheck offline asset coverage. |
| `NileHost.tsx` and platform config | Review the actual wrapper, update to the mount contract, retain platform integration, and test navigation/remount, phone dialogs, saves and platform updates in that host. |

Do not recreate missing art and pass it off as recovered Grok work. No Grok-only model calls or credentials were added to the shared core. The existing attributed art and illustrated scenes remain available.

## Hosting and deployment

The verified Sites deployment is [VORTEX](https://vortex-living-lattice.azzybee.chatgpt.site), restricted to its owner, with a version-5 build from `519098a`. It predates this integration. The separate Grok deployment's URL/version remain unknown. No deployment or access changes were made during this pass.

Before using Grok to put this live, synchronize the reviewed GitHub source and recovered host files; run the host's typecheck, tests, browser smoke and production build. Export a real save, check both chapters, sound Off/On/Off, guide opt-ins, 320px dialogs and refresh/remount. Exercise the actual platform update with an existing schema-5 save. Moving between hosting domains requires export/import; localStorage is not shared.

## Resolved and deferred work

The CLI decision is **resolved**: `run_game.py`, `python -m vortex.src.main` and the installed `vortex` command serve the browser build. Old game/AI experiments are frozen; see [LEGACY.md](LEGACY.md). Do not wire another travel model.

The [five-player worksheet](PLAYTEST_WORKSHEET.md), Safari/Firefox/Android, assistive technology, real hosted update/rollback and specialist cultural review remain outstanding. No human observations or unavailable-host test results have been invented.

## Doctrine

Ten offices, twenty-two streams. No new ponds or invented tokens. Keep original art attributed. Keep the silent referee unnamed in player-facing copy and without a chat UI. Keys, seeds and WIF never belong in the game; Bound is signature-only at Kingdom. Optional host AI must have an explicit choice, bounded requests and an authored fallback; it never changes gameplay authority.
