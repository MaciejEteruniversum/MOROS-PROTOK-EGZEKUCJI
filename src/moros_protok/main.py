import argparse
import sys
import json
import os

from . import __version__
from . import antivirus


def load_signatures(path: str):
    if not path or not os.path.exists(path):
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def main(argv=None):
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(prog="moros-protok", description="MOROS protokół - CLI (szkielet)")
    sub = parser.add_subparsers(dest="cmd")

    run_p = sub.add_parser("run", help="Uruchom próbny przebieg")

    scan_p = sub.add_parser("scan", help="Skanuj ścieżkę (pliki/katalog)")
    scan_p.add_argument("path", help="Plik lub katalog do skanowania")
    scan_p.add_argument("--signatures", help="Plik JSON z podpisami sha256->label")

    q_p = sub.add_parser("quarantine", help="Przenieś plik do kwarantanny")
    q_p.add_argument("path", help="Plik do przeniesienia")
    q_p.add_argument("--dir", help="Katalog kwarantanny (opcjonalnie)")

    list_p = sub.add_parser("list-quarantine", help="Wypisz zawartość katalogu kwarantanny")
    list_p.add_argument("--dir", help="Katalog kwarantanny (opcjonalnie)")

    addsig = sub.add_parser("add-signature", help="Dodaj podpis sha256 do signatures.json")
    addsig.add_argument("sha256", help="Sha256 sum")
    addsig.add_argument("label", help="Etykieta dla podpisu")

    listsig = sub.add_parser("list-signatures", help="Wypisz podpisy ze signatures.json")

    args = parser.parse_args(argv)

    if args.cmd == "run":
        print(f"MOROS-PROTOK-EGZEKUCJI v{__version__}: przykładowy przebieg")
        return 0

    if args.cmd == "scan":
        sigs = load_signatures(args.signatures) if getattr(args, "signatures", None) else {}
        results = antivirus.scan_path(args.path, signatures=sigs)
        for r in results:
            out = {
                "path": r["path"],
                "malicious": r["malicious"],
                "reasons": r["reasons"],
                "sha256": r["sha256"],
                "entropy": r["entropy"],
            }
            print(json.dumps(out, ensure_ascii=False))
        return 0

    if args.cmd == "quarantine":
        try:
            tgt = antivirus.quarantine(args.path, dest_dir=args.dir)
            print(f"Przeniesiono do kwarantanny: {tgt}")
            return 0
        except Exception as e:
            print(f"Błąd: {e}")
            return 2

    if args.cmd == "list-quarantine":
        d = args.dir or os.path.join(os.getcwd(), ".quarantine")
        if not os.path.exists(d):
            print("Katalog kwarantanny nie istnieje")
            return 1
        for name in sorted(os.listdir(d)):
            print(name)
        return 0

    if args.cmd == "add-signature":
        path = "signatures.json"
        sigs = load_signatures(path)
        sigs[args.sha256] = args.label
        with open(path, "w", encoding="utf-8") as f:
            json.dump(sigs, f, ensure_ascii=False, indent=2)
        print(f"Dodano podpis: {args.sha256} -> {args.label}")
        return 0

    if args.cmd == "list-signatures":
        path = "signatures.json"
        sigs = load_signatures(path)
        for k, v in sigs.items():
            print(f"{k}  {v}")
        return 0

    parser.print_help()


if __name__ == "__main__":
    main()
