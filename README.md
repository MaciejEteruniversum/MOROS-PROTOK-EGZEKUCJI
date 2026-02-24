# MOROS-PROTOK-EGZEKUCJI

Minimalny szkielet projektu przygotowany do budowania jako pakiet Python.

Szybkie kroki budowania i uruchamiania (lokalnie):

- Utwórz i aktywuj wirtualne środowisko (zalecane):

```
python -m venv .venv
source .venv/bin/activate
```

- Zainstaluj pakiet w trybie deweloperskim:

```
python -m pip install -e .
```

- Uruchom prosty CLI:

```
moros-protok --help
moros-protok run
```

- Uruchom testy (pytest):

```
python -m pip install -U pip
python -m pip install pytest
python -m pytest -q
```

# MOROS-PROTOK-EGZEKUCJI

Minimalny szkielet projektu przygotowany do budowania jako pakiet Python.

Szybkie kroki budowania i uruchamiania (lokalnie):

- Utwórz i aktywuj wirtualne środowisko (zalecane):

```
python -m venv .venv
source .venv/bin/activate
```

- Zainstaluj pakiet w trybie deweloperskim:

```
python -m pip install -e .
```

- Uruchom prosty CLI:

```
moros-protok --help
moros-protok run
```

- Uruchom testy (pytest):

```
python -m pip install -U pip
python -m pip install pytest
python -m pytest -q
```

Pliki utworzone (szkielet):

- [pyproject.toml](pyproject.toml)
- [src/moros_protok/main.py](src/moros_protok/main.py)
- [tests/test_basic.py](tests/test_basic.py)
- [.gitignore](.gitignore)

Frontend (prosty interfejs statyczny)

Możesz otworzyć interfejs znajdujący się w katalogu `frontend` jako statyczny serwis. Najprostszy sposób lokalny:

```
cd frontend
python3 -m http.server 8000
# następnie otwórz http://localhost:8000 w przeglądarce
```

Alternatywnie (jednolinijkowo z katalogu głównego):

```
python3 -m http.server 8000 --directory frontend
```

Utworzone pliki frontend:

- [frontend/index.html](frontend/index.html)
- [frontend/styles.css](frontend/styles.css)
- [frontend/script.js](frontend/script.js)

Jeżeli chcesz, przygotuję dodatkowy pipeline CI, integrację z GitHub Actions lub wersję SPA/React.

CI / GitHub Actions

- Dodałem prosty workflow `.github/workflows/antivirus-scan.yml`, który uruchamia testy i wykonuje skan repo przy każdym `push` i `pull_request`.
- Plik podpisów przykładowych znajduje się w `signatures.json` (format: `{ "sha256": "label" }`).

Uruchamianie lokalne skanu (przykład):

```
PYTHONPATH=src python -m moros_protok.main scan . --signatures signatures.json > scan-output.json
```

Wynik zostanie zapisany jako JSON (po jednym rekordzie JSON na linię dla każdego zeskanowanego pliku).
