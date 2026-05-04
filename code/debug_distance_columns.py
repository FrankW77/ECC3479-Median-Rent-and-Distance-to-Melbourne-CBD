from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

xls = pd.ExcelFile(ROOT / "Data" / "raw" / "distance_by_lga.xlsx")
print(xls.sheet_names)