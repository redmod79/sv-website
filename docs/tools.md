# Research Tools & Process

## How Each Study Was Built

Every study folder contains the complete research trail — from initial scope discovery through final conclusion. Here's what each file represents:

### Research Files

| File | Phase | Agent | Purpose |
|------|-------|-------|---------|
| `00-references.md` | 1 | Reference Agent | Prior studies found, external corpus leads |
| `PROMPT.md` | 2 | Scoping Agent | Tool-discovered scope: topics, verses, Strong's numbers, focus areas |
| `01-topics.md` | 3 | Research Agent | Nave's Topical Dictionary entries retrieved |
| `02-verses.md` | 3 | Research Agent | Full KJV verse text with chapter context |
| `04-word-studies.md` | 3 | Research Agent | Strong's word data, library references, parsing results |
| `03-analysis.md` | 4 | Analysis Agent | Verse-by-verse analysis, patterns, synthesis |
| `CONCLUSION.md` | 4 | Analysis Agent | Final conclusion with all evidence |
| `conclusion-simple.md` | 5 | Summary Agent | Plain-language summary for general readers |

### What "Tool-Discovered" Means

The scoping agent finds verses by querying Nave's Topical Dictionary and Strong's Concordance — it does NOT rely on training knowledge to select verses. This means:

- **Verses you wouldn't expect** may appear — tools find connections humans miss
- **Common proof-texts may be absent** if the tools didn't surface them for this specific question
- **The scope is reproducible** — running the same queries produces the same scope

### Interactive Features

This website includes:

- **Verse Popups** — Click any Bible reference (e.g., Daniel 8:14) to see the verse text with surrounding context
- **Strong's Popups** — Click any Strong's number (e.g., H6663) to see the Hebrew/Greek word and definition
- **Study History** — Navigate between studies with the floating history widget
- **Blue Letter Bible Links** — Hebrew and Greek words link to their BLB lexicon entries
