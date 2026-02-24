import hashlib
import math
import os
import shutil
from typing import Dict, List
import json
from datetime import datetime

SUSPICIOUS_STRINGS = [
    "eval(", "exec(", "base64", "powershell", "CreateRemoteThread", "VirtualAlloc", "LoadLibrary",
    "/bin/sh", "#!/bin/sh", "MZ", "PE", "WScript"  # simple heuristics
]


def compute_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def file_entropy(path: str) -> float:
    with open(path, "rb") as f:
        data = f.read()
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = 0.0
    length = len(data)
    for c in freq:
        if c == 0:
            continue
        p = c / length
        entropy -= p * math.log2(p)
    return entropy


def scan_file(path: str, signatures: Dict[str, str] = None) -> Dict:
    """Scan a single file and return a result dict with reasons if suspicious.

    signatures: optional dict mapping sha256 -> label
    """
    signatures = signatures or {}
    res = {
        "path": path,
        "sha256": None,
        "entropy": None,
        "suspicious_strings": [],
        "reasons": [],
        "malicious": False,
    }
    try:
        res["sha256"] = compute_sha256(path)
        res["entropy"] = file_entropy(path)
        # signature match
        if res["sha256"] in signatures:
            res["reasons"].append(f"signature:{signatures[res['sha256']]}")
        # heuristics: high entropy (e.g., >7.5) often indicates packed/encoded binaries
        if res["entropy"] and res["entropy"] > 7.5:
            res["reasons"].append("high-entropy")
        # check suspicious strings in textual portion
        try:
            with open(path, "r", errors="ignore") as f:
                text = f.read()
                for s in SUSPICIOUS_STRINGS:
                    if s in text:
                        res["suspicious_strings"].append(s)
        except Exception:
            pass
        if res["suspicious_strings"]:
            res["reasons"].append("suspicious-strings")
        # determine malicious if any reason found
        if res["reasons"]:
            res["malicious"] = True
    except Exception as e:
        res["reasons"].append(f"error:{e}")
    return res


def scan_path(path: str, recursive: bool = True, signatures: Dict[str, str] = None) -> List[Dict]:
    results = []
    if os.path.isfile(path):
        results.append(scan_file(path, signatures=signatures))
        return results
    for root, dirs, files in os.walk(path):
        for fn in files:
            fp = os.path.join(root, fn)
            results.append(scan_file(fp, signatures=signatures))
        if not recursive:
            break
    return results


def ensure_quarantine_dir(base: str = None) -> str:
    base = base or os.path.join(os.getcwd(), ".quarantine")
    os.makedirs(base, exist_ok=True)
    return base


def quarantine(path: str, dest_dir: str = None) -> str:
    dest_dir = ensure_quarantine_dir(dest_dir)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    name = os.path.basename(path)
    i = 0
    target = os.path.join(dest_dir, name)
    while os.path.exists(target):
        i += 1
        target = os.path.join(dest_dir, f"{name}.{i}")
    shutil.move(path, target)
    # write metadata alongside quarantined file
    meta = {
        "original_path": os.path.abspath(path),
        "quarantined_at": datetime.utcnow().isoformat() + "Z",
        "sha256": compute_sha256(target),
        "size": os.path.getsize(target),
    }
    meta_path = target + ".meta.json"
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return target
