# ECC3479 – Rental Prices and Distance to Melbourne CBD

## Overview
This project examines how median rental prices vary with distance from Melbourne CBD across metropolitan LGAs. The analysis is descriptive: it summarizes associations rather than estimating a causal effect.

---

## Complete Analysis Pipeline

The analysis proceeds in three stages: data cleaning, primary analysis, and robustness checks. This repository contains the scripts and notebooks required to reproduce the results.

### Stage 1: Data Cleaning and Preparation
```bash
cd code/
python clean_rent_data.py
python clean_crime_data.py
python clean_distance_data.py
python clean_schools_data.py
python clean_health_data.py
python clean_and_merge_data.py
```
Output: `Data/clean/final_panel.csv` (LGA-year level panel with all variables)

### Stage 2: Primary Econometric Analysis
```bash
# Install dependencies
pip install -r requirements.txt

# Open and run the primary analysis notebook
jupyter notebook outputs/Primary\ Econometric\ Analysis.ipynb
```
Primary Analysis Notebook contains data loading, exploratory analysis, and the main between-LGA regression. The analysis is descriptive and does not claim causation.

Main result: β ≈ -0.82 AUD/km (HC3 SE ≈ 0.53, p ≈ 0.12). The estimate is suggestive but imprecise.

### Stage 3: Robustness Analysis (Week 10 Deliverable)
```bash
# Open and run the robustness analysis notebook
jupyter notebook outputs/robustness_analysis/robustness_analysis.ipynb
```
Robustness Analysis Notebook contains a brief restatement of the main result and a focused set of checks grouped by family:

- Alternative controls: minimal, preferred, kitchen-sink
- Alternative samples: drop high-leverage LGAs
- Functional form: log outcome check
- Placebo: permutation test

The notebook exports a robustness table and diagnostic plots. The negative distance–rent association is consistent in sign across checks but imprecisely estimated. See the robustness notebook for the full table and interpretation.

If you'd like a one-page summary suitable for slides, I can produce that next.
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
│   └── eda_analysis.ipynb           # Exploratory notebook (supporting analysis)
│
└── outputs/
   ├── Primary Econometric Analysis.ipynb  # Primary analysis notebook
   ├── robustness_analysis/          # Robustness notebook, exported table, and plots
   │   ├── robustness_analysis.ipynb
   │   ├── robustness_table_framework.csv
   │   ├── robustness_summary.json
   │   ├── robustness_plot.png
   │   └── permutation_diagnostics.png
   ├── regression_results.csv       # Coefficient table
   └── regression_results.txt       # Full regression summary
```

---

## Methodological Declaration

Analysis Type: DESCRIPTIVE

We estimate the association between distance to Melbourne CBD and median rental prices. We do not attempt to identify a causal treatment effect.

---

## Econometric Specification

Main Model (between-LGA OLS with controls):
$$\overline{\text{median\_rent}}_{i} = \beta_0 + \beta_1 \cdot \overline{\text{distance}}_{i} + \beta_2 \cdot \overline{\text{crime}}_{i} + \beta_3 \cdot \overline{\text{schools}}_{i} + \beta_4 \cdot \overline{\text{health}}_{i} + \varepsilon_{i}$$

where the overbar denotes the LGA-level mean after aggregating across years.

Key Details:
- Outcome: Mean median weekly rent by LGA (AUD)
- Key Regressor: Mean straight-line distance from LGA centroid to Melbourne CBD (km)
- Controls: Mean offence count (crime), mean total schools, mean GP clinics per 1000 residents (health access)
- Sample: 31 LGAs with complete data for all variables
- Standard Errors: Plain OLS on one observation per LGA
- Functional Form: Linear, with a log-linear robustness check in the notebook

Specification Rationale:
We collapse the panel to the LGA level because distance does not vary within an LGA. We include controls for crime, schools, and health access because these amenities are plausible drivers of rental prices independent of distance and are correlated with both distance and rent. At the LGA-level aggregation, all 31 LGAs with distance data also have complete observations for these control variables, so including them does not reduce sample size.

---

## Main Results Summary

The analysis controls for crime (offence count), school availability (total schools), and health access (GP clinics per 1000 residents) at the LGA level.

**With controls (preferred inference: HC3 SEs):**
- Linear model (HC3): -$0.82 per week per km (HC3 SE ≈ 0.528, p ≈ 0.122, not statistically significant at conventional levels)
- Note: the plain OLS table in `outputs/regression_results.csv` reports the classical (non-HC3) p-value ≈ 0.161 for the same point estimate; the difference reflects the inference choice (HC3 robust SEs are larger here).
- Log-linear check (HC3): about -0.25% per km (p ≈ 0.129, not statistically significant).
- R² = 0.355 (captures ~35.5% of between-LGA rent variation)
- Sample: 31 LGAs with complete data

**Key finding (revised phrasing):** The negative distance–rent association is present in simple specifications but attenuates when controlling for local amenities. Under HC3 inference (the notebook's default), the preferred specification yields a point estimate of approximately -0.82 AUD/km that is suggestive but imprecisely estimated (p ≈ 0.12). This pattern is consistent with partial confounding by amenities: adding controls reduces the magnitude of the raw gradient, which reduces confidence that distance alone explains the full association.

---

## Robustness Analysis

`outputs/robustness_analysis/robustness_analysis.ipynb`

It reports the preferred specification alongside checks for:
- no controls
- extended controls
- drop high-leverage LGAs
- log-rent functional form
- permutation placebo

The notebook also exports a reusable table to `outputs/robustness_analysis/robustness_table_framework.csv`.

---

## Limitations

Since the analysis includes controls for major amenity variables, the main remaining limitations are measurement error and structural scope:

1. **Omitted Amenities** (Residual threat)
   - Employment density, transport quality, and other local services may still be correlated with distance and rent
   - Controlled variables (crime, schools, health) partially address this but do not fully resolve confounding

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

Conclusion:
The negative distance-rent association is present in simple specifications, but it is sensitive to the control set and becomes much weaker once richer amenity controls are added.

---

## How to Reproduce

### 1. **Environment Setup**
```bash
# Install Python 3.11+
python3 --version

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```
Activate the virtual environment first, then run the remaining commands with `python3`.
This installs the packages needed to read the Excel source files and to launch the notebook interface.

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
python3 code/clean_rent_data.py
python3 code/clean_crime_data.py
python3 code/clean_distance_data.py
python3 code/clean_health_data.py
python3 code/clean_schools_data.py
python3 code/clean_and_merge_data.py
```
Check `Data/clean/` for output CSVs.

