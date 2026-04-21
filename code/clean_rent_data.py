from pathlib import Path

import pandas as pd

from data_cleaning_utils import is_non_lga_name, normalize_lga_name

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
        dtype=str
    )

    # ---------------------------------------------------------
    # 1. FLATTEN MULTI-INDEX COLUMNS
    # ---------------------------------------------------------
    df.columns = [
        f"{str(a).strip()}_{str(b).strip()}" if str(b) != "nan" else str(a).strip()
        for a, b in df.columns
    ]

    # ---------------------------------------------------------
    # 2. RENAME THE CORRECT LGA COLUMN
    #    Column 0 = Region
    #    Column 1 = LGA (the one we want)
    # ---------------------------------------------------------
    df = df.rename(columns={
        df.columns[1]: "lga_name"   # <--- USE COLUMN 1, NOT COLUMN 0
    })

    # ---------------------------------------------------------
    # 3. DROP THE REGION COLUMN ENTIRELY
    # ---------------------------------------------------------
    df = df.drop(columns=[df.columns[0]])

    # ---------------------------------------------------------
    # 4. FORWARD-FILL LGA NAMES (merged cells)
    # ---------------------------------------------------------
    df["lga_name"] = df["lga_name"].ffill()

    # ---------------------------------------------------------
    # 5. REMOVE GROUP TOTAL ROWS
    # ---------------------------------------------------------
    df = df[~df["lga_name"].str.contains("Group Total", na=False)]

    # ---------------------------------------------------------
    # 6. KEEP ONLY MEDIAN COLUMNS
    # ---------------------------------------------------------
    median_cols = [c for c in df.columns if c.endswith("_Median")]

    # ---------------------------------------------------------
    # 7. RESHAPE WIDE → LONG
    # ---------------------------------------------------------
    df_long = df.melt(
        id_vars=["lga_name"],
        value_vars=median_cols,
        var_name="quarter",
        value_name="median_rent"
    )

    # ---------------------------------------------------------
    # 8. CLEAN QUARTER LABELS
    # ---------------------------------------------------------
    df_long["quarter"] = df_long["quarter"].str.replace("_Median", "", regex=False)

    # ---------------------------------------------------------
    # 9. CLEAN MEDIAN RENT VALUES
    # ---------------------------------------------------------
    df_long["median_rent"] = (
        df_long["median_rent"]
        .str.replace(r"[\$,]", "", regex=True)
        .replace("-", pd.NA)
        .replace("", pd.NA)
        .astype(float)
    )

    # ---------------------------------------------------------
    # 10. EXTRACT YEAR
    # ---------------------------------------------------------
    df_long["year"] = df_long["quarter"].str[-2:].astype(int)
    df_long["year"] = df_long["year"].apply(lambda x: 2000 + x if x < 50 else 1900 + x)

    # ---------------------------------------------------------
    # 11. FINAL CLEAN DATAFRAME
    # ---------------------------------------------------------
    df_final = df_long[["lga_name", "year", "median_rent"]].dropna()
    df_final["lga_name"] = df_final["lga_name"].map(normalize_lga_name)
    df_final = df_final[~df_final["lga_name"].map(is_non_lga_name)]

    # ---------------------------------------------------------
    # 12. SAVE CLEAN FILE
    # ---------------------------------------------------------
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(CLEAN_DIR / "median_rent_clean.csv", index=False)

    print("✓ Clean rental dataset saved to Data/clean/median_rent_clean.csv")


if __name__ == "__main__":
    clean_rent_data()