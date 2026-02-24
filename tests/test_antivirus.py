import os
import tempfile
from moros_protok import antivirus


def test_scan_detects_suspicious_string(tmp_path):
    p = tmp_path / "sus.txt"
    p.write_text("this is a test with eval( dangerous ) and some base64 string")
    results = antivirus.scan_path(str(tmp_path))
    found = [r for r in results if r["path"].endswith("sus.txt")]
    assert found, "file not scanned"
    r = found[0]
    assert r["malicious"] is True
    assert "suspicious-strings" in r["reasons"]


def test_quarantine_moves_file(tmp_path):
    p = tmp_path / "to_quarantine.bin"
    p.write_bytes(b"dummy")
    qdir = tmp_path / "q"
    qdir.mkdir()
    tgt = antivirus.quarantine(str(p), dest_dir=str(qdir))
    assert os.path.exists(tgt)
    assert not os.path.exists(p)
    # metadata file should exist
    meta = tgt + ".meta.json"
    assert os.path.exists(meta)
    import json
    with open(meta, "r", encoding="utf-8") as f:
        m = json.load(f)
    assert m["original_path"].endswith("to_quarantine.bin")
