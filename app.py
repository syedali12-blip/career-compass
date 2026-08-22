"""
Career Compass — Main Flask Application

This file wires together the routes (pages/URLs) of the app.
Backend logic (O*NET calls, AI calls) lives in /backend and is connected
to the /generate-report route below.
"""

from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
import os
import json
import traceback

from backend import onet_client, ai_engine, pdf_generator, pakistan_resources, worldbank_client, university_data
from backend import interest_mapping

load_dotenv()  # reads .env file for ONET_USERNAME, ONET_PASSWORD, GEMINI_API_KEY

app = Flask(__name__)


def pick_onet_keyword_candidates(answers):
    """
    Turns the student's questionnaire answers into an ORDERED LIST of
    candidate search terms to try against O*NET, from most specific to
    most general. This exists because O*NET's search matches structured
    occupation titles, not everyday/colloquial phrasing — e.g. "businessmen"
    matches nothing, but "business" does.

    This is intentionally simple for now — a real similarity-scoring
    matcher (comparing multiple answers against O*NET's full taxonomy)
    is the planned upgrade once this basic pipeline is confirmed working.
    """
    candidates = []

    dream_field = answers.get("dream_field", "").strip()
    if dream_field and dream_field.lower() not in ("not sure", "n/a", ""):
        # Curated alias first (e.g. "IT" -> "information technology") —
        # these are verified to return real O*NET matches.
        candidates.extend(interest_mapping.terms_for_dream_field(dream_field))
        candidates.append(dream_field)
        # Common colloquial -> O*NET-friendly normalization: strip common
        # suffixes ("businessmen" -> "business", "salesman" -> "sales")
        # and try each individual word too, since multi-word phrases often
        # don't match but a single key word does.
        for suffix in ("men", "man", "s"):
            if dream_field.lower().endswith(suffix):
                candidates.append(dream_field[: -len(suffix)])
        candidates.extend(dream_field.split())

    # Interests come from fixed questionnaire options like "Math & Numbers"
    # or "Computers & Technology" — O*NET's search doesn't match the raw
    # label (the "&" and category-style phrasing don't correspond to real
    # occupation titles), so route each through the curated term mapping
    # instead of sending the raw label straight to O*NET.
    interests = answers.get("interests", [])
    for interest in interests:
        candidates.extend(interest_mapping.terms_for_interest(interest))

    candidates.append("general")

    # de-duplicate while preserving order, drop empties
    seen = set()
    unique = []
    for c in candidates:
        c = c.strip()
        if c and c.lower() not in seen:
            seen.add(c.lower())
            unique.append(c)
    return unique


def search_with_fallback(candidates, limit=1):
    """
    Tries each candidate keyword against O*NET in order, returning the
    first non-empty result. Returns (matches, keyword_used) so callers
    know which term actually worked — useful for debugging/logging.
    """
    for keyword in candidates:
        matches = onet_client.search_occupations(keyword, limit=limit)
        if matches:
            return matches, keyword
    return [], None


@app.route("/")
def landing_page():
    """The homepage — introduces Career Compass to the student."""
    return render_template("index.html")


@app.route("/questionnaire")
def questionnaire():
    """The step-by-step question flow."""
    return render_template("questionnaire.html")


