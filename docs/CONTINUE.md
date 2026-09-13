# Current handoff — publish the reviewed Grok host

Updated 13 September 2026 after the owner supplied the host backup. The shared game is `arwyn6969/vortex`; the Grok deployment source is the owner's private [arwyn6969/VortexSquared](https://github.com/arwyn6969/VortexSquared). **Use the host's current `main`, including `7c1e719`, for the next Grok build.** [The ready-to-send message](GROK_FINISH_MESSAGE.md) is now a short pull/build/republish handoff.

## Completed

- PR #13 integrated the shared game, Grok's original feedback branch and all outstanding dependency PRs. The shared core passed 76 tests, typecheck, production build and offline checks.
- The Grok backup at `531e33d` contained the Atlas, schema 5, mount/cleanup integration, temple stills and optional host adapters. Codex reviewed that source and pushed host fixes in `7c1e719`.
- The water response is now displayed. Late speech and moods cannot leak past Off, new actions, seeker changes or unmount. Server calls validate input, accept only authored speech, cache/deduplicate, and have request/response/time limits. These controls are per instance, not a global provider spending cap. No paid model calls were made during testing.
- Eight targeted host tests, host typecheck/build and local Chromium dev/production checks passed. The host now has Node 22 CI. See `docs/CODEX_HOST_REVIEW.md` in VortexSquared for exact evidence and limits.
- Forty-seven stale generated `.vercel/output` files were removed from host source control. Grok must build source before publishing. This does not prove why its earlier publication did not update the public URL.
- All ten temple images were recovered unchanged into this shared repository and wired into `templeScene`. [Provenance](ART_PROVENANCE.md) and a [SHA-256 manifest](references/grok-temple-stills.json) record the recovery. All ten decode offline; the standalone worker now caches 29 files.

## Shared core and host responsibilities

`vortex/web/main.ts` exports `mount(root, options?)` with an idempotent cleanup function and is safe to import during server rendering. Call it only in a client effect and return cleanup. One mounted game is supported. The standalone `bootstrap.ts` alone opts into `{ offline: true }`.

The Grok host preserves its TanStack wrapper, `grokPwaPlugin`, `PreviewHostBridge`, startup script and platform configuration. It does not import `bootstrap.ts` or register the standalone `/sw.js`. Its `src/lib/nile/main.ts` also wires host-specific settings and adapters; **do not blindly replace it with the generic shared main.ts**, which intentionally has no model calls. The two repositories now have the same temple-scene renderer and image bytes.

The reducer, ten offices, twenty-two streams and schema-5 save remain shared. Do not grow a second map or revive the frozen Python game; supported Python commands already serve the browser build.

## Remaining publication step

The current player URL is [pepevortex.grok.me](https://pepevortex.grok.me), through Grok App Builder. At the latest check it still served `index-kncGx_4e.js`, created schema-4 saves, lacked Atlas navigation and returned 404 for the checked temple still. The Grok host repository builds for the platform's Vercel target; no platform republish was performed from Codex. The older owner-only OpenAI Sites deployment is a separate surface.

Pull VortexSquared's current `main` into the existing Grok project. Run `npm run test:host`, `npm run typecheck` and `npm run build`. Republish that same project, then verify the public URL's Atlas, new asset bundle, temple image and save upgrade. Registering a project for publication is not confirmation that its public deployment changed.

Keep `vortex-world-v3` and preserve existing saves. Actual live-site v4 save migration to v5, retained progress/journal and an exact `vortex-last-good` recovery copy were verified; see [the live-site check](GROK_LIVE_REVIEW_2026-09-13.md). Moving between preview and public origins requires export/import.

Human playtests, Safari/Firefox/Android, assistive technology, specialist cultural review and real hosted update/rollback remain deferred. Optional provider success was not tested with paid credentials; authored play stays available on failure. No new art generation or broad redesign is needed for this republish.
