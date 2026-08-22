"""
Career Compass — Curated Pakistan resources

WHY THIS FILE EXISTS: there is no live API for "which companies in Pakistan
offer internships" or "which courses teach this skill." Letting an LLM invent
company names risks hallucinating plausible-sounding but FAKE companies —
a serious credibility problem for a research submission. Instead, this file
is a manually curated, real reference list, fed to the AI as fact (same
pattern as O*NET data) rather than left for the AI to guess.

MAINTENANCE NOTE: this list needs periodic human review — companies close,
merge, or stop offering internships. Last reviewed: July 2026. Cite this
limitation in the paper: company/course data is curated, not live-sourced.

Career fields are intentionally broad buckets, matched against the
student's O*NET occupation category.
"""

# Real, well-established companies known to operate in Pakistan's tech hubs
# and commonly offer internship programs. Listed for general reference, NOT
# as a claim that positions are currently open — the report should phrase
# this as "companies in this field" rather than "actively hiring now."
COMPANY_DIRECTORY = {
    "Software / Technology": [
        {"name": "Systems Limited", "city": "Lahore"},
        {"name": "NetSol Technologies", "city": "Lahore"},
        {"name": "Arbisoft", "city": "Lahore"},
        {"name": "Devsinc", "city": "Lahore"},
        {"name": "10Pearls", "city": "Karachi"},
        {"name": "Folio3", "city": "Karachi"},
        {"name": "TPS (Techlogix)", "city": "Lahore"},
        {"name": "Careem (Uber Pakistan)", "city": "Karachi/Lahore/Islamabad"},
        {"name": "Bazaar Technologies", "city": "Karachi"},
        {"name": "Contour Software", "city": "Lahore"},
        {"name": "Techlogix", "city": "Lahore"},
        {"name": "Xgrid", "city": "Islamabad"},
    ],
    "Business / Finance": [
        {"name": "Habib Bank Limited (HBL)", "city": "Karachi"},
        {"name": "United Bank Limited (UBL)", "city": "Karachi"},
        {"name": "Engro Corporation", "city": "Karachi"},
        {"name": "Jazz (VEON Pakistan)", "city": "Islamabad"},
        {"name": "Unilever Pakistan", "city": "Karachi"},
        {"name": "K-Electric", "city": "Karachi"},
        {"name": "Meezan Bank", "city": "Karachi"},
        {"name": "Bank Alfalah", "city": "Karachi"},
        {"name": "Nestlé Pakistan", "city": "Lahore"},
        {"name": "Pakistan Tobacco Company", "city": "Islamabad"},
    ],
    "Engineering": [
        {"name": "Descon Engineering", "city": "Lahore"},
        {"name": "Pakistan State Oil (PSO)", "city": "Karachi"},
        {"name": "Nespak", "city": "Lahore/Islamabad"},
        {"name": "Fauji Fertilizer Company", "city": "Rawalpindi"},
        {"name": "Attock Refinery Limited", "city": "Rawalpindi"},
        {"name": "Pakistan Aeronautical Complex", "city": "Kamra"},
        {"name": "Heavy Mechanical Complex", "city": "Taxila"},
    ],
    "Healthcare / Biology": [
        {"name": "Aga Khan University Hospital", "city": "Karachi"},
        {"name": "Shaukat Khanum Memorial Hospital", "city": "Lahore"},
        {"name": "Getz Pharma", "city": "Karachi"},
        {"name": "The Indus Hospital", "city": "Karachi"},
        {"name": "GlaxoSmithKline Pakistan", "city": "Karachi"},
        {"name": "Shifa International Hospital", "city": "Islamabad"},
        {"name": "Searle Pakistan", "city": "Karachi"},
    ],
    "Arts / Design / Media": [
        {"name": "Interflow Communications", "city": "Lahore"},
        {"name": "Six Sigma Plus", "city": "Karachi"},
        {"name": "SadaPay (design/product teams)", "city": "Lahore"},
        {"name": "Geo TV Network", "city": "Karachi"},
        {"name": "ARY Digital Network", "city": "Karachi"},
        {"name": "Dawn Media Group", "city": "Karachi"},
    ],
}

