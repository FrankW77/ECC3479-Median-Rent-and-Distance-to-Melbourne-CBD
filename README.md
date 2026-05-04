# ECC3479 – Rental Prices and Distance to Melbourne CBD

## Overview
This project investigates the relationship between proximity to Melbourne CBD and median rental prices across metropolitan LGAs. The analysis is **descriptive**: we report conditional correlations and associations, not causal treatment effects.

---

## Quick Start: Run the Analysis

### Option 1: Jupyter Notebook (Recommended for exploratory review)
```bash
# Install dependencies
pip install -r requirements.txt

# Open the Jupyter notebook
jupyter notebook EDA/eda_analysis.ipynb
```
The notebook contains:
- Data loading and structure checks
- Exploratory data analysis (distributions, correlations)
- Regression analysis with econometric specification
- Explicit declaration of descriptive vs. causal ambition
- Formatted regression table and coefficient interpretation
- Limitations and threats to inference

### Option 2: Command-line pipeline (Reproducible batch processing)
```bash
# 1. Clean individual datasets
python code/clean_rent_data.py
python code/clean_schools_data.py
python code/clean_health_data.py
python code/clean_crime_data.py
python code/clean_distance_data.py

# 2. Merge all cleaned data
python code/clean_and_merge_data.py

# 3. Run regression analysis
python code/run_regression.py
```
Results are written to `outputs/` directory.

---

## Repository Structure

```
ECC3479-Median-Rent/
├── README.md                        # This file
├── requirements.txt                 # Python package dependencies
│
├── Data/
│   ├── raw/                         # Original Excel files (immutable)
│   │   └── README.md                # Data sources and variable definitions
│   └── clean/                       # Cleaned CSV files (produced by scripts)
│       ├── final_panel.csv          # Main analysis dataset
│       ├── median_rent_clean.csv
│       ├── crime_clean.csv
│       ├── distance_clean.csv
│       ├── schools_clean.csv
│       └── health_clean.csv
│
├── code/                            # Python scripts (executed in order below)
│   ├── clean_rent_data.py
│   ├── clean_crime_data.py
│   ├── clean_distance_data.py
│   ├── clean_health_data.py
│   ├── clean_schools_data.py
│   ├── data_cleaning_utils.py       # Shared utilities
│   ├── clean_and_merge_data.py      # Merge cleaned data into panel
│   └── run_regression.py            # Regression analysis script
│
├── EDA/
│   └── eda_analysis.ipynb           # PRIMARY ANALYSIS FILE
│                                    # Exploratory Data Analysis + Regression
│                                    # Spec, interpretation, limitations all included
│
└── outputs/
    ├── regression_results.csv       # Coefficient table (tidy format)
    └── regression_results.txt       # Full regression summary
```

---

## Methodological Declaration

**Analysis Type: DESCRIPTIVE**

We estimate the unconditional correlation between distance to Melbourne CBD and median rental prices. We do **not** attempt to identify a causal treatment effect. This is a straightforward report of associations across Local Government Areas.

---

## Econometric Specification

**Main Model (between-LGA OLS):**
$$\overline{\text{median\_rent}}_{i} = \beta_0 + \beta_1 \cdot \overline{\text{distance}}_{i} + \varepsilon_{i}$$

where the overbar denotes the LGA-level mean after aggregating across years.

**Key Details:**
- **Outcome:** Mean median weekly rent by LGA (AUD)
- **Regressor:** Mean straight-line distance from LGA centroid to Melbourne CBD (km)
- **Sample:** LGAs with both rent and distance data present after aggregation
- **N:** 31 LGAs with distance data
- **Standard Errors:** Plain OLS on one observation per LGA
- **Functional Form:** Linear, with a log-linear robustness check in the notebook

**Specification Rationale:**
We collapse the panel to the LGA level because distance does not vary within an LGA. This makes the coefficient easier to interpret as a between-LGA rent gradient and avoids giving the regression artificial within-LGA precision.

---

## Main Results Summary

**Coefficient on Distance (Linear Model, N=31 LGAs):**
- **-$1.45 per week per km** (95% CI: -$2.41 to -$0.48)
- **t-stat:** -3.06, **p-value:** 0.0047
- **R²:** 0.244 (distance explains about 24% of between-LGA variation in mean median rent)

**Interpretation:**
For each additional kilometer from the CBD, mean median rent **decreases by approximately $1.45/week** (~$75/year). An LGA 10 km farther away has mean rent about $14.50/week lower.

