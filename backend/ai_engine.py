"""
Career Compass — AI personalization engine

IMPORTANT DESIGN PRINCIPLE (matches our data logbook decisions):
This module does NOT ask the AI to invent career advice, salary numbers, or
outlook predictions. Real data (from onet_client.py, and later ILOSTAT/World
Bank) is fetched FIRST. The AI's only job is to read that real data and turn
it into a clear, personalized explanation for the student — grounded in facts,
not freeform guessing.

Uses Gemini (via direct REST call — no extra SDK dependency needed).
"""

import os
import json
import time
import requests

GEMINI_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Tried in order. gemini-3.5-flash/-lite are current, but newer/high-demand
# models see frequent transient 503 "overloaded" errors from Google's own
# infrastructure (confirmed via Google's own developer forums — this is a
# known, ongoing issue, not something wrong in this code). gemini-2.5-flash
# and gemini-2.5-flash-lite are added as a second tier: an older, more
# established generation that tends to see less contention, so a 503 on the
# newer models has somewhere real to fall back to instead of just failing.
MODEL_CHAIN = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

# Free-tier rate limits mean occasional 429s are expected, especially during
# rapid testing. 503s ("model overloaded" on Google's end) are also common
# and just as transient. Retry a few times with a short delay before giving
# up on a given model and moving to the next one in the chain.
MAX_RETRIES_PER_MODEL = 2
RETRY_DELAY_SECONDS = 5


def _api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set. Add it to your .env file.")
    return key


def build_prompt(student_answers, occupation_profile, companies=None, courses=None, macro_context=None, universities=None):
    """
    Builds the prompt sent to Gemini. Explicitly instructs the model to
    only use the provided real data, and to return JSON only — no prose,
    no markdown fences, so our code can parse it directly.
    """
    companies = companies or []
    courses = courses or []
    macro_context = macro_context or {}
    universities = universities or []

    return f"""You are helping build a personalized career report for a student in Pakistan.

STUDENT'S ASSESSMENT ANSWERS:
{json.dumps(student_answers, indent=2)}

REAL OCCUPATIONAL DATA (from O*NET, U.S. Department of Labor):
{json.dumps(occupation_profile, indent=2)}

REAL COMPANIES IN PAKISTAN THAT OPERATE IN THIS FIELD (curated reference list —
use ONLY these names, do not invent or add any other company names):
{json.dumps(companies, indent=2)}

REAL COURSES MATCHING THE REQUIRED SKILLS (curated reference list — use ONLY
these, do not invent course names, and copy their "url" values exactly as given):
{json.dumps(courses, indent=2)}

REAL UNIVERSITIES BEST SUITED TO THIS FIELD (curated reference list, already
ranked best-first by admission competitiveness — use ONLY these, do not invent
or add any other university names, and preserve this order):
{json.dumps(universities, indent=2)}

REAL PAKISTAN MACRO LABOR MARKET DATA (live from the World Bank; national-level
context, not specific to this occupation — use it only to add broader economic
context, not as occupation-specific outlook data):
{json.dumps(macro_context, indent=2)}

INSTRUCTIONS:
- Base your response ONLY on the real data provided above. Do not invent
  statistics, salary figures, outlook claims, company names, university names,
  or course names that aren't grounded in the provided data.
- If the companies, courses, or universities lists above are empty, say so
  honestly in the relevant field rather than making something up.
- When mentioning companies, phrase it as "companies in this field include..."
  rather than claiming they have open positions right now, since we don't
  have live hiring data.
- If macro data is provided, you may reference it briefly (e.g., national
  unemployment rate) to add real-world context, but do not conflate it with
  occupation-specific outlook — be clear these are national averages.
- The "career_path_steps" field must read as a genuine, ORDERED sequence of
  what the student should actually do first, second, third, and so on —
  not a flat unordered list. Ground each step in the real data provided
  (e.g., "Apply to [a university from the list above]", "Learn [a skill from
  the list above] through [a course from the list above]") rather than
  generic advice.
- Write in an encouraging, clear tone appropriate for a student aged 16-22.
- Return ONLY valid JSON, with no markdown code fences and no extra text
  before or after it, in exactly this structure:

{{
  "recommended_path": "string — the occupation title",
  "why_it_fits": "string — 2-3 sentences connecting the student's answers to this path",
  "required_skills": ["string", "string", "..."],
  "outlook_summary": "string — 1-2 sentences summarizing the real outlook data provided",
  "macro_context_note": "string — 1 sentence on the broader Pakistan labor market, or empty string if no macro data was provided",
  "recommended_universities": [{{"name": "string", "city": "string", "hec_rank": "string", "admission_competitiveness": "string"}}],
  "recommended_companies": [{{"name": "string", "city": "string"}}],
  "recommended_courses": [{{"name": "string", "provider": "string", "free": true, "url": "string"}}],
  "career_path_steps": [
    {{"step_number": 1, "title": "string — short label", "description": "string — what to actually do"}},
    {{"step_number": 2, "title": "string", "description": "string"}}
  ]
}}"""


