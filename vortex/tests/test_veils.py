from vortex.src.mythology.veils import pillars_meet, stream_open


def test_crown_veiled_until_harmony():
    assert stream_open("tiferet", "keter", harmony=False, looked_at_netzach=False) is False
    assert stream_open("tiferet", "keter", harmony=True, looked_at_netzach=False) is True
    assert stream_open("chokhmah", "keter", harmony=False, looked_at_netzach=True) is False
    assert stream_open("keter", "chokhmah", harmony=False, looked_at_netzach=False) is True


def test_qoph_veiled_until_look():
    assert stream_open("netzach", "malkhut", harmony=True, looked_at_netzach=False) is False
    assert stream_open("netzach", "malkhut", harmony=False, looked_at_netzach=True) is True
    assert stream_open("yesod", "malkhut", harmony=False, looked_at_netzach=False) is True


def test_missing_path_stays_missing():
    assert stream_open("keter", "malkhut", harmony=True, looked_at_netzach=True) is False


def test_pillars_meet():
    assert pillars_meet(0.25, 0.25) is True
    assert pillars_meet(0.24, 0.9) is False
