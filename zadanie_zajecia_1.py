import os
import sqlite3

os.environ.setdefault("MPLCONFIGDIR", ".matplotlib")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = (
    "https://restcountries.com/v3.1/all"
    "?fields=name,capital,region,subregion,population,area,currencies"
)
DATABASE_FILE = "kraje_swiata.db"
TABLE_NAME = "kraje"
PLOT_FILE = "populacja_regionow.png"
POLAND_AREA_KM2 = 312_679


def first_item(value):
    """Zwraca pierwszy element listy albo None, gdy lista jest pusta."""
    if isinstance(value, list) and value:
        return value[0]
    return None


def get_currency(currencies_dict):
    """Wyciąga kod pierwszej waluty z pola currencies."""
    if isinstance(currencies_dict, dict) and currencies_dict:
        return list(currencies_dict.keys())[0]
    return None


def fetch_countries():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def build_dataframe(data):
    rows = []

    for country in data:
        rows.append(
            {
                "nazwa": country.get("name", {}).get("common"),
                "stolica": first_item(country.get("capital")),
                "region": country.get("region"),
                "subregion": country.get("subregion"),
                "populacja": country.get("population"),
                "powierzchnia": country.get("area"),
                "waluta": get_currency(country.get("currencies")),
            }
        )

    df = pd.DataFrame(rows)
    df = df.sort_values("nazwa").reset_index(drop=True)
    return df


def save_to_sqlite(df):
    conn = sqlite3.connect(DATABASE_FILE)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    return conn


def print_dataframe_overview(df):
    print("=== Podgląd danych: head() ===")
    print(df.head())
    print("\n=== Rozmiar DataFrame: shape ===")
    print(df.shape)
    print("\n=== Typy danych: dtypes ===")
    print(df.dtypes)


def run_sql_analysis(conn):
    queries = {
        "1. Łączna populacja świata": """
            SELECT SUM(populacja) AS laczna_populacja_swiata
            FROM kraje
        """,
        "2. 10 krajów z największą populacją": """
            SELECT nazwa, region, populacja
            FROM kraje
            ORDER BY populacja DESC
            LIMIT 10
        """,
        "3. Liczba krajów i średnia populacja w regionach": """
            SELECT
                region,
                COUNT(*) AS liczba_krajow,
                ROUND(AVG(populacja), 0) AS srednia_populacja
            FROM kraje
            GROUP BY region
            ORDER BY liczba_krajow DESC
        """,
        "4. Kraje o powierzchni większej niż Polska": f"""
            SELECT nazwa, region, powierzchnia
            FROM kraje
            WHERE powierzchnia > {POLAND_AREA_KM2}
            ORDER BY powierzchnia DESC
        """,
        "5. Kraj z najwyższą gęstością zaludnienia": """
            SELECT
                nazwa,
                region,
                populacja,
                powierzchnia,
                ROUND(populacja / powierzchnia, 2) AS gestosc_zaludnienia
            FROM kraje
            WHERE powierzchnia > 0
            ORDER BY gestosc_zaludnienia DESC
            LIMIT 1
        """,
    }

    for title, query in queries.items():
        print(f"\n=== {title} ===")
        result = pd.read_sql_query(query, conn)
        print(result)


def create_population_plot(conn):
    df_regiony = pd.read_sql_query(
        """
        SELECT
            region,
            SUM(populacja) AS laczna_populacja
        FROM kraje
        GROUP BY region
        ORDER BY laczna_populacja DESC
        """,
        conn,
    )

    plt.figure(figsize=(10, 6))
    plt.bar(df_regiony["region"], df_regiony["laczna_populacja"])
    plt.title("Łączna populacja według regionu świata")
    plt.xlabel("Region")
    plt.ylabel("Populacja")
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(PLOT_FILE, dpi=150)
    plt.close()

    print(f"\nWykres zapisano do pliku: {PLOT_FILE}")


def main():
    data = fetch_countries()
    df = build_dataframe(data)

    print_dataframe_overview(df)

    conn = save_to_sqlite(df)
    print(f"\nDane zapisano w bazie: {DATABASE_FILE}, tabela: {TABLE_NAME}")

    run_sql_analysis(conn)
    create_population_plot(conn)

    conn.close()


if __name__ == "__main__":
    main()
