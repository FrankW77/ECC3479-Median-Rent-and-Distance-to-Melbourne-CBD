from pathlib import Path

import pandas as pd

from data_cleaning_utils import coerce_numeric, find_column, is_non_lga_name, normalize_lga_name, standardize_columns

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"


def clean_schools_data():
    source_path = RAW_DIR / "schools_by_lga.xlsx"
    df = pd.read_excel(source_path, sheet_name="LGA Data", engine="openpyxl", header=10, dtype=str)
    df = standardize_columns(df)

    lga_col = find_column(df.columns, "row_labels", "lga_name", "local_government_area", "lga")
    independent_col = find_column(df.columns, "sum_of_no_of_schools_2", "independent_schools")
    total_col = find_column(df.columns, "unnamed_8", "total_schools")

    df = df[[lga_col, independent_col, total_col]].rename(
        columns={
            lga_col: "lga_name",
            independent_col: "independent_schools",
            total_col: "total_schools",
        }
    )

    df["independent_schools"] = coerce_numeric(df["independent_schools"])
    df["total_schools"] = coerce_numeric(df["total_schools"])

    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df.dropna(subset=["lga_name"]).copy()
    df = df[~df["lga_name"].map(is_non_lga_name)]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "schools_clean.csv", index=False)


if __name__ == "__main__":
    clean_schools_data()