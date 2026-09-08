# Staircase — wiring the existing repo to the lattice

The lattice was already drawn in zone files, Pepe guides, sefirot paths,
The Watcher, and the Bitcoin tools. The running `Game.start()` path did
not climb those stairs. This branch installs the missing middle.

## Done on this branch

1. Doctrine (`THE_LATTICE.md`).
2. One correspondence table for all ten sefirot.
3. `Lattice` service: place a profile, list legal paths, pick a dialect,
   decide whether ledger effects are in-bounds.
4. Watcher directive vocabulary (silent director, not another chatbot).
5. `LocationManager` can build its graph from the lattice instead of the
   placeholder Hub / Grove / Library map.
6. Intro no longer asks for a private key. Bind is address + signature.
7. Tests for placement, path legality, Malkhut floor, and key refusal.
8. MIT `LICENSE` (README already claimed it).
9. `SECURITY.md` for the ledger floor.

## Still to wire (follow-up PRs, keep them small)

1. `Game.assign_guide` should call `Lattice.place()` then
   `GuideFactory.create_for_placement(...)`.
2. `Game.start_game_loop` should emit every turn to The Watcher.
3. Watcher `_update_directives` should return `WatcherDirective` objects
   that the dialogue prompt includes as constraints.
4. Register Pepe guides in `GuideFactory` only after their constructors
   match `Guide.__init__(name, archetype_name, cultural_system, attributes)`.
   Today several Pepe classes use a shorter signature — do not paper over that.
5. Token multipliers apply only when `Lattice.ledger_effects_allowed(sefirah)`.
6. Content-creation permissions gate on `node.creation_unlock`, not admin.
7. Replace local 70B `DeepseekClient` load with an API-shaped client.
   Guides and Watcher may be different models; they must not be the same call.

## Non-goals that stay out

GPS, HealthKit, government ID, social-graph scrape, federated learning,
AR/VR. Those are a different temple. They violate the intro line
"share only what you're comfortable with."
