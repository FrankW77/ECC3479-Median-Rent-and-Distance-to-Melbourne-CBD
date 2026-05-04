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

    # Collapse the panel to the LGA level so the regression matches the notebook.
    df = (
        df.groupby("lga_name", as_index=False)
        .agg(
            {
                "median_rent": "mean",
                "straight_line_km": "mean",
                "year": "count",
            }
        )
        .rename(columns={"year": "n_obs"})
        .dropna(subset=["straight_line_km"])
    )

    print()
    print(f"LGA-level sample size: {len(df)}")
    print(f"Mean median rent: {df['median_rent'].mean():.2f}")
    print(f"Mean straight-line distance: {df['straight_line_km'].mean():.2f}")

    y = df["median_rent"]
    X = sm.add_constant(df[["straight_line_km"]])
    model = sm.OLS(y, X).fit()

    results_df = pd.DataFrame(
        {
            "variable": model.params.index,
            "coefficient": model.params.values,
            "std_error": model.bse.values,
            "t_value": model.tvalues.values,
            "p_value": model.pvalues.values,
        }
    )

    print(model.summary())

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / "regression_results.txt", "w") as file_handle:
        file_handle.write(model.summary().as_text())

    results_df.to_csv(OUTPUT_DIR / "regression_results.csv", index=False)

    print("✓ Regression results saved to outputs/regression_results.txt and outputs/regression_results.csv")


if __name__ == "__main__":
    run_regression()