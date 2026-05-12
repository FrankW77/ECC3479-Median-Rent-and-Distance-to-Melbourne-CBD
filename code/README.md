# Data Cleaning Scripts

This directory contains Python scripts for cleaning and preparing raw data for analysis.

## Execution Order

The scripts must be run in the following order to create the final analysis dataset:

### Stage 1: Clean Individual Datasets
1. **`clean_rent_data.py`** → produces `Data/clean/median_rent_clean.csv`
   - Input: Raw median rent data (Excel)
   - Output: LGA-level median rent, aggregated across years
   
2. **`clean_crime_data.py`** → produces `Data/clean/crime_clean.csv`
   - Input: Raw crime data (offence counts by LGA and year)
   - Output: LGA-level offence counts, aggregated across years
   
3. **`clean_distance_data.py`** → produces `Data/clean/distance_clean.csv`
   - Input: Raw LGA coordinates and geocoding
   - Output: Straight-line distance from each LGA to Melbourne CBD
   
4. **`clean_schools_data.py`** → produces `Data/clean/schools_clean.csv`
   - Input: Raw school data (total schools, independent schools by LGA)
   - Output: LGA-level school counts
   
5. **`clean_health_data.py`** → produces `Data/clean/health_clean.csv`
   - Input: Raw health facility data (GP clinics, allied health, etc. by LGA)
   - Output: LGA-level health access measures (facilities per 1,000 residents)

### Stage 2: Merge All Data
6. **`clean_and_merge_data.py`** → produces `Data/clean/final_panel.csv`
   - Input: All cleaned datasets from steps 1–5
   - Output: LGA-year-level panel with all variables ready for analysis

## Utilities

- **`data_cleaning_utils.py`**: Shared helper functions (e.g., LGA name standardization, geocoding)
- **`debug_distance_columns.py`**: Diagnostic script for distance calculations
- **`debug_excel.py`**: Diagnostic script for Excel file inspection
- **`run_regression.py`**: (Deprecated) Old regression runner; use notebooks instead

## Running the Full Pipeline

To reproduce the analysis from raw data:

```bash
cd /path/to/ECC3479-Median-Rent
python code/clean_rent_data.py
python code/clean_crime_data.py
python code/clean_distance_data.py
python code/clean_schools_data.py
python code/clean_health_data.py
python code/clean_and_merge_data.py

# Then run the analysis notebooks:
jupyter notebook outputs/Primary\ Econometric\ Analysis.ipynb
jupyter notebook outputs/robustness_analysis/robustness_analysis.ipynb
```

## Notes

- All scripts assume the raw data files are in `Data/raw/` as specified in `Data/raw/README.md`
- Output CSVs are saved to `Data/clean/`
- Scripts handle missing values, standardize LGA names, and perform basic validation checks
- Console output includes progress messages and summary statistics
