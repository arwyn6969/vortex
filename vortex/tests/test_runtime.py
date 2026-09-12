"""Regression checks for the supported launcher and small legacy kernel fixes."""
import math
import subprocess
import sys
from vortex.web_server import main
from vortex.src.core.lattice import Lattice

def test_launcher_needs_only_standard_library_and_reports_missing_build(tmp_path, capsys):
    assert main(["--directory", str(tmp_path)]) == 1
    assert "npm ci" in capsys.readouterr().err

def test_engine_start_returns_control_without_busy_loop():
    subprocess.run([sys.executable, "-c", """
from vortex.src.core.engine import CoreEngine
e = CoreEngine()
events = []
for name in ('game_init', 'game_start', 'game_end'):
    e.event_bus.subscribe(name, lambda data, name=name: events.append(name))
e.start()
e.start()
assert e.state.is_running
e.stop()
e.stop()
assert events == ['game_init', 'game_start', 'game_end']
"""], check=True, timeout=5)

def test_neutral_placement_and_nonfinite_values():
    assert Lattice().place({}).node.sefirah == "tiferet"
    scores = Lattice().pillar_scores({"empathy": math.nan, "creativity": math.inf})
    assert all(math.isfinite(value) for value in scores.values())

def test_old_hub_aliases_can_reach_a_real_shore():
    for alias in ("Central Hub", "Reflection Pool", "Sacred Grove"):
        assert Lattice().travel(alias, "Meme Studio").sefirah == "hod"