def _call_gemini_model(model, payload):
    """
    Calls a single Gemini model, retrying on 429 (rate limit) AND 503/502/504
    (transient server-side "overloaded"/unavailable errors — common on
    Google's end, especially on newer models, and NOT the same thing as a
    quota/rate-limit issue) up to MAX_RETRIES_PER_MODEL times each. Raises
    RuntimeError("MODEL_UNAVAILABLE") when this model is exhausted, so the
    caller knows to try the next model in the chain (vs. other error types,
    like a genuine 400/401, which should stop the whole process outright —
    retrying or falling back won't fix a bad request or bad API key).
    """
    url = GEMINI_URL_TEMPLATE.format(model=model)
    TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}

    for attempt in range(1, MAX_RETRIES_PER_MODEL + 1):
        response = requests.post(
            url,
            params={"key": _api_key()},  # in params, not the URL string,
                                          # so it never appears in raise_for_status() messages
            json=payload,
            timeout=30
        )
        if response.status_code in TRANSIENT_STATUS_CODES:
            if attempt < MAX_RETRIES_PER_MODEL:
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise RuntimeError("MODEL_UNAVAILABLE")

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            safe_message = str(e).replace(_api_key(), "***")
            raise RuntimeError(f"Gemini API error ({model}): {safe_message}") from e

        return response.json()


def generate_template_report(student_answers, occupation_profile, companies=None, courses=None, macro_context=None, universities=None):
    """
    Builds a report using the SAME JSON schema as the Gemini version, but
    with plain string templates instead of an AI call. Exists so the rest
    of the app (results page, PDF generation, companies/courses features)
    can be built and tested without depending on Gemini's free-tier rate
    limit — useful right now, and also a reasonable permanent fallback if
    Gemini is ever down or exhausted during a live demo.

    Every value here is built directly from real data (O*NET, curated
    companies/courses/universities, World Bank macro data) — no invented
    content, same principle as the AI path.
    """
    companies = companies or []
    courses = courses or []
    macro_context = macro_context or {}
    universities = universities or []

    overview = occupation_profile.get("overview", {})
    title = overview.get("title") or "your matched occupation"
    skills = occupation_profile.get("skills", [])[:10]

    interests = student_answers.get("interests", [])
    interests_phrase = ", ".join(interests[:2]) if interests else "your stated interests"

    why_it_fits = (
        f"Based on your interest in {interests_phrase} and the strengths you selected, "
        f"{title} is a real occupation match from O*NET's occupational database."
    )

    outlook = occupation_profile.get("outlook", {})
    bright = outlook.get("bright_outlook") if isinstance(outlook, dict) else None
    outlook_summary = (
        f"O*NET data indicates this occupation has a 'Bright Outlook' designation "
        f"({bright})." if bright else
        "Outlook data was retrieved from O*NET; see the full profile for details."
    )

    macro_note = ""
    unemployment = macro_context.get("unemployment_total")
    if unemployment and unemployment.get("value") is not None:
        macro_note = (
            f"For broader context, Pakistan's national unemployment rate was "
            f"{unemployment['value']:.1f}% as of {unemployment['year']} "
            f"(World Bank). This is a national average, not specific to this occupation."
        )

    # Build a genuine ordered career path, grounded in the real data available —
    # not a flat unordered list. Steps are only included if we actually have
    # the underlying data to ground them in.
    career_path_steps = []
    step_num = 1

    if universities:
        top_uni = universities[0]
        career_path_steps.append({
            "step_number": step_num,
            "title": "Apply to a matched university",
            "description": f"{top_uni['name']} ({top_uni.get('city', '')}) is our top real-data match for "
                            f"{title}, based on admission competitiveness. Review its admission requirements."
        })
        step_num += 1

    if skills:
        career_path_steps.append({
            "step_number": step_num,
            "title": "Build the core required skills",
            "description": f"Focus first on: {', '.join(skills[:3])}."
        })
        step_num += 1

    if courses:
        career_path_steps.append({
            "step_number": step_num,
            "title": "Start learning with a real course",
            "description": f"Begin with \"{courses[0]['name']}\" ({courses[0].get('provider', '')})."
        })
        step_num += 1

    if companies:
        career_path_steps.append({
            "step_number": step_num,
            "title": "Research real employers in this field",
            "description": f"Companies operating in this field in Pakistan include {companies[0]['name']} "
                            f"and others — look into internship or entry-level programs as you near graduation."
        })
        step_num += 1

    if not career_path_steps:
        career_path_steps = [{
            "step_number": 1, "title": "Explore this field further",
            "description": "See O*NET's full occupation profile for more detail."
        }]

    return {
        "recommended_path": title,
        "why_it_fits": why_it_fits,
        "required_skills": skills,
        "outlook_summary": outlook_summary,
        "macro_context_note": macro_note,
        "recommended_universities": universities,
        "recommended_companies": companies,
        "recommended_courses": courses,
        "career_path_steps": career_path_steps,
        "generated_by": "template",  # marks this as non-AI, useful for debugging/QA
    }


