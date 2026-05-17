# Zadanie z zajęć 1 - Zarządzanie Big Data

Rozwiązanie zadania: **Analiza danych o krajach świata**.

Projekt wykonuje pełny pipeline:

1. pobranie danych z publicznego API REST Countries,
2. przetworzenie danych JSON do tabeli `DataFrame`,
3. zapis danych do bazy SQLite `kraje_swiata.db`,
4. analiza danych za pomocą zapytań SQL,
5. przygotowanie wykresu słupkowego z populacją regionów.

## Pliki

- `zadanie_zajecia_1.py` - główny plik z rozwiązaniem,
- `requirements.txt` - lista potrzebnych bibliotek,
- `kraje_swiata.db` - baza danych tworzona po uruchomieniu programu,
- `populacja_regionow.png` - wykres tworzony po uruchomieniu programu.

## Uruchomienie

W terminalu, w folderze projektu:

```powershell
uv init
uv add pandas requests matplotlib
uv run python zadanie_zajecia_1.py
```

Jeśli nie używasz `uv`, możesz uruchomić projekt klasycznie:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python zadanie_zajecia_1.py
```

Po uruchomieniu w terminalu pojawią się wyniki `head()`, `shape`, `dtypes` oraz odpowiedzi na pytania SQL z zadania.
