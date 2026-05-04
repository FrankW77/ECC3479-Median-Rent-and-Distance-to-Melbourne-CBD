from pathlib import Path

import pandas as pd

from data_cleaning_utils import (
    coerce_numeric,
    find_column,
    is_non_lga_name,
    normalize_lga_name,
    standardize_columns,
)

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"


def clean_health_data():
    source_path = RAW_DIR / "health_by_lga.xlsx"
    df = pd.read_excel(source_path, sheet_name="LGAs", engine="openpyxl", dtype=str)
    df = standardize_columns(df)

    lga_col = find_column(df.columns, "lga", "local_government_area", "local_government")
    gp_clinics_col = find_column(df.columns, "general_practice_clinics", "general practice clinics")
    allied_col = find_column(df.columns, "allied_health_service_sites", "allied health service sites")
    dental_col = find_column(df.columns, "dental_service_sites", "dental service sites")
    pharmacy_col = find_column(df.columns, "pharmacies")
    acsc_col = find_column(df.columns, "acsc")

    df = df[[lga_col, gp_clinics_col, allied_col, dental_col, pharmacy_col, acsc_col]].rename(
        columns={
            lga_col: "lga_name",
            gp_clinics_col: "gp_clinics_per_1000",
            allied_col: "allied_health_per_1000",
            dental_col: "dental_sites_per_1000",
            pharmacy_col: "pharmacies_per_1000",
            acsc_col: "acsc_per_1000",
        }
    )

    for column in [
        "gp_clinics_per_1000",
        "allied_health_per_1000",
        "dental_sites_per_1000",
        "pharmacies_per_1000",
        "acsc_per_1000",
    ]:
        df[column] = coerce_numeric(df[column])

    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df.dropna(subset=["lga_name"]).copy()
    df = df[~df["lga_name"].map(is_non_lga_name)]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "health_clean.csv", index=False)

    print("✓ Clean health dataset saved to Data/clean/health_clean.csv")


if __name__ == "__main__":
    clean_health_data()