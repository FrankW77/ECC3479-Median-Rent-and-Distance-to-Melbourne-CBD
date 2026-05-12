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


def clean_distance_data():
    source_path = RAW_DIR / "distance_by_lga.xlsx"
    df = pd.read_excel(source_path, sheet_name=0, engine="openpyxl")
    df = standardize_columns(df)

    lga_col = find_column(df.columns, "local_government_area", "local_government", "lga_name", "lga")
    address_col = find_column(df.columns, "council_address", "address")
    suburb_col = find_column(df.columns, "suburb")
    latitude_col = find_column(df.columns, "latitude")
    longitude_col = find_column(df.columns, "longitude")
    straight_line_col = find_column(
        df.columns,
        "straight_line_distance_to_melbourne_cbd_kilometres",
        "straight_line_distance",
        "straight_line_km",
    )
    driving_col = find_column(
        df.columns,
        "driving_distance_kilometres_using_most_direct_route",
        "driving_distance",
        "driving_km",
    )

    df = df[[lga_col, address_col, suburb_col, latitude_col, longitude_col, straight_line_col, driving_col]].rename(
        columns={
            lga_col: "lga_name",
            address_col: "address",
            suburb_col: "suburb",
            latitude_col: "latitude",
            longitude_col: "longitude",
            straight_line_col: "straight_line_km",
            driving_col: "driving_km",
        }
    )

    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df.dropna(subset=["lga_name"]).copy()
    df = df[~df["lga_name"].map(is_non_lga_name)]

    for column in ["latitude", "longitude", "straight_line_km", "driving_km"]:
        df[column] = coerce_numeric(df[column])

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_DIR / "distance_clean.csv", index=False)


if __name__ == "__main__":
    clean_distance_data()