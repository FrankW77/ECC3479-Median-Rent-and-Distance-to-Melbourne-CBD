from pathlib import Path

import pandas as pd

from data_cleaning_utils import (
    coerce_numeric,
    find_column,
    is_non_lga_name,
    normalize_column_name,
    normalize_lga_name,
    standardize_columns,
)

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"


def clean_crime_data():
    source_path = RAW_DIR / "crime_by_lga.xlsx"
    workbook = pd.ExcelFile(source_path, engine="openpyxl")
    sheet_name = next(
        (sheet for sheet in workbook.sheet_names if normalize_column_name(sheet) == "table_01"),
        workbook.sheet_names[0],
    )

    df = pd.read_excel(workbook, sheet_name=sheet_name, dtype=str)
    df = standardize_columns(df)

    lga_col = find_column(df.columns, "local_government_area", "local_government", "lga_name", "lga")
    year_col = find_column(df.columns, "year")
    offence_col = find_column(df.columns, "offence_count", "offence count", "offences")

    df = df[[lga_col, year_col, offence_col]].rename(
        columns={
            lga_col: "lga_name",
            year_col: "year",
            offence_col: "offence_count",
        }
    )

    df["offence_count"] = coerce_numeric(df["offence_count"])
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df.dropna(subset=["lga_name", "year", "offence_count"]).copy()
    df["year"] = df["year"].astype(int)
    df = df[~df["lga_name"].map(is_non_lga_name)]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "crime_clean.csv", index=False)

    print("✓ Clean crime dataset saved to Data/clean/crime_clean.csv")


if __name__ == "__main__":
    clean_crime_data()