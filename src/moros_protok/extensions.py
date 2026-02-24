import os
from typing import Dict


def detect_pe_elf(path: str) -> Dict:
    """Very small heuristic detector for PE/ELF files and basic metadata.

    Returns dict with keys: type ('pe','elf','unknown'), arch ('x86','x86_64','arm','unknown')
    """
    res = {"type": "unknown", "arch": "unknown"}
    try:
        with open(path, "rb") as f:
            head = f.read(64)
            if head.startswith(b"MZ"):
                res["type"] = "pe"
                # rough check: search for 'PE\0\0' later
                f.seek(0)
                data = f.read(4096)
                if b"PE\x00\x00" in data:
                    # crude arch detection by machine field offset (very heuristic)
                    res["arch"] = "x86_64" if b"\x64\x86" in data or b"\x86\x64" in data else "x86"
            elif head.startswith(b"\x7fELF"):
                res["type"] = "elf"
                # byte 4 is class: 1 = 32-bit, 2 = 64-bit
                cls = head[4]
                res["arch"] = "x86_64" if cls == 2 else "x86"
    except Exception:
        pass
    return res


def try_yara_scan(path: str, rules_path: str):
    """Attempt to run yara scan if python-yara is installed.

    Returns list of matched rule names. If yara not installed, raises ImportError.
    """
    try:
        import yara
    except Exception as e:
        raise ImportError("yara module not available") from e
    rules = yara.compile(filepath=rules_path)
    matches = rules.match(path)
    return [m.rule for m in matches]
