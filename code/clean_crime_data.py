from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"

def clean_crime_data():

    # Load the correct sheet (based on your screenshot: "Table 01")
    df = pd.read_excel(
        RAW_DIR / "crime_by_lga.xlsx",
        sheet_name="Table 01",
        engine="openpyxl",
        dtype=str
    )

    # Standardise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Rename the columns we need
    df = df.rename(columns={
        "local_government_area": "lga_name",
        "year": "year",
        "offence_count": "offence_count"
    })

    # Keep only the three required columns
    df = df[["lga_name", "year", "offence_count"]]

    # Convert offence_count to numeric
    df["offence_count"] = (
        df["offence_count"]
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # Convert year to integer
    df["year"] = df["year"].astype(int)

    # Drop totals or non-LGA rows
    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df[~df["lga_name"].map(is_non_lga_name)]

    # Save cleaned file
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "crime_clean.csv", index=False)

    print("✓ Clean crime dataset saved to Data/clean/crime_clean.csv")


if __name__ == "__main__":
    clean_crime_data()