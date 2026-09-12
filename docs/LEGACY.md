# Legacy Python experiments

The supported player entry is now the browser game described in the root README. `run_game.py`, `python -m vortex.src.main`, and the installed `vortex` command serve its built files. They do not import the scientific, forecasting, GUI, or LLM experiments.

The Living Atlas also excludes the old cross-cultural/archetype tables. Their unreviewed equivalences, known Maya/Aztec conflations and disputed Dogon astronomy are research leads, not published reference data. `ArchetypeManager` still has a dictionary/object mismatch; it must not be imported as a production atlas service. Curated entries and relationship provenance live in `vortex/web/atlas.ts`; the [editorial record](LIVING_ATLAS.md) describes their limits.

The older sources under `vortex/src/core/game.py`, `vortex-next/`, and most of `vortex/tests/` remain available for historical reference and selective reuse. They contain incomplete integrations and conflicting state models. `requirements-legacy.txt` records their optional dependencies; it is not required for normal play and does not make every legacy experiment production-ready.

Default `pytest` now targets the maintained lattice/path/veil/launcher checks. Running `pytest vortex/tests` explicitly requests the broader experimental suite and can still report unrelated dependency and integration failures. Do not interpret the focused CI result as a claim that the entire legacy test collection passes.

This release corrects the legacy engine's startup busy loop, neutral/nonfinite placement, hub aliases, a broken `core` import shim, and an inaccurate encryption claim. The new browser reducer owns the playable save model. Further Python components should be ported behind a tested adapter, not wired into the game by a broad import shim.

The old command-line private-key signing helper is retired. Create the challenge at Kingdom and sign it in your own wallet. Do not place private keys in a command line, game form, log, or guide conversation.