# Skill -> real course mapping. Keyed against O*NET's ACTUAL skill vocabulary
# (O*NET's "skills" data returns broad categories like "Critical Thinking" and
# "Programming" — NOT specific tech stack names like "React" or "Django").
# Earlier version used tech-specific keys that barely overlapped with what
# O*NET actually returns, causing near-empty course lists. Fixed here.
#
# Each entry includes a real, verifiable URL. YouTube entries link to
# established, real channels (not individual video URLs, which are more
# likely to break or be mis-remembered) — channels are stable long-term
# references, which matters for something going into a printed research paper.
COURSE_DIRECTORY = {
    "Programming": [
        {"name": "Python for Everybody", "provider": "Coursera (University of Michigan)", "free": True, "url": "https://www.coursera.org/specializations/python"},
        {"name": "CS50's Introduction to Computer Science", "provider": "edX (Harvard)", "free": True, "url": "https://www.edx.org/cs50"},
        {"name": "freeCodeCamp", "provider": "YouTube", "free": True, "url": "https://www.youtube.com/@freecodecamp"},
    ],
    "Critical Thinking": [
        {"name": "Introduction to Logic and Critical Thinking", "provider": "Coursera (Duke)", "free": True, "url": "https://www.coursera.org/specializations/logic-critical-thinking"},
        {"name": "CrashCourse Philosophy (Logic & Reasoning)", "provider": "YouTube", "free": True, "url": "https://www.youtube.com/@crashcourse"},
    ],
    "Complex Problem Solving": [
        {"name": "Introduction to Systems Thinking", "provider": "Coursera", "free": True, "url": "https://www.coursera.org/courses?query=systems%20thinking"},
        {"name": "Model Thinking", "provider": "Coursera (University of Michigan)", "free": True, "url": "https://www.coursera.org/learn/model-thinking"},
    ],
    "Active Learning": [
        {"name": "Learning How to Learn", "provider": "Coursera (UC San Diego)", "free": True, "url": "https://www.coursera.org/learn/learning-how-to-learn"},
    ],
    "Judgment and Decision Making": [
        {"name": "Improving Your Judgment", "provider": "Coursera (University of Michigan)", "free": True, "url": "https://www.coursera.org/learn/decision-making"},
    ],
    "Systems Analysis": [
        {"name": "System Design Primer", "provider": "GitHub (free reference)", "free": True, "url": "https://github.com/donnemartin/system-design-primer"},
        {"name": "CS50's Introduction to Computer Science", "provider": "edX (Harvard)", "free": True, "url": "https://www.edx.org/cs50"},
    ],
    "Mathematics": [
        {"name": "Khan Academy Math", "provider": "Khan Academy", "free": True, "url": "https://www.khanacademy.org/math"},
        {"name": "3Blue1Brown", "provider": "YouTube", "free": True, "url": "https://www.youtube.com/@3blue1brown"},
    ],
    "Science": [
        {"name": "Khan Academy Science", "provider": "Khan Academy", "free": True, "url": "https://www.khanacademy.org/science"},
    ],
    "Writing": [
        {"name": "Good with Words: Writing and Editing", "provider": "Coursera (University of Michigan)", "free": True, "url": "https://www.coursera.org/specializations/good-with-words"},
    ],
    "Speaking": [
        {"name": "Improving Communication Skills", "provider": "Coursera (University of Pennsylvania)", "free": True, "url": "https://www.coursera.org/learn/wharton-communication-skills"},
    ],
    "Active Listening": [
        {"name": "Improving Communication Skills", "provider": "Coursera (University of Pennsylvania)", "free": True, "url": "https://www.coursera.org/learn/wharton-communication-skills"},
    ],
    "Persuasion": [
        {"name": "Introduction to Negotiation", "provider": "Coursera (Yale)", "free": True, "url": "https://www.coursera.org/learn/negotiation"},
    ],
    "Negotiation": [
        {"name": "Introduction to Negotiation", "provider": "Coursera (Yale)", "free": True, "url": "https://www.coursera.org/learn/negotiation"},
    ],
    "Service Orientation": [
        {"name": "Customer Service Fundamentals", "provider": "Coursera", "free": True, "url": "https://www.coursera.org/courses?query=customer%20service"},
    ],
    "Time Management": [
        {"name": "Work Smarter, Not Harder: Time Management", "provider": "Coursera (UC Irvine)", "free": True, "url": "https://www.coursera.org/learn/work-smarter-not-harder"},
    ],
    "Management of Financial Resources": [
        {"name": "Financial Markets", "provider": "Coursera (Yale)", "free": True, "url": "https://www.coursera.org/learn/financial-markets-global"},
        {"name": "Introduction to Corporate Finance", "provider": "edX (Columbia)", "free": True, "url": "https://www.edx.org/learn/finance"},
    ],
    "Quality Control Analysis": [
        {"name": "Quality Management", "provider": "Coursera", "free": True, "url": "https://www.coursera.org/courses?query=quality%20management"},
    ],
    "Troubleshooting": [
        {"name": "Technical Support Fundamentals", "provider": "Coursera (Google)", "free": True, "url": "https://www.coursera.org/learn/technical-support-fundamentals"},
    ],
    "Design": [
        {"name": "Google UX Design Professional Certificate", "provider": "Coursera", "free": False, "url": "https://www.coursera.org/professional-certificates/google-ux-design"},
        {"name": "DesignCourse", "provider": "YouTube", "free": True, "url": "https://www.youtube.com/@DesignCourse"},
    ],
    "Marketing": [
        {"name": "Google Digital Marketing & E-commerce Certificate", "provider": "Coursera", "free": False, "url": "https://www.coursera.org/professional-certificates/google-digital-marketing-ecommerce"},
    ],
}

