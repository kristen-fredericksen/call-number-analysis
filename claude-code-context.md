# Claude Code Context: Call Number Analysis Skill

## Project Overview

You're helping Kristen (GitHub: kristen-fredericksen) build a **custom skill for analyzing library call numbers** from Alma Analytics data, plus a **Python script** that applies the skill's logic to batch-analyze spreadsheets. The skill helps identify miscoded MARC 852 first indicators by analyzing call number content rather than trusting the indicator value.

## Problem Being Solved

- The MARC 852 field's first indicator declares the call number scheme (0=LC, 1=Dewey, 8=Other, etc.)
- In real-world data, these indicators are frequently miscoded
- Alma Analytics normalizes call numbers differently based on the indicator
- Miscoded indicators produce obviously wrong normalization (e.g., LC call numbers coded as "8" get zero-padded)
- The skill detects these mismatches by analyzing call number content patterns

## Repositories

- **Personal repo**: https://github.com/kristen-fredericksen/call-number-analysis (script + skill)
- **Contributed skill**: https://github.com/cuny-libraries/claude-skills/pull/1 (PR open, needs updating with latest SKILL.md)
- **Fork**: https://github.com/kristen-fredericksen/claude-skills (used for the PR)

## Project Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The Skill — classification rules, decision tree, location codes, reference data |
| `src/analyze_852_indicators.py` | Python script that batch-analyzes Excel exports using the Skill's logic |
| `data/852_first_indicator_analyzed_v3.xlsx` | Latest output from analyzing ~25,665 blank-indicator 852 records |
| `README.md` | GitHub repo front page |
| `claude-code-context.md` | This file — project context for Claude |

## Key Technical Details

### 852 First Indicator Values
| Indicator | Meaning | Subfield |
|-----------|---------|----------|
| # (blank) | No information provided | |
| 0 | Library of Congress classification | $h/$i |
| 1 | Dewey Decimal classification | $h/$i |
| 2 | National Library of Medicine classification | $h/$i |
| 3 | Superintendent of Documents classification | $h/$i |
| 4 | Shelving control number | **$j** (not $h) |
| 5 | Title | **$l** (not $h) |
| 6 | Shelved separately | |
| 7 | Source specified in subfield $2 | $h/$i |
| 8 | Other scheme | $h/$i |

**Important MARC distinctions:**
- Indicator 4 uses **$j** — arbitrary shelving arrangement, not a classification (e.g., microfilm numbers, accession numbers)
- Indicator 5 uses **$l** — shelving form of title (e.g., `NYT MAG`), not $h
- Indicator 8 uses **$h** — a real classification scheme, just not LC/Dewey/NLM/SuDoc (e.g., `Fic`, `Per`, `M`)

### Alma Analytics Normalization Rules

**LC (Indicator 0):**
- Format: `0` + lowercase class letters + normalizing char + class number + elements
- Normalizing character based on digit count: 1→space, 2→!, 3→", 4→#
- Decimal portions don't count toward digit selection
- Example: `QA24.D56` → `0qa!24 d56`

**Other Scheme (Indicator 8):**
- Numbers zero-padded to 12 digits
- Example: `Z43.A2` coded as 8 → `8z000000000043.a000000000002...`

## The Python Script (`src/analyze_852_indicators.py`)

### What It Does
- Reads an Excel export from Alma Analytics (with specific column layout)
- Parses 852 MARC fields to extract call numbers from $$h/$$i/$$j subfields (ignoring $$k prefixes)
- Classifies each call number by content analysis to suggest the correct 852 first indicator
- Outputs a formatted Excel workbook with 3 sheets: detailed analysis, statistics, and institution breakdown

### Usage
```bash
python analyze_852_indicators.py input.xlsx output.xlsx
```

### Classification Capabilities
The script detects:
- **LC** (indicator 0) — valid LC class letters + number + cutter, including:
  - Attached cutters (`BF723.C5 D495`)
  - Spaced cutters (`E 185 .5 B58`)
  - Three-letter classes (`KFN`, `KJC`, `KTQ`) via two-letter parent lookup
  - Lowercase call numbers (`pn 6112`)
  - CIP/preliminary numbers (MLCS) — flagged with low confidence
- **Dewey** (indicator 1) — 3-digit start with optional decimal and cutter
- **NLM** (indicator 2) — W and QS-QZ classes
- **SuDoc** (indicator 3) — colon-based detection, Y class, agency stem patterns
- **Shelving control** (indicator 4) — AV formats (CD/DVD/VHS/Video/Fiche), local collection schemes, format/collection codes
- **LAC** (indicator 7) — FC (Canadian history), PS8000+ (Canadian literature)
- **Not a call number** — staff notes, equipment, format descriptors alone, test data
- Strips shelving prefixes (OVERSIZE, DOCS, FOLIO, SPEC, REF, etc.) before classification

