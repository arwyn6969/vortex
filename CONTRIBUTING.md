# Contributing

Read `docs/doctrine/THE_LATTICE.md` first. If a change fights the tree,
it does not land.

## Rules of the house

1. One sefirah per pond. Do not invent a twelfth sphere without updating
   `vortex/src/mythology/correspondences.py` and the path table.
2. Guides are dialects. Add a folk or classical mouth to an existing office
   before adding a new zone.
3. The Watcher does not talk.
4. Keys never enter the process. Signatures do.
5. Small PRs. One staircase step each. See `docs/doctrine/STAIRCASE.md`.

## Tests

```bash
pytest vortex/tests/test_lattice.py
```

If you change path connections in `sefirot.py`, update lattice tests.
If you change a pond name, update the correspondence table in the same commit.
