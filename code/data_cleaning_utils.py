import re

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


def normalize_lga_name(value):
    if value is None:
        return value

    text = str(value).strip().upper()
    text = re.sub(r"\s*\([^)]*\)", "", text)
    text = re.sub(r"[\u2018\u2019]", "'", text)
    text = re.sub(r"\s+", " ", text).strip()
    return NAME_REMAP.get(text, text)


def is_non_lga_name(value):
    normalized = normalize_lga_name(value)
    return normalized is None or normalized in NON_LGA_NAMES
