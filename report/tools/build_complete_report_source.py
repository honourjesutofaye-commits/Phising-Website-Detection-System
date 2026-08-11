from __future__ import annotations

"""Assemble Chapters One–Five and one deduplicated APA reference section."""

from pathlib import Path
from collections import defaultdict
import re

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "report"
OUTPUT = REPORT_DIR / "Complete_Report_Source.md"
CHAPTERS = ("One", "Two", "Three", "Four", "Five")


def split_chapter(name):
    path = REPORT_DIR / f"Chapter_{name}_Source.md"
    source = path.read_text(encoding="utf-8")
    marker = "\n## REFERENCES\n"
    if source.count(marker) != 1:
        raise ValueError(f"{path.name} must contain exactly one reference marker")
    body, references = source.split(marker, 1)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    entries = [entry.strip() for entry in references.strip().split("\n\n") if entry.strip()]
    return "\n".join(lines).strip(), entries


def reference_identifier(reference):
    doi = re.search(r"https://doi\.org/([^\s]+)", reference, re.I)
    if doi:
        return "doi:" + doi.group(1).rstrip(".").casefold()
    urls = re.findall(r"https?://\S+", reference)
    if urls:
        return "url:" + urls[-1].rstrip(".").casefold()
    return "text:" + re.sub(r"\W+", "", reference).casefold()


def author_and_year(reference):
    year_match = re.search(r"\((\d{4}|n\.d\.)", reference)
    if not year_match:
        raise ValueError(f"Reference has no APA-style year: {reference}")
    author_text = reference[: year_match.start()].rstrip(" .")
    if "," in author_text:
        lead = author_text.split(",", 1)[0]
    else:
        lead = author_text
    return lead.strip(), year_match.group(1)


def citation_is_present(body, lead, year):
    occurrences = list(re.finditer(re.escape(lead), body, re.I))
    for match in occurrences:
        window = body[max(0, match.start() - 80) : match.end() + 220]
        if year in window:
            return True
    return False


def consolidate_references(raw_references):
    # For an identical DOI/URL, retain the most complete bibliographic variant.
    best = {}
    for order, reference in raw_references:
        key = reference_identifier(reference)
        current = best.get(key)
        if current is None or len(reference) > len(current[1]):
            best[key] = (order, reference)
    selected = [reference for _, reference in best.values()]

    # Chapter Five contains the precise official GAID citation; remove the older
    # broad NDPC homepage variant if both survived URL-based deduplication.
    prefix = "Nigeria Data Protection Commission. (2025)."
    ndpc = [reference for reference in selected if reference.startswith(prefix)]
    if len(ndpc) > 1:
        keep = max(ndpc, key=len)
        selected = [reference for reference in selected if not reference.startswith(prefix) or reference == keep]

    unique = []
    seen = set()
    for reference in selected:
        key = re.sub(r"\s+", " ", reference).strip().casefold()
        if key not in seen:
            seen.add(key)
            unique.append(reference)
    unique.sort(key=lambda reference: re.sub(r"^[^A-Za-z0-9]+", "", reference).casefold())
    return unique


def validate_correspondence(chapter_data, consolidated):
    # Every bibliography entry supplied by an individual chapter must be cited in
    # that chapter. This also verifies every consolidated entry remains cited.
    failures = []
    for name, body, references in chapter_data:
        for reference in references:
            lead, year = author_and_year(reference)
            if not citation_is_present(body, lead, year):
                failures.append(f"Chapter {name}: {lead} ({year})")
    if failures:
        raise ValueError("Uncited chapter references:\n- " + "\n- ".join(failures))

    combined_body = "\n\n".join(body for _, body, _ in chapter_data)
    missing = []
    for reference in consolidated:
        lead, year = author_and_year(reference)
        if not citation_is_present(combined_body, lead, year):
            missing.append(f"{lead} ({year})")
    if missing:
        raise ValueError("Uncited consolidated references:\n- " + "\n- ".join(missing))

    # Check author-year parenthetical citations against the consolidated index.
    index = defaultdict(set)
    for reference in consolidated:
        lead, year = author_and_year(reference)
        index[year].add(lead.casefold())
    unmatched = []
    for match in re.finditer(r"\(([^()]{1,180}?),\s*((?:19|20)\d{2}|n\.d\.)\)", combined_body):
        content, year = match.groups()
        # Handle semicolon-separated citations by validating each terminal part;
        # descriptive parentheses without a recognised author are ignored.
        part = content.split(";")[-1].strip()
        if re.fullmatch(r"[\d\s–—-]+", part) or re.search(r"author[’']s\s+(?:design|compilation)", part, re.I):
            continue
        if not any(re.search(rf"\b{re.escape(lead)}\b", part, re.I) for lead in index.get(year, set())):
            # Some citations use a corporate abbreviation after first spelling.
            if not ("NIST" in part and any("national institute" in lead for lead in index.get(year, set()))):
                unmatched.append(match.group(0))
    if unmatched:
        examples = sorted(set(unmatched))[:12]
        raise ValueError("Author-year citations without a matching reference:\n- " + "\n- ".join(examples))


def validate_structure(source):
    for number, word in enumerate(CHAPTERS, start=1):
        marker = f"## CHAPTER {word.upper()}"
        if source.count(marker) != 1:
            raise ValueError(f"Expected one {marker}")
    if source.count("## REFERENCES") != 1:
        raise ValueError("Combined source must contain one reference section")
    table_starts = re.findall(r"\[\[TABLE\s+([2-5]\.\d+)\s+START\]\]", source)
    table_ends = re.findall(r"\[\[TABLE\s+([2-5]\.\d+)\s+END\]\]", source)
    figures = re.findall(r"\[\[FIGURE\s+([2-5]\.\d+):", source)
    if sorted(table_starts) != sorted(table_ends):
        raise ValueError("Table start/end markers do not correspond")
    if len(table_starts) != 32:
        raise ValueError(f"Expected 32 tables, found {len(table_starts)}")
    if len(figures) != 19:
        raise ValueError(f"Expected 19 figures, found {len(figures)}")


def main():
    chapter_data = []
    raw_references = []
    for order, name in enumerate(CHAPTERS):
        body, references = split_chapter(name)
        chapter_data.append((name, body, references))
        raw_references.extend((order, reference) for reference in references)

    consolidated = consolidate_references(raw_references)
    validate_correspondence(chapter_data, consolidated)
    source = (
        "\n\n".join(body for _, body, _ in chapter_data)
        + "\n\n## REFERENCES\n\n"
        + "\n\n".join(consolidated)
        + "\n"
    )
    validate_structure(source)
    OUTPUT.write_text(source, encoding="utf-8")
    words = len(re.findall(r"\b[\w’'-]+\b", source))
    print(f"{OUTPUT}\n5 chapters; 32 tables; 19 figures; {len(consolidated)} references; {words:,} words")


if __name__ == "__main__":
    main()
