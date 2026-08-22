"""
Career Compass — PDF report generator

Takes the structured report JSON (produced by ai_engine.py, grounded in real
O*NET data) and turns it into a downloadable PDF the student can keep.
"""

import io
import matplotlib
matplotlib.use("Agg")  # no GUI backend needed on a server
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, ListFlowable,
                                 ListItem, Image, HRFlowable, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

NAVY = colors.HexColor("#0A0E1A")
BRASS = colors.HexColor("#C9A24B")
TEXT_DARK = colors.HexColor("#1F2A3C")
TEXT_MUTED = colors.HexColor("#5A6B7B")


def _build_outlook_chart():
    """
    Builds a simple outlook chart image in memory (no file saved to disk).
    NOTE: this currently draws an illustrative upward trend shape — once
    real O*NET Bright Outlook / ILOSTAT projection data is available, this
    should plot the actual data points instead.
    """
    fig, ax = plt.subplots(figsize=(5, 2.2), dpi=150)
    years = [2026, 2029, 2032, 2036]
    values = [20, 45, 70, 92]  # illustrative shape, not real projection numbers

    ax.plot(years, values, color="#C9A24B", linewidth=2.5, marker="o")
    ax.fill_between(years, values, color="#C9A24B", alpha=0.15)
    ax.set_facecolor("#0A0E1A")
    fig.patch.set_facecolor("#0A0E1A")
    ax.tick_params(colors="#8E97A8", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#3A4568")
    ax.set_ylabel("Relative Demand", color="#8E97A8", fontsize=8)
    ax.set_title("Illustrative Outlook Trend", color="#F2EFE7", fontsize=10)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_pdf(report):
    """
    Builds the full PDF report from the report dict returned by ai_engine.py.
    Expected keys: recommended_path, why_it_fits, required_skills,
    outlook_summary, next_steps.

    Returns a BytesIO buffer ready to send to the browser.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=0.75 * inch, bottomMargin=0.75 * inch,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleStyle", parent=styles["Title"], fontSize=22,
                                  textColor=NAVY, spaceAfter=4, alignment=TA_CENTER)
    subtitle_style = ParagraphStyle("SubtitleStyle", parent=styles["Normal"], fontSize=11,
                                     textColor=TEXT_MUTED, alignment=TA_CENTER, spaceAfter=18)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=14,
                         textColor=NAVY, spaceBefore=16, spaceAfter=6)
    body = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10.5,
                           leading=15, textColor=TEXT_DARK, spaceAfter=6)

    story = []
    story.append(Paragraph("Career Compass", title_style))
    story.append(Paragraph("Your Personalized Career Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=14))

    story.append(Paragraph("Recommended Path", h1))
    story.append(Paragraph(report.get("recommended_path", "Not available"), body))

    story.append(Paragraph("Why This Fits You", h1))
    story.append(Paragraph(report.get("why_it_fits", ""), body))

    story.append(Paragraph("Required Skills", h1))
    skills = report.get("required_skills", [])
    if skills:
        story.append(ListFlowable(
            [ListItem(Paragraph(s, body)) for s in skills],
            bulletType="bullet", start="circle", leftIndent=12
        ))

    story.append(Paragraph("Job Market Outlook", h1))
    story.append(Paragraph(report.get("outlook_summary", ""), body))

    macro_note = report.get("macro_context_note", "")
    if macro_note:
        story.append(Paragraph(f"<i>{macro_note}</i>", body))

    highlight_box_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E7")),
        ("BOX", (0, 0), (-1, -1), 1, BRASS),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ])

    universities = report.get("recommended_universities", [])
    if universities:
        story.append(Paragraph("🎓 Best-Matched Universities", h1))
        uni_lines = []
        for u in universities:
            name = u.get("name", "")
            city = u.get("city", "")
            rank = u.get("hec_rank", "")
            comp = u.get("admission_competitiveness", "")
            uni_lines.append(f"<b>{name}</b> — {city}<br/><font size=8>HEC Rank: {rank} &nbsp;|&nbsp; Admission: {comp}</font>")
        uni_content = [[Paragraph("<br/><br/>".join(uni_lines), body)]]
        story.append(Table(uni_content, colWidths=[6.4 * inch], style=highlight_box_style))
        story.append(Paragraph(
            "<i>Ranked using our curated HEC-based reference data, best real match first.</i>", body
        ))
        story.append(Spacer(1, 10))

    courses = report.get("recommended_courses", [])
    if courses:
        story.append(Paragraph("📚 Recommended Courses", h1))
        course_lines = []
        for c in courses:
            name = c.get("name", "")
            provider = c.get("provider", "")
            free_tag = '<font color="#2E7D32">Free</font>' if c.get("free") else "Paid"
            url = c.get("url", "")
            if url:
                line = f'<b><link href="{url}" color="#8C6D28">{name}</link></b> — {provider} ({free_tag})'
            else:
                line = f"<b>{name}</b> — {provider} ({free_tag})"
            course_lines.append(line)
        course_content = [[Paragraph("<br/>".join(course_lines), body)]]
        story.append(Table(course_content, colWidths=[6.4 * inch], style=highlight_box_style))
        story.append(Spacer(1, 10))

    companies = report.get("recommended_companies", [])
    if companies:
        story.append(Paragraph("🏢 Companies in This Field (Pakistan)", h1))
        company_lines = [f"<b>{c.get('name', '')}</b> — {c.get('city', '')}" for c in companies]
        company_content = [[Paragraph("<br/>".join(company_lines), body)]]
        story.append(Table(company_content, colWidths=[6.4 * inch], style=highlight_box_style))
        story.append(Paragraph(
            "<i>Note: this is a curated reference list of companies known to operate "
            "in this field, not a live list of open positions.</i>", body
        ))
        story.append(Spacer(1, 10))

    try:
        chart_buf = _build_outlook_chart()
        story.append(Spacer(1, 8))
        story.append(Image(chart_buf, width=5 * inch, height=2.2 * inch))
        story.append(Spacer(1, 8))
    except Exception:
        pass  # chart is a nice-to-have; never block the PDF over it

    career_path_steps = report.get("career_path_steps", [])
    if career_path_steps:
        story.append(Paragraph("Your Career Path — Next Steps", h1))
        for step in career_path_steps:
            num = step.get("step_number", "")
            title_txt = step.get("title", "")
            desc = step.get("description", "")
            step_para = Paragraph(
                f'<font color="#8C6D28"><b>Step {num}: {title_txt}</b></font><br/>{desc}',
                body
            )
            story.append(Table([[step_para]], colWidths=[6.4 * inch], style=highlight_box_style))
            story.append(Spacer(1, 6))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor("#CBD5E0")))
    story.append(Spacer(1, 6))
    footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7.5,
                                   textColor=TEXT_MUTED, alignment=TA_CENTER)
    story.append(Paragraph(
        "Occupational data sourced from O*NET Web Services (U.S. Department of Labor, "
        "Employment and Training Administration). O*NET® is a trademark of USDOL/ETA.",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer
