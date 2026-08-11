from __future__ import annotations

"""Generate standard and large-print Word copies of the combined references."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

import generate_chapter_five as document_tools

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "report" / "Complete_Report_Source.md"
OUTPUT = ROOT / "report" / "Combined_References_Chapters_One_to_Five.docx"
LARGE_PRINT_OUTPUT = ROOT / "report" / "Combined_References_Chapters_One_to_Five_Large_Print.docx"


def load_references():
    source = SOURCE.read_text(encoding="utf-8")
    marker = "\n## REFERENCES\n"
    if source.count(marker) != 1:
        raise ValueError("Complete report source must contain exactly one reference section")
    references = [entry.strip() for entry in source.split(marker, 1)[1].strip().split("\n\n") if entry.strip()]
    if len(references) != 35:
        raise ValueError(f"Expected 35 consolidated references, found {len(references)}")
    return references


def generate(output, references, reference_size=12, heading_size=14, large_print=False):
    document = Document()
    document_tools.configure_styles(document)
    section = document.sections[0]
    document_tools.set_standard_page(section)
    document_tools.set_page_number_start(section, 1)
    document_tools.add_page_number(section.footer.paragraphs[0])

    heading = document.add_paragraph()
    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading.paragraph_format.space_after = Pt(18)
    run = heading.add_run("REFERENCES")
    document_tools.set_run_font(run, size=heading_size, bold=True)

    reference_style = document.styles["PCU Reference"]
    reference_style.font.size = Pt(reference_size)
    for reference in references:
        paragraph = document.add_paragraph(style="PCU Reference")
        document_tools.add_inline_markup(paragraph, reference, size=reference_size)

    properties = document.core_properties
    properties.title = "Combined References — Chapters One to Five" + (" — Large Print" if large_print else "")
    properties.subject = "Phishing Digital Medium Detection System Using Machine Learning"
    properties.author = "Honour Jesutofaye Jesutofaye"
    properties.comments = (
        "Large-print reading copy with 16-point references. " if large_print else ""
    ) + "Alphabetised and deduplicated APA reference list from the complete project report."

    settings = document.settings._element
    node = settings.find(qn("w:updateFields"))
    if node is None:
        node = OxmlElement("w:updateFields")
        settings.append(node)
    node.set(qn("w:val"), "true")

    document.save(output)
    print(f"{output}\n{len(references)} alphabetised, deduplicated references; {reference_size}-point text")


def main():
    references = load_references()
    generate(OUTPUT, references, reference_size=12, heading_size=14)
    generate(LARGE_PRINT_OUTPUT, references, reference_size=16, heading_size=18, large_print=True)


if __name__ == "__main__":
    main()
