from __future__ import annotations

"""Generate the complete PCU-style PhishGuard AI project report.

The chapter manuscripts remain independently reviewable. This generator builds one
submission document, adds evidence-bounded preliminary matter, removes repeated
chapter covers/references, and appends one deduplicated APA reference list.
"""

from pathlib import Path
import re

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

import generate_chapter_three as chapter_three
import generate_chapter_four as chapter_four
import generate_chapter_five as document_tools

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "report"
SOURCE = REPORT_DIR / "Complete_Report_Source.md"
OUTPUT = REPORT_DIR / "Complete_Project_Report_Phishing_Digital_Medium_Detection_System.docx"
DIAGRAM_DIR = REPORT_DIR / "diagrams"

FIGURES = {
    "PHISHGUARD AI CONCEPTUAL FRAMEWORK": {
        "number": "2.1",
        "placeholder": False,
        "svg": DIAGRAM_DIR / "PhishGuard_AI_Conceptual_Framework.svg",
        "landscape": False,
        "width": 6.15,
    },
    **chapter_three.FIGURES,
    **chapter_four.FIGURES,
    **document_tools.FIGURES,
}

LANDSCAPE_TABLES = {
    "2.1",
    *chapter_three.LANDSCAPE_TABLES,
    *chapter_four.LANDSCAPE_TABLES,
    *document_tools.LANDSCAPE_TABLES,
}
TABLE_WIDTHS = {
    "2.1": [1.22, 1.05, 1.55, 1.62, 1.68, 1.55, 1.53],
    **chapter_three.TABLE_WIDTHS,
    **chapter_four.TABLE_WIDTHS,
    **document_tools.TABLE_WIDTHS,
}

CHAPTER_TITLES = {
    "## CHAPTER ONE": "CHAPTER ONE",
    "## CHAPTER TWO": "CHAPTER TWO",
    "## CHAPTER THREE": "CHAPTER THREE",
    "## CHAPTER FOUR": "CHAPTER FOUR",
    "## CHAPTER FIVE": "CHAPTER FIVE",
}
CHAPTER_SUBTITLES = {
    "## INTRODUCTION": "INTRODUCTION",
    "## LITERATURE REVIEW": "LITERATURE REVIEW",
    "## RESEARCH METHODOLOGY, SYSTEM ANALYSIS AND DESIGN": "RESEARCH METHODOLOGY, SYSTEM ANALYSIS AND DESIGN",
    "## SYSTEM IMPLEMENTATION, TESTING, RESULTS AND DISCUSSION": "SYSTEM IMPLEMENTATION, TESTING, RESULTS AND DISCUSSION",
    "## SUMMARY, CONCLUSION AND RECOMMENDATIONS": "SUMMARY, CONCLUSION AND RECOMMENDATIONS",
}

ABSTRACT = (
    "Phishing increasingly reaches users through both email and Short Message Service (SMS), while many detection studies remain "
    "channel-specific, opaque, or difficult to reproduce outside their original datasets. This project designed, implemented and "
    "evaluated PhishGuard AI, a practical machine-learning decision-support prototype for analysing email and SMS messages. A "
    "design-science approach combined literature analysis, repository-grounded requirements, system design, implementation inspection "
    "and reproducible verification. The Django application routes email and SMS inputs to separate term frequency–inverse document "
    "frequency and Logistic Regression pipelines, then combines bounded model evidence with deterministic content rules, sender/domain "
    "intelligence and URL checks. It aggregates the findings into Low Risk (0–39), Suspicious (40–69) and High Risk (70–100) bands and "
    "returns explanations and recommended actions. Verification was deliberately separated from unsupported performance claims. The "
    "bundled SMS corpus contained 5,574 records: 4,827 ham and 747 spam. On the repository's stored 4,459/1,115 split, the SMS model "
    "produced 98.30% accuracy, 93.92% precision, 93.29% recall and 93.60% F1-score, with a confusion matrix of 957 true negatives, "
    "9 false positives, 10 false negatives and 139 true positives. However, an audit found 414 duplicate rows and 139 test rows whose "
    "exact messages also occurred in training. Performance on the non-leaked test subset and after deduplicated retraining was lower, "
    "with F1-scores of 91.89% and 91.95%, respectively. Forty-seven Django tests passed, and fixed hybrid scenarios demonstrated "
    "implemented routing, scoring and presentation behaviours. No defensible held-out email metrics or participant usability findings "
    "were available; corresponding sections therefore remain clearly marked for verified evidence. The study concludes that PhishGuard "
    "AI achieves its aim at practical academic-prototype level, not as a production-ready cybersecurity service. Database migrations, "
    "production security, privacy controls, contemporary channel-specific datasets, independent robustness testing and governed user "
    "evaluation are required before operational protection claims or deployment."
)

