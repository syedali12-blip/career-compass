"""
Career Compass — World Bank API client

Real, free, no-API-key-needed source for Pakistan macro labor market data.
Docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

This supplies MACRO-level context (national unemployment rate, labor force
participation, GDP growth) — not occupation-specific data, which still comes
from O*NET. Together they give the AI a fuller, real picture: O*NET says
what the job involves, World Bank says what the broader economy looks like.

NOTE ON ILOSTAT: we looked into ILOSTAT as a second Pakistan-specific source,
but unlike World Bank, ILOSTAT does not offer a simple REST/JSON API — access
is via bulk data downloads and SDMX tools, which don't fit a live request/
response pipeline. Rather than fabricate specific ILOSTAT figures we can't
verify programmatically, we only link to it as a citable source for further
reading, and rely on World Bank's live API for actual numbers. This
limitation should be disclosed in the paper's Methods/Limitations section.
"""

import time
import requests

WORLD_BANK_BASE_URL = "https://api.worldbank.org/v2/country/PAK/indicator"

# Real World Bank indicator codes relevant to career/labor market context
INDICATORS = {
    "unemployment_total": {
        "code": "SL.UEM.TOTL.ZS",
        "label": "Total Unemployment Rate",
        "unit": "% of total labor force",
    },
    "youth_unemployment": {
        "code": "SL.UEM.1524.ZS",
        "label": "Youth Unemployment Rate (ages 15-24)",
        "unit": "% of youth labor force",
    },
    "labor_force_participation": {
        "code": "SL.TLF.CACT.ZS",
        "label": "Labor Force Participation Rate",
        "unit": "% of population ages 15+",
    },
    "gdp_growth": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "label": "GDP Growth Rate",
        "unit": "% annual",
    },
}

# Simple in-memory cache — this data changes at most once a year, so there's
# no need to hit the API on every single report generation. Cached for 24h.
_cache = {"data": None, "fetched_at": 0}
CACHE_TTL_SECONDS = 24 * 60 * 60


def _fetch_indicator(indicator_code):
    """
    Fetches one indicator for Pakistan from the World Bank API, returning
    the most recent non-null data point as {"value": ..., "year": ...}.
    Returns None if no data is available (rather than crashing).
    """
    url = f"{WORLD_BANK_BASE_URL}/{indicator_code}"
    response = requests.get(url, params={"format": "json", "per_page": 10}, timeout=10)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        return None

    for point in data[1]:
        if point.get("value") is not None:
            return {"value": point["value"], "year": point.get("date")}
    return None


def get_pakistan_labor_snapshot():
    """
    Returns a real, current snapshot of Pakistan's macro labor market
    context, pulled live from the World Bank API. Cached for 24 hours
    since this data doesn't change frequently.

    Returns a dict like:
    {
      "unemployment_total": {"label": ..., "value": 6.3, "year": "2023", "unit": "..."},
      ...
      "source": "World Bank Open Data (api.worldbank.org)"
    }
    Individual indicators may be missing (None) if unavailable — callers
    should handle that gracefully rather than assuming all fields exist.
    """
    now = time.time()
    if _cache["data"] and (now - _cache["fetched_at"]) < CACHE_TTL_SECONDS:
        return _cache["data"]

    snapshot = {"source": "World Bank Open Data (api.worldbank.org)"}
    for key, meta in INDICATORS.items():
        result = _fetch_indicator(meta["code"])
        snapshot[key] = {
            "label": meta["label"],
            "unit": meta["unit"],
            "value": result["value"] if result else None,
            "year": result["year"] if result else None,
        }

    _cache["data"] = snapshot
    _cache["fetched_at"] = now
    return snapshot
