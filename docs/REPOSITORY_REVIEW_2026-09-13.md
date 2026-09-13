# Repository and Grok handoff review — 13 September 2026

The project is on a sound track: the ten-office game already supports two complete chapters, meaningful return scenes, a solar crossing puzzle, a sourced Atlas and resilient local saves. Grok's smaller changes to movement, sound and water feedback strengthen that game. The immediate completion problem is keeping the GitHub and hosted copies aligned, then observing real players before expanding the scope.

This review inspected the repository, all remote branches, open pull requests and their available discussion, GitHub Actions, and the Sites deployment record. Native Chromium exercised the integrated local build. Grok's private wrapper, server functions and temple stills were unavailable; statements about those files below come from Grok's checked-in handoff, not independent inspection of that running app.

## Who hosts what

| Surface | Verified state at the start of this review |
| --- | --- |
| GitHub | Source at `arwyn6969/vortex`; `main` was `caabda0`. GitHub's deployments endpoint was empty. GitHub is the source repository, not evidence of a GitHub Pages deployment. |
| OpenAI Sites | `.openai/hosting.json` identifies the active VORTEX project. Sites reports [this live URL](https://vortex-living-lattice.azzybee.chatgpt.site), version 5, source `519098ab539df09c10c918149662ab7d7c5de7b4`. The deployment succeeded on 12 September at 22:39 UTC. Access is restricted to the owner. That published build predates `caabda0` and this integration. |
| Grok App Builder | `docs/GROK_HOST.md` and the original `docs/CONTINUE.md` describe a separate TanStack Start wrapper with platform preview/PWA support. No Grok URL, deployment record, wrapper source or server source was present in this repository. Its current live version and underlying infrastructure remain unverified. |

No deployment or hosting access change was performed in this pass. Pushing source to GitHub does not update either hosted copy automatically. Saves belong to each browser origin; export/import is necessary when moving between the Sites and Grok URLs.

## Branches and PRs

| Work | Finding and treatment |
| --- | --- |
| `feel/three-verbs` at `88dcf25` | Four Grok commits with no PR; the handoff reports GitHub's PR-create API failed. Integrated the authored referee, audio, map feedback and shorter help, then fixed the defects below. |
| `docs/grok-host`, PR [#12](https://github.com/arwyn6969/vortex/pull/12) | Three commits documenting the host and unfinished work. Preserved the original review and replaced the active handoff with the current state. No submitted reviews or inline review requests were present; the owner comment points to the gameplay branch. |
| Dependabot PRs [#9](https://github.com/arwyn6969/vortex/pull/9), [#10](https://github.com/arwyn6969/vortex/pull/10), [#11](https://github.com/arwyn6969/vortex/pull/11) | Integrated pinned checkout 7.0.1, setup-node 7.0.0 and setup-python 7.0.0. Their individual CI runs passed. Kept Node 22, Python 3.11 and read-only job permissions. Resolved the adjacent workflow-line merge conflict by retaining both updated pins. |
| `codex/playable-lattice`, `codex/returning-nile`, `codex/counterparty-ledger`, `codex/everlasting-marks`, `codex/living-atlas`, `play/named-streams` | Already contained in main; no missing commits to recover. |
| `lattice/bind-the-tree`, `docs/next-bound`, `play/lattice-veils` | Historical branches associated with already-merged work. Some commits remain unique because older PRs were integrated through different history. Their original feature requests are delivered; merging the old trees would reintroduce stale code/docs. Preserved the branches. |
| Issues and earlier PRs | No GitHub issues. PRs 1–8 were already merged. No additional open review requests were found. |

The integration branch is `codex/grok-handoff`. It preserves Grok's and Dependabot's commit ancestry so their work remains traceable. CI previously ran on `main` and `codex/**` pushes only: a `feel/**` branch without a PR received no checks. It now runs on every branch push as well as PRs.

## Strengths and weaknesses

- **The game has a coherent shape.** Ten offices and twenty-two streams give stories, rites and the Atlas a shared geography. Keep enriching those places; another travel map or a revived CLI game would divide the experience.
- **Consequences are becoming visible.** The boarding puzzle and saved-choice props give the player something to act on and later recognize. Grok's stream label, immediate feedback and opt-in tones support that direction. The next measure is whether fresh players actually notice the consequences and understand why a route is closed.
- **The foundation is unusually well covered.** Both chapters are tested from all 729 questionnaire combinations, along with story branches, encounter pairs, save migrations and randomized travel. Those tests did not catch Grok's audio and rendering bugs; integration and browser checks remain necessary.
- **The interface still asks players to read a lot.** The next-step guide, brief help, contextual labels and early rite controls reduce that burden. Keep the core verbs obvious and introduce archive/Atlas depth through encounters. Do not treat the host review's numeric scores as observed player evidence.
- **The main maintenance risk is two copies of the same game.** The new mount API lets the host reuse the core without maintaining a second startup implementation. Host-only code and images still need to be exported and backed up before they can be reviewed or synchronized safely.
- **Completion needs evidence, not more features.** The five-player worksheet, Safari/Firefox/Android and assistive-technology checks, cultural review and a real hosted update/rollback exercise remain outstanding. More model calls, accounts or additional systems would not resolve these gaps.

## Defects corrected

1. **Sound could resume after Off.** Ordinary game actions called the audio-unlock function before checking the setting. After suspension, an action could restart existing drones while the UI still said Off. Only explicit enabling now creates/resumes audio. Toggles serialize async operations, immediately mute, handle denial/device failure and dispose cleanly.
2. **Travel feedback was a turn late.** The game rendered before setting the last stream and animation. Feedback is now prepared before the action's render. Focus follows the new location. Opening a dialog no longer replays the previous action's animation.
3. **One seeker's feedback could leak into another's map.** Crossing/animation state now resets on seeker changes and external save updates; highlighting also requires that seeker's own crossing. A dark/veiled stream retains its unavailable appearance.
4. **The repository lacked a safe host entry point.** `main.ts` formerly booted at import time. It now exports `mount(root)` and a cleanup function; the standalone bootstrap alone opts into the repository's service worker. Cleanup removes listeners, browser tools, observers and audio, and cancels game actions still queued behind a lock. The module imports without a browser during server rendering.
5. **Short help omitted completion instructions.** Restored the Qoph condition and the Chapter II festival requirements while keeping the dialog scrollable on a small phone. Removed the hidden referee's name from the settings copy.
6. **The handoff reopened a resolved CLI decision.** The existing browser launcher and legacy freeze already settle it. Updated the old staircase/backlog labels so a future agent does not build a second runtime.

## Verification

- `npm run check`: **76 tests passed**, TypeScript passed, production build passed, offline worker's 19-file cache checks passed.
- Maintained Python suite: **22 passed**. Canon generation: **10 offices, 22 streams match**.
- Native Chromium: correct Samekh label and one highlighted stream on the actual crossing; travel focus; zero audio contexts during silent play; explicit On creates a running context; Off remains suspended after Sit; remount closes audio and one Look commits exactly once with one live announcer.
- Layout: help checked at 320, 390, 768 and 1280 pixels; at 320 it stays within the viewport and scrolls. All six main views checked at 320 pixels without duplicate IDs or horizontal overflow. No page exceptions in these checks.
- Production offline: the standalone worker controls the page; Look/Walk persist, an offline Sit saves, reload retains that save, and all six views open offline.
- The dev host mount registered no worker. A real Grok/TanStack production build and its platform worker remain untested because that source is unavailable.

Local JavaScript checks used Node 23.3; GitHub CI supplies the supported Node 22 runtime. The Python environment used 3.11. This evidence does not certify the frozen Python experiments or replace human/browser coverage. Current code keeps `vortex-world-v3`, schema 5 and the existing artwork; no hosted model calls were added.

## What is still needed for Grok

Use [CONTINUE.md](CONTINUE.md) for the exact host contract and remaining work. Retrieve the Grok project/URL and source export, preserve its wrapper/platform files, recover the ten temple images with provenance, and test the optional enum and TTS bridges before deploying there. The checked-in SVG/world/card treatment remains complete and playable while those assets are unavailable.