ABBREVIATIONS = [
    ("AI", "Artificial Intelligence"),
    ("APA", "American Psychological Association"),
    ("APWG", "Anti-Phishing Working Group"),
    ("B.Sc.", "Bachelor of Science"),
    ("CSRF", "Cross-Site Request Forgery"),
    ("DFD", "Data-Flow Diagram"),
    ("F1", "Harmonic mean of precision and recall"),
    ("GAID", "General Application and Implementation Directive"),
    ("HCI", "Human–Computer Interaction"),
    ("LIME", "Local Interpretable Model-Agnostic Explanations"),
    ("ML", "Machine Learning"),
    ("NDPA", "Nigeria Data Protection Act"),
    ("NIST", "National Institute of Standards and Technology"),
    ("ORM", "Object–Relational Mapping"),
    ("SMS", "Short Message Service"),
    ("TF-IDF", "Term Frequency–Inverse Document Frequency"),
    ("URL", "Uniform Resource Locator"),
    ("XAI", "Explainable Artificial Intelligence"),
]


def _set_style_font(style, size=12, bold=False):
    style.font.name = "Times New Roman"
    fonts = style._element.get_or_add_rPr().get_or_add_rFonts()
    for attribute in ("ascii", "hAnsi", "eastAsia"):
        fonts.set(qn(f"w:{attribute}"), "Times New Roman")
    style.font.size = Pt(size)
    style.font.bold = bold


def configure_complete_styles(document):
    document_tools.configure_styles(document)
    styles = document.styles

    specifications = {
        "PCU Chapter Heading": (14, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 0),
        "PCU Chapter Subtitle": (14, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 12),
        "PCU Preliminary Heading": (14, True, WD_ALIGN_PARAGRAPH.CENTER, 0, 18),
        "PCU Table Caption": (10, False, WD_ALIGN_PARAGRAPH.CENTER, 0, 5),
        "PCU Figure Caption": (10, False, WD_ALIGN_PARAGRAPH.CENTER, 5, 0),
        "PCU Field Note": (10, False, WD_ALIGN_PARAGRAPH.CENTER, 6, 0),
    }
    for name, (size, bold, alignment, before, after) in specifications.items():
        style = styles[name] if name in styles else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        _set_style_font(style, size=size, bold=bold)
        style.paragraph_format.alignment = alignment
        style.paragraph_format.line_spacing = 1.0 if "Caption" in name or name == "PCU Field Note" else 1.5
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = "Heading" in name or name == "PCU Table Caption"

    # Outline levels make the custom chapter hierarchy navigable in Word.
    for name, level in (("PCU Chapter Heading", 0), ("PCU Section Heading", 1), ("PCU Subsection Heading", 2)):
        p_pr = styles[name]._element.get_or_add_pPr()
        outline = p_pr.find(qn("w:outlineLvl"))
        if outline is None:
            outline = OxmlElement("w:outlineLvl")
            p_pr.append(outline)
        outline.set(qn("w:val"), str(level))


def set_vertical_alignment(section, value):
    node = section._sectPr.find(qn("w:vAlign"))
    if node is None:
        node = OxmlElement("w:vAlign")
        section._sectPr.append(node)
    node.set(qn("w:val"), value)


def set_number_format(section, start=None, format_name=None):
    node = section._sectPr.find(qn("w:pgNumType"))
    if node is None:
        node = OxmlElement("w:pgNumType")
        section._sectPr.append(node)
    if start is not None:
        node.set(qn("w:start"), str(start))
    if format_name is not None:
        node.set(qn("w:fmt"), format_name)


