#%%
import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup

URL = "https://bank.gov.ua/en/monetary/archive-rish"

def fetch_nbu_key_policy_rate(start="2000-01-01", end="2025-12-31"):
    """
    Fetch NBU key policy rate archive directly from the official NBU webpage
    by parsing visible text instead of relying on pd.read_html().

    Returns
    -------
    pd.DataFrame
        Columns:
        - date_effective
        - key_policy_rate
    """
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # Extract visible strings in reading order
    tokens = [s.strip() for s in soup.stripped_strings if s.strip()]

    rows = []
    current_year = None
    pending_date = None

    for tok in tokens:
        # Year line, e.g. "2025"
        if re.fullmatch(r"(19|20)\d{2}", tok):
            current_year = int(tok)
            pending_date = None
            continue

        # Date line, e.g. "from 06.06"
        m_date = re.fullmatch(r"from\s+(\d{2})\.(\d{2})", tok.lower())
        if m_date and current_year is not None:
            day = int(m_date.group(1))
            month = int(m_date.group(2))
            pending_date = pd.Timestamp(year=current_year, month=month, day=day)
            continue

        # Rate line, e.g. "15,5" or "10.0"
        # Must come after a pending date
        if pending_date is not None:
            m_rate = re.fullmatch(r"\d{1,3}(?:[.,]\d+)?", tok)
            if m_rate:
                rate = float(tok.replace(",", "."))
                rows.append({
                    "date_effective": pending_date,
                    "key_policy_rate": rate
                })
                pending_date = None
                continue

    df = pd.DataFrame(rows).drop_duplicates().sort_values("date_effective")

    # Restrict to exam sample
    df = df[
        (df["date_effective"] >= pd.Timestamp(start)) &
        (df["date_effective"] <= pd.Timestamp(end))
    ].reset_index(drop=True)

    return df


# Run
nbu_rate = fetch_nbu_key_policy_rate(start="2000-01-01", end="2025-12-31")

# Save
nbu_rate.to_csv("data_nbu_key_policy_rate.csv", index=False)

# Checks
print("Head:")
print(nbu_rate.head(), "\n")

print("Tail:")
print(nbu_rate.tail(), "\n")

print("Summary:")
print(nbu_rate["key_policy_rate"].describe(), "\n")

print("Max rate:", nbu_rate["key_policy_rate"].max())