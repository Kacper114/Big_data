# Zadanie z zajęć 2 - Zarządzanie Big Data

To jest rozwiązanie zadania z czyszczenia i analizy danych e-commerce.

W pracy robię po kolei:

1. generuję brudny plik `zamowienia_messy.csv`,
2. sprawdzam dane i wypisuję problemy z jakością,
3. czyszczę teksty, daty, ceny, braki i błędne ilości,
4. dodaję nowe kolumny, np. wartość zamówienia i dane z daty,
5. robię proste analizy przez `groupby`,
6. zapisuję wykres i oczyszczony plik CSV.

## Pliki

- `zadanie_zajecia_2.py` - główne rozwiązanie,
- `zadanie_zajecia_2.ipynb` - notebook do wygodnego podglądu na GitHubie,
- `requirements.txt` - biblioteki potrzebne do uruchomienia,
- `zamowienia_messy.csv` - brudne dane wygenerowane przez skrypt,
- `zamowienia_clean.csv` - dane po czyszczeniu,
- `wartosc_zamowien_miesiace.png` - wykres miesięcznej wartości zamówień.

## Jak uruchomić

W terminalu w tym folderze:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python zadanie_zajecia_2.py
```

Po uruchomieniu w terminalu pojawi się eksploracja danych, lista problemów, wyniki analiz oraz informacja o zapisanych plikach.