def clear_paragraph(paragraph):
    paragraph._p.clear_content()


def add_page_field(paragraph, cached_text):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = cached_text
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instruction, separate, text, end])
    document_tools.set_run_font(run, size=12)


def add_dynamic_field(paragraph, instruction, cached_text):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    begin.set(qn("w:dirty"), "true")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {instruction} "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = cached_text
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, instr, separate, text, end])
    document_tools.set_run_font(run, size=11)


def add_cover(document):
    section = document.sections[0]
    document_tools.set_standard_page(section)
    set_vertical_alignment(section, "center")
    entries = [
        ("PHISHING DIGITAL MEDIUM DETECTION SYSTEM USING MACHINE LEARNING", 14, True, 24),
        ("BY", 12, True, 14),
        ("HONOUR JESUTOFAYE JESUTOFAYE", 13, True, 4),
        ("MATRICULATION NUMBER: [INSERT MATRICULATION NUMBER]", 12, True, 24),
        (
            "A PROJECT REPORT SUBMITTED TO THE DEPARTMENT OF COMPUTER SCIENCE, "
            "PRECIOUS CORNERSTONE UNIVERSITY, IBADAN, IN PARTIAL FULFILMENT OF "
            "THE REQUIREMENTS FOR THE AWARD OF THE DEGREE OF BACHELOR OF SCIENCE "
            "(B.Sc.) IN COMPUTER SCIENCE",
            12,
            True,
            22,
        ),
        ("SUPERVISOR: DR. OSUNTOKUN", 12, True, 22),
        ("[INSERT APPROVED MONTH AND YEAR]", 12, True, 0),
    ]
    for text, size, bold, after in entries:
        paragraph = document.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.line_spacing = 1.15
        paragraph.paragraph_format.space_after = Pt(after)
        run = paragraph.add_run(text)
        document_tools.set_run_font(run, size=size, bold=bold)


def begin_preliminary_section(document):
    section = document.add_section(WD_SECTION.NEW_PAGE)
    document_tools.set_standard_page(section)
    set_vertical_alignment(section, "top")
    set_number_format(section, start=2, format_name="lowerRoman")
    section.footer.is_linked_to_previous = False
    section.header.is_linked_to_previous = False
    footer = section.footer.paragraphs[0]
    clear_paragraph(footer)
    add_page_field(footer, "ii")


def begin_main_section(document):
    section = document.add_section(WD_SECTION.NEW_PAGE)
    document_tools.set_standard_page(section)
    set_vertical_alignment(section, "top")
    set_number_format(section, start=1, format_name="decimal")
    section.footer.is_linked_to_previous = False
    section.header.is_linked_to_previous = False
    footer = section.footer.paragraphs[0]
    clear_paragraph(footer)
    add_page_field(footer, "1")


def add_preliminary_heading(document, text):
    paragraph = document.add_paragraph(style="PCU Preliminary Heading")
    run = paragraph.add_run(text)
    document_tools.set_run_font(run, size=14, bold=True)


def add_front_body(document, text, first_line=True):
    paragraph = document.add_paragraph(style="Normal")
    if first_line:
        paragraph.paragraph_format.first_line_indent = Inches(0.5)
    document_tools.add_inline_markup(paragraph, text)
    return paragraph


def add_signature_table(document, rows):
    table = document.add_table(rows=len(rows), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False
    for index, (role, name) in enumerate(rows):
        row = table.rows[index]
        for cell in row.cells:
            cell.width = Inches(3.0)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.BOTTOM
            document_tools.set_cell_margins(cell, top=180, start=70, bottom=40, end=70)
        left = row.cells[0].paragraphs[0]
        left.alignment = WD_ALIGN_PARAGRAPH.CENTER
        document_tools.add_inline_markup(left, f"______________________________\n{name}\n{role}", size=11)
        right = row.cells[1].paragraphs[0]
        right.alignment = WD_ALIGN_PARAGRAPH.CENTER
        document_tools.add_inline_markup(right, "______________________________\nSignature and Date", size=11)
    # Signature blocks intentionally use no visible grid.
    table_xml = table._tbl
    borders = table_xml.tblPr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        table_xml.tblPr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "nil")
        borders.append(node)


