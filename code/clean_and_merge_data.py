from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

ROOT = Path(__file__).resolve().parents[1]
CLEAN_DIR = ROOT / "Data" / "clean"

def standardise_lga_column(df):
    """
    Detects the LGA column in any dataset and renames it to lga_name.
    """
    possible_cols = [
        "lga_name",
        "local_government_area",
        "local_government",
        "lga",
        "lga_code",
        "area_name",
        "council",
        "local government area",
        "Local Government Area",
    ]

    df_cols_lower = {c.lower(): c for c in df.columns}

    for col in possible_cols:
        if col.lower() in df_cols_lower:
            df = df.rename(columns={df_cols_lower[col.lower()]: "lga_name"})
            return df

    raise KeyError(f"No LGA column found. Columns were: {df.columns.tolist()}")


def expand_cross_section(df, years):
    """
    Expands a cross-sectional dataset (no year column) across all years.
    """
    expanded = []
    for y in years:
        temp = df.copy()
        temp["year"] = y
        expanded.append(temp)
    return pd.concat(expanded, ignore_index=True)


def clean_lga_frame(df):
    df = df.copy()
    df["lga_name"] = df["lga_name"].map(normalize_lga_name)
    df = df[~df["lga_name"].map(is_non_lga_name)]
    return df


def clean_and_merge():

    # -----------------------------------
    # 1. Load cleaned datasets
    # -----------------------------------
    rent = pd.read_csv(CLEAN_DIR / "median_rent_clean.csv")
    crime = pd.read_csv(CLEAN_DIR / "crime_clean.csv")
    schools = pd.read_csv(CLEAN_DIR / "schools_clean.csv")
    health = pd.read_csv(CLEAN_DIR / "health_clean.csv")
    distance = pd.read_csv(CLEAN_DIR / "distance_clean.csv")

    print("RENT COLUMNS:", rent.columns.tolist())
    print("CRIME COLUMNS:", crime.columns.tolist())
    print("SCHOOLS COLUMNS:", schools.columns.tolist())
    print("HEALTH COLUMNS:", health.columns.tolist())
    print("DISTANCE COLUMNS:", distance.columns.tolist())

    # -----------------------------------
    # 2. Expand cross-sectional datasets
    # -----------------------------------
    years = rent["year"].unique()

    # Schools has no year column → expand
    if "year" not in schools.columns:
        schools = expand_cross_section(schools, years)

    # Health has no year column → expand
    if "year" not in health.columns:
        health = expand_cross_section(health, years)

    # -----------------------------------
    # 3. Standardise LGA column names
    # -----------------------------------
    rent = standardise_lga_column(rent)
    crime = standardise_lga_column(crime)
    schools = standardise_lga_column(schools)
    health = standardise_lga_column(health)
    distance = standardise_lga_column(distance)

    # -----------------------------------
    # 4. Standardise LGA formatting
    # -----------------------------------
    rent = clean_lga_frame(rent)
    crime = clean_lga_frame(crime)
    schools = clean_lga_frame(schools)
    health = clean_lga_frame(health)
    distance = clean_lga_frame(distance)

    # -----------------------------------
    # 5. Merge datasets
    # -----------------------------------
    merged = rent.merge(crime, on=["lga_name", "year"], how="left")
    merged = merged.merge(schools, on=["lga_name", "year"], how="left")
    merged = merged.merge(health, on=["lga_name", "year"], how="left")
    merged = merged.merge(distance, on="lga_name", how="left")

    # -----------------------------------
    # 6. Sort and save
    # -----------------------------------
    merged = merged.sort_values(["lga_name", "year"]).reset_index(drop=True)
    merged.to_csv(CLEAN_DIR / "final_panel.csv", index=False)

    missing_pct = (merged.isna().mean() * 100).sort_values(ascending=False)
    print("\nMissing values in final merged panel (%):")
    print(missing_pct.round(2).to_string())

    print("\n✓ Final merged dataset saved to Data/clean/final_panel.csv")


if __name__ == "__main__":
    clean_and_merge()