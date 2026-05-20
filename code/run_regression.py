from pathlib import Path

import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = ROOT / "Data" / "clean" / "final_panel.csv"
OUTPUT_DIR = ROOT / "outputs"


def run_regression():
    df = pd.read_csv(CLEAN_PATH)

    print("Missing values per column:")
    print(df.isna().sum())

    # Collapse the panel to the LGA level with controls to match the notebook.
    df = (
        df.groupby("lga_name", as_index=False)
        .agg(
            {
                "median_rent": "mean",
                "straight_line_km": "mean",
                "offence_count": "mean",
                "total_schools": "mean",
                "gp_clinics_per_1000": "mean",
                "year": "count",
            }
        )
        .rename(columns={"year": "n_obs"})
        .dropna()
    )

    print()
    print(f"LGA-level sample size (with complete data): {len(df)}")
    print(f"Mean median rent: ${df['median_rent'].mean():.2f}/week")
    print(f"Mean straight-line distance: {df['straight_line_km'].mean():.2f} km")
    print(f"Mean offence count: {df['offence_count'].mean():.1f}")
    print(f"Mean total schools: {df['total_schools'].mean():.1f}")
    print(f"Mean GP clinics per 1000: {df['gp_clinics_per_1000'].mean():.3f}")

    y = df["median_rent"]
    X = sm.add_constant(df[["straight_line_km", "offence_count", "total_schools", "gp_clinics_per_1000"]])
    # Fit OLS and compute HC3 robust covariance results (preferred inference)
    model = sm.OLS(y, X).fit()
    robust = model.get_robustcov_results(cov_type="HC3")

    # Prepare tidy results using HC3 robust SEs and p-values
    results_df = pd.DataFrame(
        {
            "variable": X.columns,
            "coefficient": robust.params,
            "std_error": robust.bse,
            "t_value": robust.tvalues,
            "p_value": robust.pvalues,
        }
    )

    # Print both summaries for transparency
    print(model.summary())
    print("\nHC3 robust summary:\n")
    print(robust.summary())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save the HC3 robust summary and the tidy CSV (using HC3 SEs)
    with open(OUTPUT_DIR / "regression_results.txt", "w") as file_handle:
        file_handle.write(robust.summary().as_text())

    results_df.to_csv(OUTPUT_DIR / "regression_results.csv", index=False)


if __name__ == "__main__":
    run_regression()