def add_preliminary_matter(document):
    add_preliminary_heading(document, "CERTIFICATION")
    add_front_body(
        document,
        "This is to certify that the project titled **Phishing Digital Medium Detection System Using Machine Learning** was carried out "
        "by **Honour Jesutofaye Jesutofaye**, Matriculation Number **[INSERT MATRICULATION NUMBER]**, in the Department of Computer "
        "Science, Precious Cornerstone University, Ibadan, under the supervision of Dr. Osuntokun. The report is submitted in partial "
        "fulfilment of the requirements for the award of the Bachelor of Science (B.Sc.) degree in Computer Science.",
    )
    add_signature_table(document, [("Project Supervisor", "Dr. Osuntokun"), ("Head of Department", "[INSERT NAME]")])

    document.add_page_break()
    add_preliminary_heading(document, "DECLARATION")
    add_front_body(
        document,
        "I, **Honour Jesutofaye Jesutofaye**, declare that this project report is an original account of the work completed for this "
        "degree, except where the ideas, findings or words of other authors have been acknowledged through citation and reference. "
        "The report has not been submitted in whole or in part for another degree or qualification."
    )
    add_signature_table(document, [("Student", "Honour Jesutofaye Jesutofaye")])

    document.add_page_break()
    add_preliminary_heading(document, "APPROVAL")
    add_front_body(
        document,
        "This project report has been examined and approved as meeting the academic requirements of the Department of Computer "
        "Science, Precious Cornerstone University, Ibadan. All names, signatures and dates below are editable and must be completed "
        "only by the authorised persons.",
    )
    add_signature_table(
        document,
        [
            ("Project Supervisor", "Dr. Osuntokun"),
            ("Head of Department", "[INSERT NAME]"),
            ("External Examiner", "[INSERT NAME]"),
        ],
    )

    document.add_page_break()
    add_preliminary_heading(document, "DEDICATION")
    paragraph = document.add_paragraph(style="Normal")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(30)
    run = paragraph.add_run("[INSERT APPROVED DEDICATION]")
    document_tools.set_run_font(run, size=12, bold=True, color=(36, 74, 104))

    document.add_page_break()
    add_preliminary_heading(document, "ACKNOWLEDGEMENTS")
    paragraph = document.add_paragraph(style="Normal")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(20)
    run = paragraph.add_run(
        "[INSERT PERSONALISED ACKNOWLEDGEMENTS AFTER CONFIRMING THE PEOPLE, INSTITUTIONS AND SUPPORT TO BE RECOGNISED]"
    )
    document_tools.set_run_font(run, size=12, bold=True, color=(36, 74, 104))

    document.add_page_break()
    add_preliminary_heading(document, "ABSTRACT")
    add_front_body(document, ABSTRACT)
    keywords = document.add_paragraph(style="Normal")
    keywords.paragraph_format.space_before = Pt(8)
    run = keywords.add_run("Keywords: ")
    document_tools.set_run_font(run, bold=True)
    document_tools.add_inline_markup(
        keywords,
        "phishing; smishing; email; SMS; machine learning; TF-IDF; Logistic Regression; explainability; Django; PhishGuard AI",
    )

    document.add_page_break()
    add_preliminary_heading(document, "TABLE OF CONTENTS")
    field = document.add_paragraph()
    add_dynamic_field(
        field,
        'TOC \\h \\z \\t "PCU Chapter Heading,1,PCU Section Heading,2,PCU Subsection Heading,3"',
        "Update this table in Microsoft Word: press Ctrl+A, then F9.",
    )
    note = document.add_paragraph(style="PCU Field Note")
    note.add_run("This table is an updateable Word field; page numbers are recalculated after edits.")

    document.add_page_break()
    add_preliminary_heading(document, "LIST OF TABLES")
    field = document.add_paragraph()
    add_dynamic_field(field, 'TOC \\h \\z \\t "PCU Table Caption,1"', "Update this list in Microsoft Word: press Ctrl+A, then F9.")
    note = document.add_paragraph(style="PCU Field Note")
    note.add_run("This list is generated from the report's table-caption style.")

    document.add_page_break()
    add_preliminary_heading(document, "LIST OF FIGURES")
    field = document.add_paragraph()
    add_dynamic_field(field, 'TOC \\h \\z \\t "PCU Figure Caption,1"', "Update this list in Microsoft Word: press Ctrl+A, then F9.")
    note = document.add_paragraph(style="PCU Field Note")
    note.add_run("This list is generated from the report's figure-caption style.")

    document.add_page_break()
    add_preliminary_heading(document, "LIST OF ABBREVIATIONS")
    table = document.add_table(rows=len(ABBREVIATIONS), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for index, (abbreviation, meaning) in enumerate(ABBREVIATIONS):
        first, second = table.rows[index].cells
        document_tools.set_fixed_cell_width(first, 1.35)
        document_tools.set_fixed_cell_width(second, 4.85)
        for cell in (first, second):
            document_tools.set_cell_margins(cell, top=35, start=45, bottom=35, end=45)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        first_p = first.paragraphs[0]
        first_p.paragraph_format.line_spacing = 1.0
        run = first_p.add_run(abbreviation)
        document_tools.set_run_font(run, size=10.5, bold=True)
        second_p = second.paragraphs[0]
        second_p.paragraph_format.line_spacing = 1.0
        document_tools.add_inline_markup(second_p, meaning, size=10.5)


def add_chapter_heading(document, text):
    paragraph = document.add_paragraph(style="PCU Chapter Heading")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(text)
    document_tools.set_run_font(run, size=14, bold=True)


def add_chapter_subtitle(document, text):
    paragraph = document.add_paragraph(style="PCU Chapter Subtitle")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run(text)
    document_tools.set_run_font(run, size=14, bold=True)


def add_caption(document, label, text, before=False):
    is_table = label.startswith("Table ")
    style = "PCU Table Caption" if is_table else "PCU Figure Caption"
    paragraph = document.add_paragraph(style=style)
    paragraph.paragraph_format.space_before = Pt(0 if before else 5)
    paragraph.paragraph_format.space_after = Pt(5 if before else 0)
    paragraph.paragraph_format.keep_with_next = before
    run = paragraph.add_run(f"{label}: ")
    document_tools.set_run_font(run, size=10, bold=True)
    document_tools.add_inline_markup(paragraph, text, size=10)


def add_comparative_table_note(document):
    paragraph = document.add_paragraph(style="PCU Caption")
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(4)
    run = paragraph.add_run("Note. ")
    document_tools.set_run_font(run, size=8.5, italic=True)
    document_tools.add_inline_markup(
        paragraph,
        "Metrics are reproduced from the cited studies and are not directly comparable across different datasets or evaluation designs.",
        size=8.5,
    )


def parse_source(document, lines, pending_svg_links):
    in_references = False
    first_chapter = True
    pending_figure_key = None
    pending_chapter_subtitle = False
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        index += 1
        if not line:
            continue

        if line in CHAPTER_TITLES:
            if not first_chapter:
                document.add_page_break()
            add_chapter_heading(document, CHAPTER_TITLES[line])
            first_chapter = False
            pending_chapter_subtitle = True
            continue
        if line in CHAPTER_SUBTITLES:
            if not pending_chapter_subtitle:
                raise ValueError(f"Unexpected chapter subtitle: {line}")
            add_chapter_subtitle(document, CHAPTER_SUBTITLES[line])
            pending_chapter_subtitle = False
            continue
        if line == "## REFERENCES":
            document.add_page_break()
            add_chapter_heading(document, "REFERENCES")
            in_references = True
            continue
        if line.startswith("## "):
            raise ValueError(f"Unhandled level-two heading: {line}")

        table_start = re.match(r"^\[\[TABLE\s+([2-5]\.\d+)\s+START\]\]$", line)
        if table_start:
            number = table_start.group(1)
            table_lines = []
            end_marker = f"[[TABLE {number} END]]"
            while index < len(lines) and lines[index].strip() != end_marker:
                table_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError(f"Missing end marker for Table {number}")
            index += 1

            if number == "2.1":
                caption = "Comparative analysis of selected phishing email and SMS studies (2024–2026)"
            else:
                while index < len(lines) and not lines[index].strip():
                    index += 1
                if index >= len(lines):
                    raise ValueError(f"Missing caption for Table {number}")
                match = re.match(rf"^\*\*Table\s+{re.escape(number)}:\*\*\s*(.*)$", lines[index].strip())
                if not match:
                    raise ValueError(f"Expected caption immediately after Table {number}")
                caption = match.group(1)
                index += 1

            document_tools.add_table(document, number, caption, document_tools.parse_markdown_table(table_lines))
            if number == "2.1":
                add_comparative_table_note(document)
            continue

        figure_match = re.match(r"^\[\[FIGURE\s+([2-5]\.\d+):\s+(.+)\]\]$", line)
        if figure_match:
            number, key = figure_match.groups()
            if key not in FIGURES:
                raise ValueError(f"Unknown figure key: {key}")
            if FIGURES[key]["number"] != number:
                raise ValueError(f"Figure marker/configuration mismatch for {key}")
            document_tools.add_figure(document, key, pending_svg_links)
            pending_figure_key = key
            continue

        caption_match = re.match(r"^\*\*Figure\s+([2-5]\.\d+):\*\*\s*(.*)$", line)
        if caption_match:
            if pending_figure_key is None:
                raise ValueError(f"Figure caption without marker: {line}")
            expected = FIGURES[pending_figure_key]["number"]
            if caption_match.group(1) != expected:
                raise ValueError(f"Figure number mismatch: expected {expected}")
            add_caption(document, f"Figure {expected}", caption_match.group(2))
            document_tools.finish_figure_section(document, pending_figure_key)
            pending_figure_key = None
            continue

        if line.startswith("#### "):
            document_tools.add_heading(document, line[5:], subsection=True)
            continue
        if line.startswith("### "):
            document_tools.add_heading(document, line[4:], subsection=False)
            continue
        if in_references:
            document_tools.add_reference(document, line)
            continue
        if line.startswith("- "):
            document_tools.add_bullet_item(document, line[2:])
            continue
        if re.match(r"^\d+\.\s", line):
            document_tools.add_numbered_item(document, line)
            continue
        document_tools.add_body_paragraph(document, line)

    if pending_figure_key is not None:
        raise ValueError(f"Figure {pending_figure_key} has no caption")


def set_document_properties(document):
    properties = document.core_properties
    properties.title = "Phishing Digital Medium Detection System Using Machine Learning"
    properties.subject = "Complete Final-Year Project Report — Chapters One to Five"
    properties.author = "Honour Jesutofaye Jesutofaye"
    properties.keywords = (
        "phishing, smishing, email, SMS, machine learning, TF-IDF, Logistic Regression, "
        "hybrid detection, explainability, Django, PhishGuard AI"
    )
    properties.comments = (
        "PCU-style combined project report. Unsupported email/usability evidence remains explicitly marked; "
        "the system is described as a practical academic prototype rather than a production service."
    )


def main():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    for figure in FIGURES.values():
        if not figure.get("placeholder") and not figure["svg"].exists():
            raise FileNotFoundError(figure["svg"])

    # Reuse the structurally tested chapter-five document primitives with the
    # complete report's merged table/figure registries.
    document_tools.FIGURES = FIGURES
    document_tools.LANDSCAPE_TABLES = LANDSCAPE_TABLES
    document_tools.TABLE_WIDTHS = TABLE_WIDTHS
    document_tools.RENDER_DIR = ROOT / ".report-work" / "complete-report-renders"
    document_tools.add_caption = add_caption

    document = Document()
    configure_complete_styles(document)
    set_document_properties(document)
    add_cover(document)
    begin_preliminary_section(document)
    add_preliminary_matter(document)
    begin_main_section(document)
    pending_svg_links = []
    parse_source(document, SOURCE.read_text(encoding="utf-8").splitlines(), pending_svg_links)
    document_tools.set_update_fields(document)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document.save(OUTPUT)
    document_tools.inject_svg_fallbacks(OUTPUT, pending_svg_links)
    print(OUTPUT)


if __name__ == "__main__":
    main()
