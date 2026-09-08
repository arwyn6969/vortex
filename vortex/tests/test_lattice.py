"""Lattice rules: placement, path legality, Malkhut floor."""
from vortex.src.core.lattice import Lattice, LatticeError
from vortex.src.core.watcher_directives import DirectiveKind, WatcherDirective
from vortex.src.mythology.correspondences import NODES, get_node


def test_every_sefirah_has_a_pond_and_classical_guide():
    assert set(NODES) == {
        "keter",
        "chokhmah",
        "binah",
        "chesed",
        "gevurah",
        "tiferet",
        "netzach",
        "hod",
        "yesod",
        "malkhut",
    }
    for node in NODES.values():
        assert node.pond
        assert node.classical_guide_id
        assert node.pillar in {"mercy", "severity", "balance"}


def test_only_malkhut_is_ledger_floor():
    floors = [n.sefirah for n in NODES.values() if n.ledger_floor]
    assert floors == ["malkhut"]


def test_mercy_profile_starts_in_wisdom():
    lattice = Lattice()
    profile = {
        "empathy": 0.9,
        "creativity": 0.8,
        "curiosity": 0.85,
        "social_awareness": 0.7,
        "decision_making": 0.2,
        "persistence": 0.2,
    }
    placement = lattice.place(profile)
    assert placement.node.sefirah == "chokhmah"
    assert placement.node.pond == "Wisdom Pond"
    assert placement.dialect == "folk"
    assert placement.guide_id == "wise_pepe"


def test_severity_profile_starts_in_zen():
    lattice = Lattice()
    profile = {
        "decision_making": 0.9,
        "strategic_thinking": 0.85,
        "persistence": 0.8,
        "moral_alignment": 0.7,
        "empathy": 0.1,
        "creativity": 0.1,
    }
    placement = lattice.place(profile)
    assert placement.node.sefirah == "binah"
    assert placement.dialect == "classical"
    assert placement.guide_id == "maat"


def test_travel_only_along_sefirot_paths():
    lattice = Lattice()
    lattice.travel("Harmony Pond", "Kingdom Pond")
    try:
        lattice.travel("Crown Pond", "Kingdom Pond")
        assert False, "Crown must not teleport to Kingdom"
    except LatticeError as exc:
        assert "No path" in str(exc)


def test_ledger_blocked_off_malkhut():
    lattice = Lattice()
    assert lattice.ledger_effects_allowed("Kingdom Pond") is True
    assert lattice.ledger_effects_allowed("Wisdom Pond") is False
    try:
        lattice.assert_ledger_floor("Vibe Temple")
        assert False, "Vibe Temple is not the ledger floor"
    except LatticeError as exc:
        assert "not Malkhut" in str(exc)


def test_hod_may_create_kingdom_may_bind():
    lattice = Lattice()
    assert lattice.creation_allowed("Meme Studio") is True
    assert lattice.creation_allowed("Crown Pond") is False
    assert get_node("hod").token_categories


def test_watcher_cannot_teleport_to_malkhut_from_keter():
    lattice = Lattice()
    directive = WatcherDirective(
        kind=DirectiveKind.REQUIRE_MALKHUT,
        reason="test",
    )
    assert lattice.interpret_directive("keter", directive) is None


def test_location_graph_covers_ten_ponds():
    graph = Lattice().location_graph()
    assert len(graph) == 10
    for pond, exits in graph.items():
        assert pond
        for dest in exits:
            assert dest in graph
