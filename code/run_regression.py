import pandas as pd
import statsmodels.api as sm
import os

def run_regression():

    df = pd.read_csv("Data/clean/final_panel.csv")

    print("Missing values per column:")
    print(df.isna().sum())

    # Aggregate to the LGA level so the script matches the notebook's descriptive specification.
    df = (
        df.groupby("lga_name", as_index=False)
          .agg({
              "median_rent": "mean",
              "straight_line_km": "mean",
              "year": "count",
          })
          .rename(columns={"year": "n_obs"})
          .dropna(subset=["straight_line_km"])
    )

    print()
    print(f"LGA-level sample size: {len(df)}")
    print(f"Mean median rent: {df['median_rent'].mean():.2f}")
    print(f"Mean straight-line distance: {df['straight_line_km'].mean():.2f}")

    y = df["median_rent"]
    X = df[["straight_line_km"]]

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    results_df = pd.DataFrame({
        "variable": model.params.index,
        "coefficient": model.params.values,
        "std_error": model.bse.values,
        "t_value": model.tvalues.values,
        "p_value": model.pvalues.values
    })

    # Print summary to terminal
    print(model.summary())

    # Ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    # Save full summary to text file
    with open("outputs/regression_results.txt", "w") as f:
        f.write(model.summary().as_text())

    # Save tidy CSV of coefficients
    results_df.to_csv("outputs/regression_results.csv", index=False)

    print("✓ Regression results saved to outputs/regression_results.txt and outputs/regression_results.csv")


if __name__ == "__main__":
    run_regression()