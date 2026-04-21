from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "Data" / "raw"
CLEAN_DIR = ROOT / "Data" / "clean"

def clean_distance_data():

    # Load the correct distance file
    df = pd.read_excel(
        RAW_DIR / "distance_by_lga.xlsx",
        sheet_name=0,
        engine="openpyxl"
    )

    # Standardise column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )

    print("COLUMNS AFTER CLEANING:")
    print(df.columns.tolist())

    # Rename columns based on your distance dataset
    df = df.rename(columns={
        "local_government": "lga_name",
        "local_government_area": "lga_name",
        "council_address": "address",
        "suburb": "suburb",
        "latitude": "latitude",
        "longitude": "longitude",
        "straight_line_distance_to_melbourne_cbd_kilometres": "straight_line_km",
        "driving_distance_kilometres_using_most_direct_route": "driving_km"
    })

    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df[~df["lga_name"].map(is_non_lga_name)]

    # Convert numeric columns
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["straight_line_km"] = df["straight_line_km"].astype(float)
    df["driving_km"] = df["driving_km"].astype(float)

    # Save clean file
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "distance_clean.csv", index=False)
    print("✓ Clean distance dataset saved to Data/clean/distance_clean.csv")


if __name__ == "__main__":
    clean_distance_data()