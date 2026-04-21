from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"

def clean_schools_data():

    # Load sheet with correct header row (row 10)
    df = pd.read_excel(
        RAW_DIR / "schools_by_lga.xlsx",
        sheet_name="LGA Data",
        engine="openpyxl",
        header=10,
        dtype=str
    )

    # Rename columns explicitly based on detected names
    df = df.rename(columns={
        "Row Labels": "lga_name",
        "Sum of No Of Schools.2": "independent_schools",
        "Unnamed: 8": "total_schools"
    })

    # Keep only the required columns
    df = df[["lga_name", "independent_schools", "total_schools"]]

    # Clean numeric columns
    df["independent_schools"] = df["independent_schools"].replace("-", "0").astype(float)
    df["total_schools"] = df["total_schools"].replace("-", "0").astype(float)

    # Drop totals or blank rows
    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df[df["lga_name"].notna()]
    df = df[~df["lga_name"].map(is_non_lga_name)]

    # Save cleaned file
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "schools_clean.csv", index=False)

    print("✓ Clean schools dataset saved to Data/clean/schools_clean.csv")


if __name__ == "__main__":
    clean_schools_data()