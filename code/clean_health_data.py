from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"

def clean_health_data():

    # Load the health dataset (replace sheet_name if needed)
    df = pd.read_excel(
        RAW_DIR / "health_by_lga.xlsx",
        sheet_name="LGAs",
        engine="openpyxl",
        dtype=str
    )

    # Standardise column names
    df.columns = df.columns.str.strip().str.lower()

    # Identify columns using partial matching
    lga_col = [c for c in df.columns if "lga" in c][0]
    gp_clinics_col = [c for c in df.columns if "general practice clinics" in c][0]
    allied_col = [c for c in df.columns if "allied health service sites" in c][0]
    dental_col = [c for c in df.columns if "dental service sites" in c][0]
    pharmacy_col = [c for c in df.columns if "pharmacies" in c][0]
    acsc_col = [c for c in df.columns if "acsc" in c][0]

    # Rename columns
    df = df.rename(columns={
        lga_col: "lga_name",
        gp_clinics_col: "gp_clinics_per_1000",
        allied_col: "allied_health_per_1000",
        dental_col: "dental_sites_per_1000",
        pharmacy_col: "pharmacies_per_1000",
        acsc_col: "acsc_per_1000"
    })

    # Keep only required columns
    df = df[[
        "lga_name",
        "gp_clinics_per_1000",
        "allied_health_per_1000",
        "dental_sites_per_1000",
        "pharmacies_per_1000",
        "acsc_per_1000"
    ]]

    # Convert numeric columns
    numeric_cols = [
        "gp_clinics_per_1000",
        "allied_health_per_1000",
        "dental_sites_per_1000",
        "pharmacies_per_1000",
        "acsc_per_1000"
    ]

    for col in numeric_cols:
        df[col] = df[col].replace("-", "0").astype(float)

    # Drop blank rows
    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df[df["lga_name"].notna()]
    df = df[~df["lga_name"].map(is_non_lga_name)]

    # Save cleaned file
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "health_clean.csv", index=False)

    print("✓ Clean health dataset saved to Data/clean/health_clean.csv")


if __name__ == "__main__":
    clean_health_data()