# Grok live-site check — 13 September 2026

The owner supplied the current player URL: **https://pepevortex.grok.me**. Native Chromium loaded it successfully (HTTP 200, title “VORTEX · The Nile of Rare Frogs”). The page loads Grok App Builder's extension, confirming the Grok-hosted surface. The separate OpenAI Sites deployment is not the URL the owner is currently using. This check did not identify Grok's underlying infrastructure vendor or the exact source commit of the published bundle.

## The live build is behind GitHub

The live page referenced `/assets/index-kncGx_4e.js`. It created a **version-4** save in `vortex-world-v3`. Its navigation had Tree, Stories, Streams, Asset archive and Journal, with **no Living Atlas**. The new temple-scene panel, named last-crossing stream and feedback animation were absent. Settings offered the older simple ambient chord and no voice/model opt-ins.

This is older than the shared game now merged to GitHub `main` through PR #13 (`315738d`). The features reported in Grok's earlier handoff may exist in an unpublished workspace; the live site does not demonstrate that they were deployed. Do not spend credit rebuilding features already in GitHub or assume the currently published bundle contains the latest Grok draft.

All ten documented `/temples/<id>.jpg` URLs returned **404** on HEAD requests: keter, chokhmah, binah, chesed, gevurah, tiferet, netzach, hod, yesod and malkhut. Those images could not be recovered from these public paths. They may still be available in Grok's project workspace. The standard Nile and original Rare Pepe art loaded.

## Observed behavior

A disposable browser context created a synthetic seeker, answered all six questions, Looked, walked Tiferet → Hod and reloaded. The save persisted and no page exceptions occurred. No existing player save was accessed or changed. Voice/model options were not enabled and no paid generation requests were made.

| Viewport | Observed horizontal overflow |
| --- | --- |
| 320px | Stories and Asset archive |
| 390px | None across the five available main views |
| 768px | All five main views |
| 1280px | None across the five available main views |

No duplicate IDs were found across these 20 view/width combinations. At 320 × 780, the help dialog sat at the top-left (`left: 0`, `top: 0`), with scrollable content taller than its box. The GitHub build already contains navigation/reflow and dialog fixes; synchronize them before making another CSS patch. No service-worker registration was observed in the isolated live browser context; preserve and verify the actual Grok platform configuration rather than assuming either offline success or a platform fault.

## Actual live-save migration

A synthetic version-4 save created through the live site's UI was loaded into the locally built production version of GitHub `main`. The first successful Look wrote schema 5 and advanced the revision exactly once. Identity, dialect, location, pillars, visited temples, rites, stories, festival, crossings, Harmony, sigil, rooted state, proof and creation timestamp were preserved. Existing journal entries were retained. `vortex-last-good` held the **exact original live-site save bytes**. Living Atlas became available.

This checks the actual published save format in addition to the released-v4 fixtures already in the 76-test suite. It is not a test of the eventual TanStack deployment or every existing player's data. Publish in place on the same origin and retain `vortex-world-v3`; do not clear localStorage or downgrade a schema-5 save.

## Minimum remaining host work

1. Synchronize the reviewed shared game from GitHub `main` into the existing Grok host using the mount/cleanup contract in [CONTINUE.md](CONTINUE.md). Preserve its TanStack/platform files and any existing unpublished host adapters.
2. Recover and back up the existing host-only wrapper/server glue and temple images if present. Keep credentials out of GitHub. Do not generate replacement art or add model features just to satisfy an earlier wish list; the shared game works with its existing art and authored guides.
3. Test the actual host: typecheck/build and targeted browser smoke, including a current v4 save, Atlas, Look/Walk/Sit, On/Off, phone/tablet layout and remount/reload. Keep optional hosted calls off by default with bounded inputs and an authored fallback if those adapters already exist.
4. Publish to the existing `pepevortex.grok.me` project only after checks pass, then verify the deployed page contains the Atlas and preserves an existing journey. Record the deployed Git commit and any genuinely deferred host-only work.

The owner has limited Grok credit. No fresh architecture, large feature additions, regenerated media, Python-runtime revival or repeat full-game review is needed. [The ready-to-send message](GROK_FINISH_MESSAGE.md) focuses the remaining work.