### Latest Run (v3)
| Classification | Count |
|---|---|
| Library of Congress | 20,464 |
| Shelving control number | 2,795 |
| Other scheme | 1,084 |
| Title | 536 |
| SuDoc | 531 |
| Not a call number | 175 |
| Local scheme | 40 |
| Dewey | 15 |
| NLM | 14 |
| LAC | 11 |

### Input Format
Excel (.xlsx) exports from Alma Analytics with columns:
- Permanent Call Number
- Permanent Call Number Type
- 852 MARC (full field with subfields)
- Normalized Call Number
- Institution Name
- MMS Id

Note: The script skips 2 header rows and 1 sub-header row typical of Alma Analytics exports.

## The Skill (`SKILL.md`)

Contains the classification rules the script implements, plus:
- Alma Analytics normalization algorithm details
- Consortium-specific data quality patterns (CUNY examples)
- CUNY location codes organized by classification hint (gov docs, special collections, AV/media)
- Known limitations (colonless SuDoc, G-schedule colon exception)
- Workflow checklist for manual analysis
- Decision tree for quick reference

The Skill and the script should stay in sync — if classification logic changes in one, update the other.

## Reference Documents

1. **Ex Libris documentation**: "Understanding normalized call numbers in Analytics" by Simon Hunt (2019)
2. **LC MARC 21 Holdings**: https://www.loc.gov/marc/holdings/hd852.html
3. **LC Classification Outline**: https://www.loc.gov/catdir/cpso/lcco/

## Data Sources

- **Locations spreadsheet**: `/Users/kristenfredericksen/Library/CloudStorage/OneDrive-CUNY/Alma reports/NZ Alma reports/CUNY locations 2026.02.28.xlsx` (1,002 CUNY locations)
- **Analysis input**: `/Users/kristenfredericksen/Library/CloudStorage/OneDrive-CUNY/Downloads - CUNY/852 first indicator _-3.xlsx` (25,665 records)

## What's Been Done

1. Created initial SKILL.md with classification detection logic
2. Built Python script to batch-analyze Excel exports
3. First round of fixes (SuDoc regex, LC spacing, LAC, AV shelving, prefix stripping, equipment detection)
4. Code review: fixed 9 issues (bugs, inconsistencies, inefficiencies), 40+ tests pass
5. Published to GitHub (personal repo + PR to cuny-libraries/claude-skills)
6. Added README
7. Documented G-schedule colon exception (LC call numbers with colons in table notation)
8. Second round of fixes based on disagreement review (~4,200 rows):
   - LC attached cutter regex (`BF723.C5`) — rescued ~2,940 records from "Other scheme"
   - AV detection no longer grabs LC class CD when cutter follows
   - Three-letter LC classes via two-letter parent lookup
   - Case-insensitive LC matching
   - SPEC added as shelving prefix
   - CIP/MLCS preliminary numbers flagged with low confidence
   - Format/collection code pattern correctly handles `VC A54` (LC requires digits after class)
   - Colonless SuDoc documented as known limitation (needs location context)
9. Added CUNY location codes to SKILL.md (gov docs, special collections, AV/media)

## Known Limitations

- **Colonless SuDoc**: `A 1.2 F 51/3` looks like LC from content alone. Location codes (DOCS, CUSP0) are needed to identify these as SuDoc.
- **G-schedule colons**: LC numbers like `G1254.N4:2M3` (table notation) will be misclassified as SuDoc. Exceedingly rare.
- **Indicator 4 vs 8 distinction**: The script doesn't yet fully distinguish between shelving control numbers ($j) and other schemes ($h). See "Open Questions" below.

## Open Questions / Next Session

1. **Indicator 4 vs 8 vs "not a call number" reclassification**: MARC distinguishes between shelving control ($j, arbitrary arrangement) and other scheme ($h, real classification). The script currently conflates some of these. Examples:
   - "DVD 2847" → indicator 4 ($j) — correct
   - "Periodical" → currently "not a call number" but may be indicator 8 ($h, simplified classification)
   - "Fic Adams" → indicator 8 ($h, local classification scheme)
   - "Digital Projector" → genuinely not a call number

2. **Indicator 5 (title)**: Uses $l (shelving form of title), not $h. The script currently classifies "Thesis" and "Dissertation" as indicator 5, which may be wrong since those are in $h.

3. **Periodicals locations**: Not yet added to SKILL.md (47 locations identified).

4. **Update the PR**: The PR to cuny-libraries/claude-skills still has the old SKILL.md. Push the latest version to the fork to update it.

5. **Full LC class list**: The user offered to provide a complete list from Classification Web. The current three-letter class workaround (check if first two letters are valid) works but isn't authoritative.

6. **Remaining "Other scheme" (1,084 records)**: Worth spot-checking to find more patterns.
