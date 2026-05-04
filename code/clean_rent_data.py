from pathlib import Path

import pandas as pd

from data_cleaning_utils import coerce_numeric, is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"


def clean_rent_data():
    df = pd.read_excel(
        RAW_DIR / "median_rent_by_lga.xlsx",
        sheet_name="All Properties",
        skiprows=1,
        header=[0, 1],
        engine="openpyxl",
        dtype=str,
    )

    # Flatten the two header rows into a single set of readable column names.
    df.columns = [
        "_".join(str(part).strip() for part in pair if str(part).strip().lower() != "nan")
        for pair in df.columns
    ]

    df = df.rename(columns={df.columns[1]: "lga_name"})
    df = df.drop(columns=[df.columns[0]])
    df["lga_name"] = df["lga_name"].ffill()
    df = df[~df["lga_name"].str.contains("Group Total", na=False)].copy()

    median_cols = [column for column in df.columns if column.endswith("_Median")]
    df_long = df.melt(
        id_vars=["lga_name"],
        value_vars=median_cols,
        var_name="quarter",
        value_name="median_rent",
    )

    df_long["quarter"] = df_long["quarter"].str.replace("_Median", "", regex=False)
    df_long["median_rent"] = coerce_numeric(df_long["median_rent"])
    df_long["year"] = pd.to_numeric(df_long["quarter"].str[-2:], errors="coerce")
    df_long["year"] = df_long["year"].apply(lambda value: 2000 + value if value < 50 else 1900 + value)

    df_final = df_long[["lga_name", "year", "median_rent"]].dropna().copy()
    df_final["year"] = df_final["year"].astype(int)
    df_final["lga_name"] = df_final["lga_name"].map(normalize_lga_name)
    df_final = df_final.dropna(subset=["lga_name"])
    df_final = df_final[~df_final["lga_name"].map(is_non_lga_name)]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(CLEAN_DIR / "median_rent_clean.csv", index=False)

    print("✓ Clean rental dataset saved to Data/clean/median_rent_clean.csv")


if __name__ == "__main__":
    clean_rent_data()