@app.route("/generate-report", methods=["POST"])
def generate_report():
    """
    Real pipeline: takes the student's answers, searches O*NET for a
    matching occupation, pulls its real skills/outlook data, then asks
    Gemini to turn that into a personalized explanation. Returns JSON
    that the frontend results page can render.
    """
    answers = request.get_json()
    if not answers:
        return jsonify({"error": "No answers received"}), 400

    try:
        candidates = pick_onet_keyword_candidates(answers)
        matches, keyword_used = search_with_fallback(candidates, limit=1)

        if not matches:
            tried = ", ".join(candidates)
            return jsonify({"error": f"No O*NET matches found. Tried: {tried}"}), 404

        top_match = matches[0]
        occupation_profile = onet_client.get_full_occupation_profile(top_match["code"])

        # Pull real, curated Pakistan companies + matching courses — never
        # let the AI invent these, since hallucinated company/course names
        # would be a serious credibility problem for a research submission.
        field = pakistan_resources.guess_field(top_match["title"])
        companies = pakistan_resources.get_companies_for_field(field) if field else []
        courses = pakistan_resources.get_courses_for_skills(occupation_profile.get("skills", []), field=field)

        # Best real universities for this specific occupation — this was
        # requested in the original project registration and had been
        # dropped from the pipeline; restored here.
        top_universities = university_data.get_top_universities_for_occupation(
            top_match["title"], career_field=field, limit=3
        )

        # Real Pakistan macro labor market context from World Bank's live API.
        # Wrapped in its own try/except: if World Bank is temporarily down,
        # the report should still generate using O*NET + curated data alone,
        # rather than failing the whole request over an optional data source.
        try:
            macro_context = worldbank_client.get_pakistan_labor_snapshot()
        except Exception as e:
            print(f"World Bank data unavailable, continuing without it: {e}")
            macro_context = None

        # Toggle in .env: set USE_GEMINI=false to skip the AI call entirely
        # and use the template-based report instead. Useful right now while
        # testing everything else without being blocked by Gemini's free-tier
        # rate limit — flip it back to true once quota is available again.
        use_gemini = os.environ.get("USE_GEMINI", "true").lower() != "false"

        if use_gemini:
            try:
                report = ai_engine.generate_report_content(
                    answers, occupation_profile, companies=companies, courses=courses,
                    macro_context=macro_context, universities=top_universities
                )
            except RuntimeError as e:
                print(f"\n--- Gemini unavailable, falling back to template report: {e} ---\n")
                report = ai_engine.generate_template_report(
                    answers, occupation_profile, companies=companies, courses=courses,
                    macro_context=macro_context, universities=top_universities
                )
        else:
            report = ai_engine.generate_template_report(
                answers, occupation_profile, companies=companies, courses=courses,
                macro_context=macro_context, universities=top_universities
            )

        report["onet_code"] = top_match["code"]

        return jsonify(report)

    except Exception as e:
        # Catches EVERYTHING — missing keys, O*NET errors, Gemini errors,
        # network issues, anything. This guarantees the server always
        # returns a clean JSON error instead of crashing the whole process
        # (which is what caused the "couldn't reach server" symptom before —
        # only RuntimeError was being caught, so other exception types were
        # crashing the app instead of being handled).
        print("\n--- ERROR in /generate-report ---")
        traceback.print_exc()
        print("--- END ERROR ---\n")
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500


@app.route("/download-report", methods=["POST"])
def download_report():
    """
    Takes the report JSON (already generated by /generate-report, sent back
    from the browser) and returns it as a downloadable PDF.
    """
    report = request.get_json()
    if not report:
        return jsonify({"error": "No report data received"}), 400

    try:
        pdf_buffer = pdf_generator.generate_pdf(report)
        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="career_compass_report.pdf"
        )
    except Exception as e:
        print("\n--- ERROR in /download-report ---")
        traceback.print_exc()
        print("--- END ERROR ---\n")
        return jsonify({"error": f"PDF generation failed: {type(e).__name__}: {str(e)}"}), 500


@app.route("/sample-roadmap")
def sample_roadmap():
    """A sample results page, kept as a fallback/demo view alongside the
    real pipeline above. Clearly labeled as illustrative on the page itself."""
    return render_template("sample_roadmap.html")


@app.route("/about-data")
def about_data():
    """Transparency page explaining our data sources."""
    return render_template("about_data.html")


@app.route("/universities")
def universities():
    """University comparison tool, powered by our curated reference data
    (see backend/university_data.py for sourcing notes)."""
    from backend import university_data
    return render_template(
        "universities.html",
        universities=university_data.UNIVERSITIES,
        categories=university_data.CATEGORIES
    )


