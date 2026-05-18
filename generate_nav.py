#!/usr/bin/env python3
"""Generate the nav section for mkdocs.yml by scanning actual study files."""

import os
from pathlib import Path

DOCS = Path(__file__).parent / "docs" / "studies"

STUDIES = [
    # (slug, short_title, arc_name, arc_comment)
    ("sv-01-biblical-righteousness", "01 -- Biblical Righteousness", "Arc 1 -- Foundations", "Arc 1: Foundations"),
    ("sv-02-biblical-defilement", "02 -- Biblical Defilement", "Arc 1 -- Foundations", None),
    ("sv-03-tamid-doa-connection", "03 -- Daily-to-Annual Connection", "Arc 1 -- Foundations", None),
    ("sv-04-doa-ritual-sequence", "04 -- Day of Atonement Ritual", "Arc 1 -- Foundations", None),
    ("sv-04b-jubilee-festival-calendar", "04b -- Jubilee, Isaiah 61, and the Festival Calendar", "Arc 1 -- Foundations", None),

    ("sv-05-daniel-literary-architecture", "05 -- Literary Architecture of Daniel", "Arc 2 -- Daniel 8: The Vision", "Arc 2: Daniel 8 — The Vision"),
    ("sv-06-dan-8-verse-by-verse", "06 -- Daniel 8:8-19 Verse by Verse", "Arc 2 -- Daniel 8: The Vision", None),
    ("sv-07-dan-7-8-same-horn", "07 -- Same Horn in Daniel 7 and 8?", "Arc 2 -- Daniel 8: The Vision", None),
    ("sv-08-sanctuary-earthly-or-heavenly", "08 -- Earthly or Heavenly Sanctuary?", "Arc 2 -- Daniel 8: The Vision", None),
    ("sv-09-counterfeit-system", "09 -- The Counterfeit System", "Arc 2 -- Daniel 8: The Vision", None),
    ("sv-10-evening-morning-unit", "10 -- Evening-Morning: The Coded Unit", "Arc 2 -- Daniel 8: The Vision", None),

    ("sv-11-sealing-system", "11 -- The Sealing System", "Arc 3 -- The 70 Weeks and 2300 Days", "Arc 3: The 70 Weeks and 2300 Days"),
    ("sv-12-gabriel-return", "12 -- Gabriel's Return", "Arc 3 -- The 70 Weeks and 2300 Days", None),
    ("sv-13-seventy-weeks", "13 -- The 70 Weeks Prophecy", "Arc 3 -- The 70 Weeks and 2300 Days", None),
    ("sv-14-dan-924-six-purposes", "14 -- Daniel 9:24's Six Purposes", "Arc 3 -- The 70 Weeks and 2300 Days", None),
    ("sv-15-2300-calculation", "15 -- The 2300-Day Calculation", "Arc 3 -- The 70 Weeks and 2300 Days", None),

    ("sv-16-dan-10-12-resolution", "16 -- Daniel 10-12: The Resolution", "Arc 4 -- Judgment and Vindication", "Arc 4: Judgment and Vindication"),
    ("sv-17-judgment-antitypical-doa", "17 -- Judgment as Antitypical DOA", "Arc 4 -- Judgment and Vindication", None),
    ("sv-17b-vindication-as-process", "17b -- Vindication as Process, Not Instant", "Arc 4 -- Judgment and Vindication", None),
    ("sv-18-vindication-meaning", "18 -- What Does nitsdaq qodesh Mean?", "Arc 4 -- Judgment and Vindication", None),
    ("sv-19-righteousness-defilement-vindication", "19 -- Righteousness and Defilement Converge", "Arc 4 -- Judgment and Vindication", None),

    ("sv-20-rev-10-unsealing", "20 -- Revelation 10: The Little Book", "Arc 5 -- Revelation and the Maskilim", "Arc 5: Revelation and the Maskilim"),
    ("sv-21-three-angels", "21 -- The Three Angels' Messages", "Arc 5 -- Revelation and the Maskilim", None),
    ("sv-22-maskilim", "22 -- The Maskilim", "Arc 5 -- Revelation and the Maskilim", None),
    ("sv-23-grand-synthesis", "23 -- Grand Synthesis", "Arc 5 -- Revelation and the Maskilim", None),

    ("sv-24-hebrews-within-the-veil", "24 -- Hebrews and 'Within the Veil'", "Supplementary Studies", "Supplementary Studies"),
    ("sv-25-atonement-three-phases", "25 -- The Atonement: Three Phases", "Supplementary Studies", None),
    ("sv-26-colossians-2-14-ceremonial-law", "26 -- Colossians 2:14 and the Ceremonial Law", "Supplementary Studies", None),
    ("sv-27-leviticus-4-blood-transfer", "27 -- Leviticus 4 and Blood Transfer", "Supplementary Studies", None),
]

RAW_DATA_LABELS = {
    "concept-context.md": "Concept Context",
    "existing-studies.md": "Existing Studies",
    "grammar-references.md": "Grammar References",
    "greek-parsing.md": "Greek Parsing",
    "hebrew-parsing.md": "Hebrew Parsing",
    "naves-topics.md": "Nave's Topics",
    "naves-entries.md": "Nave's Entries",
    "parallels.md": "Cross-Testament Parallels",
    "strongs-lookups.md": "Strong's Lookups",
    "strongs.md": "Strong's Lookups",
    "strongs-data.md": "Strong's Data",
    "web-research.md": "Web Research",
    "external-corpus-verification.md": "External Corpus Verification",
}

def generate():
    lines = []
    lines.append("  - Studies:")
    current_arc = None

    for slug, title, arc, arc_comment in STUDIES:
        study_dir = DOCS / slug
        prefix = f"studies/{slug}"

        if arc != current_arc:
            current_arc = arc
            lines.append("")
            if arc_comment:
                lines.append(f"    # ── {arc_comment} ──")
            lines.append(f'    - "{arc}":')
            lines.append("")

        lines.append(f'      - "{title}":')
        lines.append(f"        - {prefix}/conclusion-simple.md")
        lines.append(f"        - Conclusion: {prefix}/CONCLUSION.md")
        lines.append(f"        - Analysis: {prefix}/03-analysis.md")
        lines.append(f"        - Verses: {prefix}/02-verses.md")

        if (study_dir / "04-word-studies.md").exists():
            lines.append(f"        - Word Studies: {prefix}/04-word-studies.md")

        lines.append(f"        - Topics: {prefix}/01-topics.md")
        lines.append(f"        - Research Scope: {prefix}/PROMPT.md")

        if (study_dir / "00-references.md").exists():
            lines.append(f"        - References: {prefix}/00-references.md")

        raw_dir = study_dir / "raw-data"
        if raw_dir.is_dir():
            raw_files = sorted(raw_dir.glob("*.md"))
            if raw_files:
                lines.append("        - Raw Data:")
                for rf in raw_files:
                    label = RAW_DATA_LABELS.get(rf.name, rf.stem.replace("-", " ").title())
                    lines.append(f'          - "{label}": {prefix}/raw-data/{rf.name}')

    return "\n".join(lines)


if __name__ == "__main__":
    print(generate())
