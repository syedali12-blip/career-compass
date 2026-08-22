"""
Career Compass — Interest → O*NET search term mapping

WHY THIS EXISTS:
O*NET's /mnm/search endpoint matches against real occupation titles/keywords
in its taxonomy (things like "Software Developers", "Financial Analysts").
It does NOT handle:
  - Ampersands: "Math & Numbers" as a literal query returns nothing, since
    no O*NET occupation title contains "&".
  - Colloquial/category phrasing: "Computers & Technology" is a category
    label a student would recognize, but it isn't itself an occupation
    title, so it doesn't match anything either.

The old code sent the raw questionnaire option strings straight to O*NET as
search keywords, which is why students kept hitting "no matches found."

This file curates each interest option (and a few common dream_field
phrasings) to a short, ORDERED list of verified terms that DO return real
O*NET results, most-specific first. app.py tries each term in order via
search_with_fallback() until one hits.
"""

# Exact-match keys correspond to the option strings in static/js/questions.js
# ("interests" question). Keep these two files in sync if options change.
INTEREST_TO_ONET_TERMS = {
    "Math & Numbers": ["mathematician", "statistician", "actuary"],
    "Science": ["scientist", "research", "laboratory"],
    "Computers & Technology": ["software developer", "computer", "information technology"],
    "Arts & Design": ["graphic designer", "artist", "designer"],
    "Business & Finance": ["financial analyst", "business", "accountant"],
    "Writing & Communication": ["writer", "editor", "public relations"],
    "Social Sciences": ["psychologist", "sociologist", "social worker"],
    "Healthcare & Biology": ["registered nurse", "medical", "biologist"],
    "Engineering & Mechanics": ["engineer", "mechanic", "technician"],
    "Teaching & Mentoring": ["teacher", "instructor", "education"],
}

# A handful of common colloquial dream_field answers that don't map cleanly
# via the generic suffix-stripping logic in app.py (e.g. "IT" is too short/
# ambiguous to search directly, "doctor" alone is fine but "medicine" as a
# field name returns nothing useful without a more specific term).
DREAM_FIELD_ALIASES = {
    "it": ["information technology", "computer"],
    "medicine": ["physician", "medical"],
    "law": ["lawyer", "legal"],
    "business": ["business", "management"],
    "finance": ["financial analyst", "accountant"],
    "marketing": ["marketing manager", "advertising"],
    "design": ["graphic designer", "designer"],
    "engineering": ["engineer"],
    "teaching": ["teacher", "education"],
    "psychology": ["psychologist"],
}


def terms_for_interest(interest_label):
    """
    Returns the curated O*NET search terms for a single interest label.
    Falls back to a cleaned version of the label itself (strip '&', collapse
    whitespace) if the label isn't in the curated map, so new/unmapped
    options degrade gracefully instead of silently producing zero terms.
    """
    if interest_label in INTEREST_TO_ONET_TERMS:
        return list(INTEREST_TO_ONET_TERMS[interest_label])

    cleaned = interest_label.replace("&", " ").split()
    return [" ".join(cleaned)] if cleaned else []


def terms_for_dream_field(dream_field):
    """
    Returns curated O*NET search terms for a free-text dream_field answer,
    if it matches a known colloquial alias (case-insensitive). Returns an
    empty list if there's no known alias — callers should still fall back
    to the raw text / word-splitting logic already in app.py.
    """
    key = dream_field.strip().lower()
    return list(DREAM_FIELD_ALIASES.get(key, []))