# Field-level fallback courses — shown when skill-based matching finds few
# or no results, so the report never looks empty for a well-defined field.
FIELD_FALLBACK_COURSES = {
    "Software / Technology": COURSE_DIRECTORY["Programming"] + COURSE_DIRECTORY["Systems Analysis"],
    "Business / Finance": COURSE_DIRECTORY["Management of Financial Resources"] + COURSE_DIRECTORY["Negotiation"],
    "Engineering": COURSE_DIRECTORY["Systems Analysis"] + COURSE_DIRECTORY["Mathematics"],
    "Healthcare / Biology": COURSE_DIRECTORY["Science"],
    "Arts / Design / Media": COURSE_DIRECTORY["Design"],
}


def get_companies_for_field(field):
    """
    Returns real companies known to operate in the given broad career field.
    Falls back to an empty list (not fabricated data) if the field isn't
    in our curated directory yet.
    """
    return COMPANY_DIRECTORY.get(field, [])


# Keywords used to map a free-text occupation title (from O*NET) to one of
# our curated field buckets above. Simple substring matching for now.
FIELD_KEYWORDS = {
    "Software / Technology": ["software", "developer", "programmer", "data", "computer", "it ", "web", "network", "systems analyst"],
    "Business / Finance": ["business", "finance", "accountant", "manager", "marketing", "sales", "economist", "analyst"],
    "Engineering": ["engineer", "mechanical", "civil", "electrical", "industrial"],
    "Healthcare / Biology": ["health", "medical", "nurse", "physician", "biology", "pharma", "clinical"],
    "Arts / Design / Media": ["design", "artist", "media", "writer", "graphic", "film", "journalist"],
}


def guess_field(occupation_title):
    """
    Guesses which curated field bucket an O*NET occupation title belongs to,
    using simple keyword matching. Returns None if no confident match —
    callers should handle that gracefully (skip company/course suggestions
    rather than guessing wrong).
    """
    if not occupation_title:
        return None
    title_lower = occupation_title.lower()
    for field, keywords in FIELD_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            return field
    return None


def get_courses_for_skills(skills, field=None, min_results=4):
    """
    Given a list of skill names (from O*NET's real skill vocabulary), returns
    matching real courses. If skill-based matching returns fewer than
    min_results, tops up with field-level fallback courses so the report
    never looks sparse for a well-defined field — while still preferring
    the more specific skill-matched courses first.
    """
    results = []
    for skill in skills:
        for key, courses in COURSE_DIRECTORY.items():
            if key.lower() in skill.lower() or skill.lower() in key.lower():
                results.extend(courses)

    if len(results) < min_results and field:
        results.extend(FIELD_FALLBACK_COURSES.get(field, []))

    # de-duplicate while preserving order
    seen = set()
    unique_results = []
    for c in results:
        marker = (c["name"], c["provider"])
        if marker not in seen:
            seen.add(marker)
            unique_results.append(c)
    return unique_results