@app.route("/programs")
def programs():
    """Programs directory — search by degree, see which universities offer
    it, ranked with more competitive institutions first."""
    from backend import university_data
    return render_template(
        "programs.html",
        all_programs=university_data.get_all_programs(),
        universities_json=json.dumps(university_data.UNIVERSITIES),
        # Authoritative top-7-per-degree ranking (see university_data.py) —
        # a real researched ranking, distinct from the notable_programs-based
        # proxy above. Programs directory prefers this when a degree is an
        # exact match; JS falls back to the proxy search otherwise. JS builds
        # its own name->detail lookup from universities_json above, so we
        # only need to send the ranking itself here.
        degree_rankings_json=json.dumps(university_data.DEGREE_TOP_UNIVERSITIES)
    )


@app.route("/saved")
def saved_options():
    """Saved career options — persisted client-side in localStorage (see
    static/js/saved.js), since this app has no user accounts/database.
    Actual list rendering happens in saved.html via JS reading localStorage
    directly; this route just serves that template."""
    return render_template("saved.html")


@app.route("/advisor")
def advisor():
    """AI Advisor — a chat interface for follow-up questions about a
    student's own results. Reads the report from sessionStorage on the
    client side (set after /generate-report succeeds)."""
    return render_template("advisor.html")


@app.route("/advisor-chat", methods=["POST"])
def advisor_chat():
    """
    Two modes, chosen by payload["mode"]:

    "report" (default if a report is present): answers a follow-up question
    about a student's ALREADY-GENERATED report. Deliberately constrained —
    the AI is given only the student's report data and their question, with
    explicit instructions to answer using that data only.

    "general": answers broader career/university/course questions that
    aren't tied to one report — available even before a student has taken
    the assessment. Grounded loosely in curated Pakistan companies/courses/
    universities data (best-effort keyword match on the question) rather
    than a specific report.
    """
    payload = request.get_json()
    if not payload or "question" not in payload:
        return jsonify({"error": "Missing 'question' in request"}), 400

    mode = payload.get("mode") or ("report" if payload.get("report") else "general")

    try:
        if mode == "report":
            if "report" not in payload:
                return jsonify({"error": "mode is 'report' but no 'report' was provided"}), 400
            answer = ai_engine.generate_advisor_response(
                report=payload["report"],
                question=payload["question"],
                history=payload.get("history", [])
            )
        else:
            # General mode: best-effort grounding by guessing a field from
            # the question text itself, same helper the main pipeline uses
            # for occupation titles — reused here since it's the same kind
            # of "guess a broad field from free text" task.
            question = payload["question"]
            field = pakistan_resources.guess_field(question)
            companies = pakistan_resources.get_companies_for_field(field) if field else []
            matched_degree = university_data.find_matching_degree(question)
            universities = (
                university_data.get_top_universities_for_degree(matched_degree, limit=5)
                if matched_degree else []
            )
            answer = ai_engine.generate_general_advisor_response(
                question=question,
                history=payload.get("history", []),
                companies=companies,
                courses=[],
                universities=universities
            )
        return jsonify({"answer": answer, "mode": mode})
    except Exception as e:
        print("\n--- ERROR in /advisor-chat ---")
        traceback.print_exc()
        print("--- END ERROR ---\n")
        return jsonify({"error": f"{type(e).__name__}: {str(e)}"}), 500



if __name__ == "__main__":
    # use_reloader=False: the auto-reloader can restart the server mid-request
    # (e.g. when new files get created, like Python's __pycache__ files on
    # first import), which kills in-flight requests and causes "couldn't
    # reach the server" errors in the browser. Disabled for stability.
    # If you edit code, stop the server (Ctrl+C) and run "python app.py" again.
    app.run(debug=True, port=5000, use_reloader=False)
