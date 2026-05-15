#!/usr/bin/env python3
"""
Build script for sv-website.
Copies study files from bible-studies/sv-* to docs/studies/sv-*.
Generates verses.json and strongs.json for the popup system.
"""

import os
import re
import json
import shutil
from pathlib import Path

BIBLE_STUDIES = Path(r"D:\bible\bible-studies")
DOCS_STUDIES = Path(__file__).parent / "docs" / "studies"
KJV_PATH = Path(r"D:\bible\tools\data\kjv.txt")
STRONGS_DB = Path(r"D:\bible\tools\data\strongs_translations.db")
JS_DIR = Path(__file__).parent / "docs" / "javascripts"

SV_PREFIXES = ["sv-"]

COPY_FILES = [
    "CONCLUSION.md",
    "conclusion-simple.md",
    "03-analysis.md",
    "02-verses.md",
    "04-word-studies.md",
    "01-topics.md",
    "PROMPT.md",
    "00-references.md",
]

RAW_DATA_PATTERNS = [
    "concept-context.md",
    "hebrew-parsing.md",
    "greek-parsing.md",
    "naves-topics.md",
    "naves-entries.md",
    "parallels.md",
    "strongs-lookups.md",
    "strongs.md",
    "strongs-data.md",
    "grammar-references.md",
    "existing-studies.md",
    "web-research.md",
]


def copy_studies():
    """Copy study files from bible-studies to docs/studies."""
    copied = 0
    for study_dir in sorted(BIBLE_STUDIES.iterdir()):
        if not study_dir.is_dir():
            continue
        if not any(study_dir.name.startswith(p) for p in SV_PREFIXES):
            continue

        dest = DOCS_STUDIES / study_dir.name
        dest.mkdir(parents=True, exist_ok=True)

        for fname in COPY_FILES:
            src = study_dir / fname
            if src.exists():
                shutil.copy2(src, dest / fname)
                copied += 1

        raw_src = study_dir / "raw-data"
        if raw_src.is_dir():
            raw_dest = dest / "raw-data"
            raw_dest.mkdir(exist_ok=True)
            for fname in RAW_DATA_PATTERNS:
                src = raw_src / fname
                if src.exists():
                    shutil.copy2(src, raw_dest / fname)
                    copied += 1
            # Also copy any other .md files in raw-data
            for f in raw_src.glob("*.md"):
                if f.name not in RAW_DATA_PATTERNS:
                    shutil.copy2(f, raw_dest / f.name)
                    copied += 1

    print(f"Copied {copied} files")
    return copied


def build_verses_json():
    """Build verses.json from KJV text for popup system."""
    if not KJV_PATH.exists():
        print("KJV text not found, skipping verses.json")
        return

    book_map = {
        'Genesis': 'Gen', 'Exodus': 'Exo', 'Leviticus': 'Lev',
        'Numbers': 'Num', 'Deuteronomy': 'Deu', 'Joshua': 'Jos',
        'Judges': 'Jdg', 'Ruth': 'Rth', '1 Samuel': '1Sa',
        '2 Samuel': '2Sa', '1 Kings': '1Ki', '2 Kings': '2Ki',
        '1 Chronicles': '1Ch', '2 Chronicles': '2Ch', 'Ezra': 'Ezr',
        'Nehemiah': 'Neh', 'Esther': 'Est', 'Job': 'Job',
        'Psalms': 'Psa', 'Proverbs': 'Pro', 'Ecclesiastes': 'Ecc',
        'Song of Solomon': 'Sng', 'Isaiah': 'Isa', 'Jeremiah': 'Jer',
        'Lamentations': 'Lam', 'Ezekiel': 'Ezk', 'Daniel': 'Dan',
        'Hosea': 'Hos', 'Joel': 'Jol', 'Amos': 'Amo',
        'Obadiah': 'Oba', 'Jonah': 'Jon', 'Micah': 'Mic',
        'Nahum': 'Nah', 'Habakkuk': 'Hab', 'Zephaniah': 'Zep',
        'Haggai': 'Hag', 'Zechariah': 'Zec', 'Malachi': 'Mal',
        'Matthew': 'Mat', 'Mark': 'Mrk', 'Luke': 'Luk',
        'John': 'Jhn', 'Acts': 'Act', 'Romans': 'Rom',
        '1 Corinthians': '1Co', '2 Corinthians': '2Co',
        'Galatians': 'Gal', 'Ephesians': 'Eph', 'Philippians': 'Php',
        'Colossians': 'Col', '1 Thessalonians': '1Th',
        '2 Thessalonians': '2Th', '1 Timothy': '1Ti',
        '2 Timothy': '2Ti', 'Titus': 'Tit', 'Philemon': 'Phm',
        'Hebrews': 'Heb', 'James': 'Jas', '1 Peter': '1Pe',
        '2 Peter': '2Pe', '1 John': '1Jn', '2 John': '2Jn',
        '3 John': '3Jn', 'Jude': 'Jud', 'Revelation': 'Rev'
    }

    verses = {}
    pattern = re.compile(r'^(.+?)\s+(\d+):(\d+)\t(.+)$')

    with open(KJV_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if not m:
                continue
            book_full, ch, vs, text = m.groups()
            abbr = book_map.get(book_full, book_full[:3])
            chapter_key = f"{abbr} {ch}"
            verse_key = f"{abbr} {ch}:{vs}"
            if chapter_key not in verses:
                verses[chapter_key] = {}
            verses[chapter_key][verse_key] = text

    JS_DIR.mkdir(parents=True, exist_ok=True)
    out = JS_DIR / "verses.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(verses, f, separators=(',', ':'))
    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"Built verses.json ({size_mb:.1f} MB)")


def build_strongs_json():
    """Build strongs.json from the strongs database."""
    import sqlite3
    if not STRONGS_DB.exists():
        print("Strong's DB not found, skipping strongs.json")
        return

    conn = sqlite3.connect(str(STRONGS_DB))
    cur = conn.cursor()

    strongs = {}
    try:
        cur.execute("SELECT strongs_number, word, transliteration, definition FROM lexicon")
        for num, word, translit, defn in cur.fetchall():
            strongs[num] = {
                "word": word or "",
                "translit": translit or "",
                "def": (defn or "")[:300]
            }
    except Exception as e:
        print(f"Error reading Strong's DB: {e}")
        # Try alternate table structure
        try:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [r[0] for r in cur.fetchall()]
            print(f"Available tables: {tables}")
        except:
            pass
    finally:
        conn.close()

    if strongs:
        out = JS_DIR / "strongs.json"
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(strongs, f, separators=(',', ':'))
        print(f"Built strongs.json ({len(strongs)} entries)")
    else:
        print("No Strong's data found")


if __name__ == "__main__":
    import sys

    if "--copy" in sys.argv or len(sys.argv) == 1:
        copy_studies()

    if "--verses" in sys.argv or len(sys.argv) == 1:
        build_verses_json()

    if "--strongs" in sys.argv or len(sys.argv) == 1:
        build_strongs_json()
