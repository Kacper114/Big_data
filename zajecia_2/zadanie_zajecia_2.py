import os
from datetime import datetime, timedelta

os.environ.setdefault("MPLCONFIGDIR", ".matplotlib")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MESSY_FILE = "zamowienia_messy.csv"
CLEAN_FILE = "zamowienia_clean.csv"
PLOT_FILE = "wartosc_zamowien_miesiace.png"


def generate_messy_data():
    np.random.seed(42)
    n = 500

    klienci = [
        "Anna Kowalska",
        " Jan Nowak",
        "Anna Kowalska",
        "PIOTR WIŚNIEWSKI",
        "katarzyna lewandowska",
        "Tomasz Zieliński ",
        "Marta Wójcik",
        "anna kowalska ",
        "Krzysztof Kamiński",
        " Magdalena Dąbrowska",
    ]
    produkty = [
        "Laptop",
        "Mysz",
        "Klawiatura",
        "Monitor",
        "laptop",
        "MYSZ",
        "Słuchawki",
        "Pendrive",
        "monitor",
        "Webcam",
    ]
    kategorie = [
        "Elektronika",
        "elektronika",
        "ELEKTRONIKA",
        "Akcesoria",
        "akcesoria",
        "Akcesoria ",
    ]
    miasta = [
        "Warszawa",
        "Kraków",
        "warszawa",
        "Gdańsk",
        "WROCŁAW",
        "Poznań",
        "Łódź ",
        " Warszawa",
        "kraków",
    ]

    start_date = datetime(2025, 1, 1)
    daty_iso = [
        (start_date + timedelta(days=int(d))).strftime("%Y-%m- %d ")
        for d in np.random.randint(0, 300, n // 2)
    ]
    daty_pl = [
        (start_date + timedelta(days=int(d))).strftime(" %d .%m.%Y")
        for d in np.random.randint(0, 300, n // 2)
    ]
    daty = daty_iso + daty_pl
    np.random.shuffle(daty)

    df = pd.DataFrame(
        {
            "order_id": range(1001, 1001 + n),
            "klient": np.random.choice(klienci, n),
            "produkt": np.random.choice(produkty, n),
            "kategoria": np.random.choice(kategorie, n),
            "miasto": np.random.choice(miasta, n),
            "ilosc": np.random.choice(
                [1, 2, 3, 5, -1, 0],
                n,
                p=[0.5, 0.2, 0.15, 0.1, 0.025, 0.025],
            ),
            "cena_jednostkowa": np.random.choice(
                ["199.99", "299,99", "1 499.00", "89.50", "2999", "399.00 zł", None, "abc"],
                n,
            ),
            "data_zamowienia": daty,
            "email": np.random.choice(
                [
                    "anna@gmail.com",
                    "JAN@WP.PL",
                    "piotr.w@onet",
                    "marta@gmail.com",
                    "tomasz@interia.pl",
                    None,
                    "krzysztof.k@gmail.com",
                    "brak",
                ],
                n,
            ),
        }
    )

    for col in ["miasto", "kategoria", "data_zamowienia"]:
        df.loc[df.sample(frac=0.05, random_state=1).index, col] = np.nan

    df = pd.concat([df, df.sample(20, random_state=2)], ignore_index=True)
    df.to_csv(MESSY_FILE, index=False)
    print(f"Wygenerowano plik {MESSY_FILE}: {len(df)} wierszy")


def show_exploration(df):
    print("\n=== 1. Pierwszy rzut oka na dane ===")
    print("Rozmiar danych:", df.shape)

    print("\nTypy danych i braki:")
    df.info()

    print("\nStatystyki kolumn liczbowych:")
    print(df.describe())

    print("\nBraki danych w kolumnach:")
    print(df.isnull().sum())

    print("\nLiczba pełnych duplikatów:", df.duplicated().sum())

    for col in ["klient", "produkt", "kategoria", "miasto", "email"]:
        print(f"\nNajczęstsze wartości w kolumnie {col}:")
        print(df[col].value_counts(dropna=False).head(10))

    print(
        """

Problemy, które widać w danych:
1. Są pełne duplikaty wierszy.
2. W kolumnach tekstowych są spacje na początku albo końcu, np. przy klientach i miastach.
3. Te same wartości są zapisane różną wielkością liter, np. Laptop/laptop albo Warszawa/warszawa.
4. Daty są w dwóch formatach, więc trzeba je ujednolicić do datetime.
5. Ceny są tekstem, część ma przecinek, spacje, dopisek "zł", a część ma błędną wartość "abc".
6. Są braki w mieście, kategorii, dacie i emailu.
7. W kolumnie ilosc są wartości 0 i -1, czyli błędne zamówienia.
8. Niektóre emaile wyglądają niepoprawnie, np. "brak" albo adres bez normalnej końcówki.
"""
    )


def clean_text_title(series):
    return series.astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.title()


def parse_mixed_dates(series):
    cleaned = series.astype("string").str.strip().str.replace(r"\s+", "", regex=True)
    iso_dates = pd.to_datetime(cleaned, format="%Y-%m-%d", errors="coerce")
    pl_dates = pd.to_datetime(cleaned, format="%d.%m.%Y", errors="coerce")
    return iso_dates.fillna(pl_dates)


def clean_price(series):
    cleaned = (
        series.astype("string")
        .str.replace("zł", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def clean_data(df):
    cleaned = df.drop_duplicates().copy()

    cleaned["klient"] = clean_text_title(cleaned["klient"])
    cleaned["produkt"] = clean_text_title(cleaned["produkt"])
    cleaned["miasto"] = clean_text_title(cleaned["miasto"])
    cleaned["kategoria"] = (
        cleaned["kategoria"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

    cleaned["data_zamowienia"] = parse_mixed_dates(cleaned["data_zamowienia"])
    cleaned["cena_jednostkowa"] = clean_price(cleaned["cena_jednostkowa"])

    cleaned["miasto"] = cleaned["miasto"].fillna("unknown")
    cleaned["kategoria"] = cleaned["kategoria"].fillna("unknown")
    cleaned["email"] = cleaned["email"].astype("string").str.strip().str.lower().fillna("brak_emaila")

    cleaned = cleaned.dropna(subset=["cena_jednostkowa", "data_zamowienia"])
    cleaned = cleaned[cleaned["ilosc"] > 0].copy()

    cleaned["wartosc_zamowienia"] = cleaned["ilosc"] * cleaned["cena_jednostkowa"]
    cleaned["rok"] = cleaned["data_zamowienia"].dt.year
    cleaned["miesiac"] = cleaned["data_zamowienia"].dt.month
    cleaned["nazwa_dnia"] = cleaned["data_zamowienia"].dt.day_name()
    cleaned["email_poprawny"] = cleaned["email"].str.match(
        r"^[\w\.-]+@[\w\.-]+\.\w+$",
        na=False,
    )

    return cleaned


def analyze_data(df):
    print("\n=== 2. Dane po czyszczeniu ===")
    print("Rozmiar po czyszczeniu:", df.shape)
    print("\nBraki po czyszczeniu:")
    print(df.isnull().sum())
    print("\nPodgląd oczyszczonych danych:")
    print(df.head())

    monthly_sales = (
        df.groupby(["rok", "miesiac"], as_index=False)["wartosc_zamowienia"]
        .sum()
        .sort_values(["rok", "miesiac"])
    )

    top_clients = (
        df.groupby("klient", as_index=False)["wartosc_zamowienia"]
        .sum()
        .sort_values("wartosc_zamowienia", ascending=False)
        .head(5)
    )

    category_avg = (
        df.groupby("kategoria", as_index=False)["wartosc_zamowienia"]
        .mean()
        .sort_values("wartosc_zamowienia", ascending=False)
    )

    print("\n=== Łączna wartość zamówień w każdym miesiącu ===")
    print(monthly_sales)

    print("\n=== Top 5 klientów według wartości zamówień ===")
    print(top_clients)

    print("\n=== Średnia wartość zamówienia w każdej kategorii ===")
    print(category_avg)

    return monthly_sales, top_clients, category_avg


def create_plot(monthly_sales):
    labels = monthly_sales["rok"].astype(str) + "-" + monthly_sales["miesiac"].astype(str).str.zfill(2)

    plt.figure(figsize=(11, 6))
    plt.bar(labels, monthly_sales["wartosc_zamowienia"], color="#2F7D6D")
    plt.title("Łączna wartość zamówień w każdym miesiącu")
    plt.xlabel("Miesiąc")
    plt.ylabel("Wartość zamówień")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=150)
    plt.close()

    print(f"\nWykres zapisany do pliku: {PLOT_FILE}")


def main():
    generate_messy_data()

    df_messy = pd.read_csv(MESSY_FILE)
    show_exploration(df_messy)

    df_clean = clean_data(df_messy)
    monthly_sales, _, _ = analyze_data(df_clean)

    create_plot(monthly_sales)
    df_clean.to_csv(CLEAN_FILE, index=False)
    print(f"Oczyszczone dane zapisane do pliku: {CLEAN_FILE}")


if __name__ == "__main__":
    main()