def generate_report_content(student_answers, occupation_profile, companies=None, courses=None, macro_context=None, universities=None):
    """
    Sends the prompt to Gemini and returns the parsed JSON response.
    Tries each model in MODEL_CHAIN in order — if the first model is fully
    rate-limited or unavailable after retries, automatically falls back to the next
    model instead of failing
    outright. Raises a clear error if Gemini's output isn't valid JSON,
    rather than silently passing broken data further down the pipeline.
    """
    prompt = build_prompt(student_answers, occupation_profile, companies, courses, macro_context, universities)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    result = None
    last_error = None
    for model in MODEL_CHAIN:
        try:
            result = _call_gemini_model(model, payload)
            break  # success — stop trying further models
        except RuntimeError as e:
            if str(e) == "MODEL_UNAVAILABLE":
                last_error = RuntimeError(
                    f"Gemini model '{model}' was rate-limited or temporarily unavailable."
                )
                continue  # try the next model in the chain
            raise  # any other error type stops the whole process

    if result is None:
        raise RuntimeError(
            "All available Gemini models are currently rate-limited or "
            "temporarily overloaded on Google's end. This usually resolves "
            "within a few minutes — try again shortly."
        ) from last_error

    try:
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response shape: {result}") from e

    # Safety net: strip markdown fences if the model adds them anyway
    cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Gemini did not return valid JSON: {cleaned}") from e


def generate_advisor_response(report, question, history=None):
    """
    Answers a follow-up question about a student's ALREADY-GENERATED report.
    Deliberately constrained: the model is given the report and the
    conversation so far, and explicitly instructed to answer only using
    that data — no open-ended career advice, no new facts not already in
    the report. If the question can't be answered from the report, the
    model is told to say so honestly rather than guess.

    Uses the same model fallback chain as the main report generator, but
    returns plain text (not JSON), since this is a conversational reply.
    """
    history = history or []

    history_text = ""
    if history:
        turns = []
        for turn in history[-6:]:  # keep the prompt small — last 6 turns is plenty of context
            role = "Student" if turn.get("role") == "user" else "Advisor"
            turns.append(f"{role}: {turn.get('text', '')}")
        history_text = "\n".join(turns)

    prompt = f"""You are an experienced career advisor who has just finished reviewing this
student's career assessment report in detail, and is now sitting down with them to talk
through it. You know this report thoroughly — speak with the confidence and specificity
of someone who actually read it, not someone summarizing a document at arm's length.

DATA RULE (non-negotiable): every specific fact you state — skills, universities, courses,
companies, figures — must come from the report below or the conversation so far. Never
invent a fact that isn't there. If the student asks something this report genuinely
doesn't cover, say so plainly and point them to retaking the assessment or the site's
University Comparisons / Programs Directory pages, instead of guessing.

STYLE RULE: sound like a professional advisor, not a search-result summarizer. Don't
lean on filler phrases like "your result says" or "your report indicates" as a crutch —
that gets repetitive and robotic fast. Instead, state things directly and specifically,
the way a real advisor would in conversation: name the actual skill, university, or
course by name, explain the "so what" behind it, and connect it back to what the student
is asking. It's fine to reference the report's contents naturally in passing (e.g. "given
your interest in X..." or "one of the universities that came up, [Name], is a strong fit
because...") without constantly flagging that you're reading from a report.

STUDENT'S REPORT:
{json.dumps(report, indent=2)}

CONVERSATION SO FAR:
{history_text if history_text else "(no previous messages)"}

STUDENT'S NEW QUESTION:
{question}

Answer with real substance — 3-6 sentences is often right, more if the question genuinely
needs it, but don't pad. Warm and encouraging, but direct and specific, like an advisor
who respects the student's time. Return plain text only — no JSON, no markdown formatting."""

    return _call_advisor_prompt(prompt)


