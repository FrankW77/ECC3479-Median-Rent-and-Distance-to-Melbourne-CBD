from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def inspect_excel(path):
    print(f"\nInspecting: {path}")

    xls = pd.ExcelFile(path)

    print("\n--- SHEETS FOUND ---")
    print(xls.sheet_names)
    print("--------------------\n")

    for sheet in xls.sheet_names:
        print(f"\n--- FIRST 20 ROWS OF SHEET: {sheet} ---")
        df = pd.read_excel(xls, sheet_name=sheet, header=None)
        print(df.head(20))
        print("----------------------------------------\n")


if __name__ == "__main__":
    inspect_excel(ROOT / "Data" / "raw" / "distance_by_lga.xlsx")