### 4. **Run Analysis**

**Jupyter notebook**
```bash
jupyter notebook outputs/Primary\ Econometric\ Analysis.ipynb
jupyter notebook outputs/robustness_analysis/robustness_analysis.ipynb
```
- Run the primary notebook first, then the robustness notebook
- Run all cells to generate tables, plots, regression results, and robustness checks
- Output displays inline

---

## Software & Dependencies

**Python Version:** 3.11+

**Key Packages:**
- `pandas` – data manipulation
- `numpy` – numerical computing
- `matplotlib`, `seaborn` – visualization
- `statsmodels` – OLS regression and inference
- `jupyter` – notebook interface
- `openpyxl` – Excel file reader used by the cleaning scripts

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
├── Primary Econometric Analysis.ipynb  # Main notebook with tables, figure, and interpretation
├── robustness_analysis/          # Robustness notebook, exported table, and plots
│   ├── robustness_analysis.ipynb      # Robustness notebook
│   ├── robustness_table_framework.csv  # Exported robustness table
│   ├── robustness_summary.json        # Concise summary statistics
│   ├── robustness_plot.png             # Forest plot
│   └── permutation_diagnostics.png     # Permutation diagnostics
├── regression_results.csv       # Coefficient table
└── regression_results.txt       # Full OLS summary
```

Key outputs:
- Primary Econometric Analysis.ipynb: main notebook with the descriptive analysis, regression table, and figure
- robustness_analysis.ipynb: robustness checks and interpretation
- robustness_table_framework.csv: exported side-by-side robustness table
- regression_results.csv: tidy coefficient table
- regression_results.txt: full regression summary

Note: `outputs/regression_results.csv` and `outputs/regression_results.txt` are generated by `code/run_regression.py` using classical (non-robust) OLS standard errors (Covariance Type: nonrobust). The Primary Econometric Analysis notebook computes HC3 robust standard errors for the preferred inference; see the notebook for HC3 summaries and robustness checks.

**Table & Figure Mapping**
- **Table 1:** Regression results with controls — produced by `outputs/Primary Econometric Analysis.ipynb` ([outputs/Primary Econometric Analysis.ipynb](outputs/Primary%20Econometric%20Analysis.ipynb)).
- **Regression table (CSV):** tidy coefficient table `outputs/regression_results.csv` — produced by `code/run_regression.py` ([code/run_regression.py](code/run_regression.py)).
- **Regression summary (text):** `outputs/regression_results.txt` — produced by `code/run_regression.py` ([code/run_regression.py](code/run_regression.py)).
- **Figure 1:** Mean Rent vs. Distance from CBD (scatter + regression line) — produced by `outputs/Primary Econometric Analysis.ipynb` ([outputs/Primary Econometric Analysis.ipynb](outputs/Primary%20Econometric%20Analysis.ipynb)).
- **Robustness table:** `outputs/robustness_analysis/robustness_table_framework.csv` — produced by `outputs/robustness_analysis/robustness_analysis.ipynb` ([outputs/robustness_analysis/robustness_analysis.ipynb](outputs/robustness_analysis/robustness_analysis.ipynb)).
- **Robustness plot:** `outputs/robustness_analysis/robustness_plot.png` — produced by `outputs/robustness_analysis/robustness_analysis.ipynb` ([outputs/robustness_analysis/robustness_analysis.ipynb](outputs/robustness_analysis/robustness_analysis.ipynb)).
- **Permutation diagnostics:** `outputs/robustness_analysis/permutation_diagnostics.png` — produced by `outputs/robustness_analysis/robustness_analysis.ipynb` ([outputs/robustness_analysis/robustness_analysis.ipynb](outputs/robustness_analysis/robustness_analysis.ipynb)).
- **Final merged dataset:** `Data/clean/final_panel.csv` — produced by `code/clean_and_merge_data.py` ([code/clean_and_merge_data.py](code/clean_and_merge_data.py)).
- **Cleaning outputs:** `Data/clean/median_rent_clean.csv`, `crime_clean.csv`, `distance_clean.csv`, `schools_clean.csv`, `health_clean.csv` — produced by the corresponding scripts in `code/` (`clean_rent_data.py`, `clean_crime_data.py`, `clean_distance_data.py`, `clean_schools_data.py`, `clean_health_data.py`) (see [code/](code/)).

---

## Key Findings at a Glance

| Finding | Value |
|---------|-------|
| Sample size (LGAs) | 31 |
| Distance coefficient (with controls) | -$0.82 / week / km |
| R² | 0.355 |
| Log-linear effect | -0.25% per km |
| Statistical significance (p-value) | HC3 (preferred): 0.122 (not significant); classical OLS: 0.161 |
| Main takeaway | Distance remains negative in simple specs but attenuates with controls; HC3 inference yields a suggestive but imprecise estimate |