**Robustness (Log-linear model):**
The notebook’s log-linear check shows a similarly negative gradient: about **-0.41% per km** (p = 0.0038).

---

## Limitations & Threats (Descriptive Standards)

Since we claim descriptive rather than causal inference, we acknowledge but do not attempt to resolve confounding:

1. **Omitted Amenities / Confounders** (Primary threat)
   - Crime, school quality, employment density, and local services are correlated with both distance and rent
   - Our coefficient absorbs these effects; direction ambiguous

2. **Structural Missingness**
   - Distance data available only for ~60% of Victorian LGAs (metropolitan subset)
   - Results do not generalize to rural Victoria

3. **Measurement Error**
   - Distance = centroid-to-centroid; within-LGA heterogeneity ignored
   - Rent = LGA median; individual-level variation not captured
   - Classical measurement error would attenuate the distance coefficient

4. **Temporal Aggregation**
   - No fixed effects; relies on between-LGA variation
   - Within-LGA changes over time (e.g., gentrification) not modeled

**Conclusion:**
The negative distance-rent association is robust and genuinely descriptive—farther LGAs do have lower median rents. However, the mechanisms (distance → amenities → rent vs. distance ← amenities ← rent) remain unidentified and are beyond the scope of descriptive analysis.

---

## How to Reproduce

### 1. **Environment Setup**
```bash
# Install Python 3.11+
python --version

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. **Raw Data**
Ensure the following files exist in `Data/raw/`:
- `median_rent_by_lga.xlsx`
- `crime_by_lga.xlsx`
- `distance_by_lga.xlsx`
- `schools_by_lga.xlsx`
- `health_by_lga.xlsx`

(See `Data/raw/README.md` for sources)

### 3. **Run Data Pipeline**
```bash
# Run these from the repository root
python code/clean_rent_data.py
python code/clean_crime_data.py
python code/clean_distance_data.py
python code/clean_health_data.py
python code/clean_schools_data.py
python code/clean_and_merge_data.py
```
Check `Data/clean/` for output CSVs.

### 4. **Run Analysis**

**Option A: Jupyter (Interactive)**
```bash
jupyter notebook EDA/eda_analysis.ipynb
```
- Run all cells to generate tables, plots, and regression results
- Output displays inline

**Option B: Python (Batch)**
```bash
# Run from the repository root
python code/run_regression.py
```
- Produces `outputs/regression_results.txt` and `outputs/regression_results.csv`

---

## Software & Dependencies

**Python Version:** 3.11+

**Key Packages:**
- `pandas` – data manipulation
- `numpy` – numerical computing
- `matplotlib`, `seaborn` – visualization
- `statsmodels` – OLS regression, inference, clustered SE
- `jupyter` – notebook interface

See `requirements.txt` for full list.

---

## Files Generated

After running the pipeline:

```
Data/clean/
├── final_panel.csv              # Merged analysis dataset
├── median_rent_clean.csv
├── crime_clean.csv
├── distance_clean.csv
├── schools_clean.csv
└── health_clean.csv

outputs/
├── regression_results.csv       # Coefficient table
└── regression_results.txt       # Full OLS summary
```

---

## Key Findings at a Glance

| Finding | Value |
|---------|-------|
| Sample size (LGAs) | 31 LGAs with distance data |
| Distance coefficient | -$1.45 / week / km |
| t-statistic | -3.06 (p = 0.0047) |
| R² | 0.244 |
| Effect size (10 km farther) | -$14.50 / week (~$750/year) |
| Semi-elasticity | -0.41% per km |
| Conclusion | Significant negative distance gradient; descriptive analysis of between-LGA variation |

---

## Documentation

- [Data Dictionary](Data/raw/README.md) – Raw data sources and variable definitions
- [Notebook](EDA/eda_analysis.ipynb) – Full analysis, interpretation, and limitations
- [Code](code/) – Cleaning and regression scripts with inline comments
- pandas
- numpy
- matplotlib
- seaborn
- statsmodels
- linearmodels
- requests
Exact versions are listed in requirements.txt.

Manual Steps (Outside of Code)
- Download raw Excel datasets from official sources
- Place them unchanged into data/raw/
- Verify that the column names match those expected by the cleaning scripts
- Optionally inspect outputs in data/clean/ and outputs/ after running scripts

AI Use
Some parts of this project (e.g. code structure and debugging assistance) were supported by Microsoft Copilot. All analysis, interpretation and final decisions were made by the author. 

Contact
For questions about reproducibility, data structure, or workflow, please contact the author.
