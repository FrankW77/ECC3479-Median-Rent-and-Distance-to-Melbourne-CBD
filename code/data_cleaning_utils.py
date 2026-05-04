import re

import pandas as pd

NON_LGA_NAMES = {
    "",
    "TOTAL",
    "GRAND TOTAL",
    "VICTORIA",
    "METRO",
    "NON-METRO",
    "UNINCORPORATED VIC",
    "JUSTICE INSTITUTIONS AND IMMIGRATION FACILITIES",
}

NAME_REMAP = {
    "MORNINGTON PENIN'A": "MORNINGTON PENINSULA",
    "MORELAND": "MERRI-BEK",
}


def normalize_column_name(value):
    text = str(value).strip().lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def standardize_columns(df):
    result = df.copy()
    result.columns = [normalize_column_name(column) for column in result.columns]
    return result


def find_column(columns, *candidates):
    normalized = [(normalize_column_name(column), column) for column in columns]

    for candidate in candidates:
        candidate_norm = normalize_column_name(candidate)
        for normalized_name, original_name in normalized:
            if normalized_name == candidate_norm:
                return original_name

    for candidate in candidates:
        candidate_norm = normalize_column_name(candidate)
        for normalized_name, original_name in normalized:
            if candidate_norm in normalized_name:
                return original_name

    raise KeyError(
        f"Could not find a matching column for any of: {candidates}. "
        f"Available columns were: {list(columns)}"
    )


def coerce_numeric(series):
    cleaned = (
        series.astype("string")
        .str.strip()
        .replace({"": pd.NA, "-": pd.NA, "nan": pd.NA, "None": pd.NA})
        .str.replace(r"[\$,%]", "", regex=True)
        .str.replace(",", "", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def normalize_lga_name(value):
    if value is None or pd.isna(value):
        return pd.NA

    text = str(value).strip().upper()
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"[\u2018\u2019]", "'", text)
    text = re.sub(r"\s+", " ", text).strip()
    return NAME_REMAP.get(text, text)


def is_non_lga_name(value):
    normalized = normalize_lga_name(value)
    return pd.isna(normalized) or normalized in NON_LGA_NAMES
