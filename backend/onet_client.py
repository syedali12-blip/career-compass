"""
Career Compass — O*NET Web Services client (API v2)

IMPORTANT: O*NET migrated from v1.9 (HTTP Basic Auth, username/password) to
v2 (a single API key sent via an X-API-Key header). This client uses v2.
Docs: https://services.onetcenter.org/reference/start/migration

All functions here return plain Python dicts/lists — nothing O*NET-specific
should leak into the rest of the app, so we can swap data sources later
without rewriting everything downstream.
"""

import os
import requests

ONET_BASE_URL = "https://api-v2.onetcenter.org"


def _headers():
    """Builds the X-API-Key header O*NET v2 requires."""
    api_key = os.environ.get("ONET_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ONET_API_KEY not set. Add it to your .env file. "
            "(Note: O*NET moved to API v2, which uses a single API key "
            "instead of the old username/password.)"
        )
    return {"X-API-Key": api_key}


def _get(path, params=None):
    """Internal helper: makes a GET request to O*NET v2 and returns parsed JSON."""
    url = f"{ONET_BASE_URL}{path}"
    response = requests.get(url, params=params, headers=_headers(), timeout=10)
    response.raise_for_status()
    return response.json()


def search_occupations(keyword, limit=5):
    """
    Searches O*NET occupations by keyword (e.g. a student's interest like
    "software" or "healthcare"). Returns a simplified list of matches:
    [{ "code": "15-1252.00", "title": "Software Developers" }, ...]

    NOTE: O*NET's search response uses "career" as the results array key
    (not "occupation" — easy mistake, since other O*NET endpoints use
    different key names for similar-looking data).
    """
    data = _get("/mnm/search", params={"keyword": keyword})
    occupations = data.get("career", [])[:limit]
    return [
        {"code": o.get("code"), "title": o.get("title")}
        for o in occupations
    ]


def get_occupation_overview(onet_code):
    """
    Fetches the career overview for a specific O*NET-SOC code — includes
    a plain-language description of the occupation.
    """
    return _get(f"/mnm/careers/{onet_code}")


def _extract_elements(data):
    """
    Safely extracts flat element names from O*NET's nested response shape:
    { "group": [ { "title": {...}, "element": [ {"name": "..."}, ... ] }, ... ] }

    Defensive against two real O*NET quirks:
    - Occupations with no collected data for this category can return an
      empty list `[]` instead of a dict — calling .get() on that would crash.
    - Some responses may be missing "group" entirely.
    """
    if not isinstance(data, dict):
        return []  # e.g. data came back as [] — no data available

    names = []
    for group in data.get("group", []):
        for element in group.get("element", []):
            name = element.get("name")
            if name:
                names.append(name)
    return names


def get_occupation_skills(onet_code):
    """
    Fetches the required skills for a specific occupation.
    Returns a simplified flat list of skill names.
    """
    data = _get(f"/mnm/careers/{onet_code}/skills")
    return _extract_elements(data)


def get_occupation_knowledge(onet_code):
    """Fetches the knowledge areas relevant to a specific occupation."""
    data = _get(f"/mnm/careers/{onet_code}/knowledge")
    return _extract_elements(data)


def get_job_outlook(onet_code):
    """
    Fetches the job outlook / Bright Outlook status for an occupation.
    This is the real, citable growth-projection data — used instead of
    letting the AI guess about future demand.
    """
    return _get(f"/mnm/careers/{onet_code}/job_outlook")


def get_full_occupation_profile(onet_code):
    """
    Convenience function: pulls together overview, skills, knowledge, and
    outlook for one occupation into a single dict. This is what gets
    handed to the AI layer for personalization.
    """
    return {
        "overview": get_occupation_overview(onet_code),
        "skills": get_occupation_skills(onet_code),
        "knowledge": get_occupation_knowledge(onet_code),
        "outlook": get_job_outlook(onet_code),
    }
