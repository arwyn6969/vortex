from vortex.src.mythology.paths import (
    PATH_LETTERS,
    PATH_MEANINGS,
    all_letters,
    path_between,
    path_key,
    path_meaning,
)
from vortex.src.mythology.sefirot import get_direct_connections


def test_twenty_two_streams():
    assert len(PATH_LETTERS) == 22
    assert len(set(all_letters())) == 22
    assert set(PATH_MEANINGS) == set(all_letters())


def test_undirected_lookup():
    a = path_between("yesod", "malkhut")
    b = path_between("Malkhut", "Yesod")
    assert a is not None and b is not None
    assert a["letter"] == "Tav"
    assert a["letter"] == b["letter"]
    assert a["meaning"] == path_meaning("Tav")


def test_qoph_is_netzach_malkhut():
    p = path_between("netzach", "malkhut")
    assert p is not None
    assert p["letter"] == "Qoph"
    assert "malkhut" in get_direct_connections("netzach")
    assert "netzach" in get_direct_connections("malkhut")


def test_missing_path():
    assert path_between("keter", "malkhut") is None


def test_path_key_stable():
    assert path_key("hod", "yesod") == path_key("yesod", "hod")