def generate_general_advisor_response(question, history=None, companies=None, courses=None, universities=None):
    """
    Answers career/university/course questions in GENERAL — not tied to a
    specific student report. This is the second AI Advisor mode: available
    even before a student has completed the assessment, for broader
    "what field should I consider" / "tell me about X degree" questions.

    Less tightly constrained than generate_advisor_response() (which is
    locked to one report's data), since there's no single report to ground
    every claim in here. The model is expected to draw on genuine domain
    knowledge to give substantive, specific guidance — the constraint is
    narrowly about not fabricating hyper-specific data points (exact
    numbers, rankings, named institutions) it can't actually verify, not
    about staying vague or generic. If curated companies/courses/
    universities data is passed in, the model is told to prefer that real
    data over guessing when it's relevant to the question.
    """
    history = history or []
    companies = companies or []
    courses = courses or []
    universities = universities or []

    history_text = ""
    if history:
        turns = []
        for turn in history[-6:]:
            role = "Student" if turn.get("role") == "user" else "Advisor"
            turns.append(f"{role}: {turn.get('text', '')}")
        history_text = "\n".join(turns)

    grounding_block = ""
    if companies or courses or universities:
        grounding_block = f"""
REAL REFERENCE DATA YOU MAY USE (curated for Pakistan — prefer these specifics over
generic phrasing when they're relevant to the question; if they're not relevant, ignore
them rather than forcing them in):
Companies: {json.dumps(companies, indent=2)}
Courses: {json.dumps(courses, indent=2)}
Universities: {json.dumps(universities, indent=2)}
"""

    prompt = f"""You are Career Compass's general career advisor for students in Pakistan —
this is "general questions" mode, for career, degree, and university questions that
aren't tied to one specific assessment report. Answer like a genuinely knowledgeable
advisor who has counseled many students through these exact decisions: substantive,
specific, and opinionated where it's actually helpful (e.g. "X tends to suit people who
enjoy Y more than Z" or "the real trade-off between these two paths is..."). Don't hedge
into vagueness — a flat, generic answer is a worse outcome than a specific, well-reasoned
one, even on a topic with no single right answer.

You have real, substantial knowledge of career paths, degree structures, industries, and
how they map to different interests and strengths — use it. Explain trade-offs, name
concrete examples of what people in a field actually do day-to-day, and give a genuine
point of view when the student is comparing options, while still respecting that the
final call is theirs.

WHAT TO AVOID FABRICATING: specific numbers you can't actually verify — exact salary
figures, admission percentages/cutoffs, or claims like "ranked #1 in Pakistan." If a
number would strengthen the answer but you're not confident in a specific figure, describe
the pattern or magnitude qualitatively (e.g. "among the more competitive programs" rather
than inventing "top 2%") instead of dropping the point entirely. Same for named entities:
don't invent specific company names, course providers, or university names beyond the
reference data below — but general, well-established facts about fields and industries
are fair game and should be stated with normal confidence, not caveated to death.
{grounding_block}
CONVERSATION SO FAR:
{history_text if history_text else "(no previous messages)"}

STUDENT'S NEW QUESTION:
{question}

If the question is really about the student's own personal fit rather than general
information, give a genuinely useful general answer first, then mention that the Career
Compass assessment can personalize this further — don't deflect to the assessment instead
of answering.

Answer with real depth — several sentences to a short paragraph is often appropriate,
more if the question has real complexity to it. Professional and direct in tone, not
overly casual, but still warm. Return plain text only — no JSON, no markdown formatting."""

    return _call_advisor_prompt(prompt)


def _call_advisor_prompt(prompt):
    """
    Shared plumbing for both advisor modes (report-scoped and general):
    sends the prompt through the same model fallback chain as the main
    report generator, and returns the plain-text reply.
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    result = None
    last_error = None
    for model in MODEL_CHAIN:
        try:
            result = _call_gemini_model(model, payload)
            break
        except RuntimeError as e:
            if str(e) == "MODEL_UNAVAILABLE":
                last_error = RuntimeError(f"Gemini model '{model}' was rate-limited or temporarily unavailable.")
                continue
            raise

    if result is None:
        raise RuntimeError(
            "All available Gemini models are currently rate-limited or "
            "temporarily overloaded on Google's end. Try again shortly."
        ) from last_error

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Gemini response shape: {result}") from e
