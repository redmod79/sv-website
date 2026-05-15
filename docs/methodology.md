# Methodology

## Research Pipeline

Each study in this series was produced through a multi-agent pipeline (bible-study5) with five phases:

1. **Reference Gathering** — A reference agent searches for prior studies in the library, reads completed series studies, and queries external corpora (Ellen G. White writings, Secrets Unsealed) for research leads.

2. **Scope Discovery** — A scoping agent uses tools (not training knowledge) to discover the study's scope: Nave's Topical Dictionary queries, Strong's concordance searches, and verse reference extraction. The output is a PROMPT.md file listing every verse, topic, and word to investigate.

3. **Library Generation** — Missing word studies and grammar references are generated as canonical entries before research begins, ensuring the research agent has comprehensive data.

4. **Data Gathering** — A research agent retrieves full verse text with chapter context, runs cross-testament parallels in both directions, parses Hebrew and Greek morphology, and organizes all data into structured files. The research agent does NOT interpret — it only gathers.

5. **Analysis** — An analysis agent reads the clean research files and produces verse-by-verse analysis, pattern identification, and a comprehensive conclusion. Every claim requires verse support.

## Interpretive Principles

- **Scripture interprets Scripture** — meaning is derived from how the Bible itself uses terms, not from external theological frameworks
- **Contextual analysis** — expanding circles: verse → chapter → book → same author → cross-testament
- **Historical-grammatical method** — Hebrew and Greek grammar inform meaning; context must match before importing meaning across passages
- **Scripture is the only authority for doctrine** — external corpora (EGW, church fathers) are research leads, not evidence
- **Consistency** — answers must be consistent with ALL analyzed verses, not just selected proof-texts

## Series Reference Boundary

Each study's final analysis and conclusion may ONLY cite studies completed earlier in the series. This prevents:

- **Circular reasoning** — Study 18 cannot cite Study 23's synthesis to support its own claims
- **Anachronistic reading** — each study stands on its own evidence at the time it was written
- **Cherry-picking** — the series builds progressively, not retrospectively

The reference agent, scoping agent, and research agent may use the full study library. The restriction applies ONLY to 03-analysis.md and CONCLUSION.md.

## Tools Used

All tools are local Python scripts running against local databases:

- **Nave's Topical Dictionary** — 5,319 topics with verse references
- **Strong's Concordance** — Hebrew, Aramaic, and Greek word database with translation distributions
- **Hebrew Parser** (Text-Fabric/BHSA) — morphological parsing, clause structure, construct chains
- **Greek Parser** (Text-Fabric/N1904) — morphological parsing, tense/voice/mood analysis
- **Cross-Testament Parallels** — hybrid scoring (semantic + keyword + theological phrase matching)
- **Concept Context** — finds verses with same theological concepts, prioritized by proximity
- **Grammar Reference Search** — semantic search across 10 Hebrew/Greek grammar textbooks
- **Word Studies Library** — 500+ canonical word studies by Strong's number
- **Grammar Reference Library** — Hebrew stems, Greek tenses, passage analyses

No internet searches were used for biblical evidence. Web resources (Blue Letter Bible) supplement lexicon data only.
