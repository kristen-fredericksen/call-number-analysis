# Claude Code Context: Call Number Analysis Skill

## Project Overview

You're helping Kristen (GitHub: kristen-fredericksen) build a **custom skill for analyzing library call numbers** from Alma Analytics data, plus a **Python script** that applies the skill's logic to batch-analyze spreadsheets. The skill helps identify miscoded MARC 852 first indicators by analyzing call number content rather than trusting the indicator value.

## Problem Being Solved

- The MARC 852 field's first indicator declares the call number scheme (0=LC, 1=Dewey, 8=Other, etc.)
- In real-world data, these indicators are frequently miscoded
- Alma Analytics normalizes call numbers differently based on the indicator
- Miscoded indicators produce obviously wrong normalization (e.g., LC call numbers coded as "8" get zero-padded)
- The skill detects these mismatches by analyzing call number content patterns

## Project Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The Skill — classification rules, decision tree, reference data |
| `src/analyze_852_indicators.py` | Python script that batch-analyzes Excel exports using the Skill's logic |
| `data/852_first_indicator_analyzed.xlsx` | Output from analyzing ~25,700 blank-indicator 852 records |
| `claude-code-context.md` | This file — project context for Claude |

## Key Technical Details

### 852 First Indicator Values
| Indicator | Meaning |
|-----------|---------|
| # (blank) | No information provided |
| 0 | Library of Congress classification |
| 1 | Dewey Decimal classification |
| 2 | National Library of Medicine classification |
| 3 | Superintendent of Documents classification |
| 4 | Shelving control number |
| 5 | Title |
| 6 | Shelved separately |
| 7 | Source specified in subfield $2 |
| 8 | Other scheme |

### Alma Analytics Normalization Rules

**LC (Indicator 0):**
- Format: `0` + lowercase class letters + normalizing char + class number + elements
- Normalizing character based on digit count: 1→space, 2→!, 3→", 4→#
- Decimal portions don't count toward digit selection
- Example: `QA24.D56` → `0qa!24 d56`

**Other Scheme (Indicator 8):**
- Numbers zero-padded to 12 digits
- Example: `Z43.A2` coded as 8 → `8z000000000043.a000000000002...`

### Detection Heuristic
If a normalized call number starts with `8` but contains patterns like `000000000` followed by small numbers that would make sense as LC class numbers, it's likely miscoded.

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
- **LC** (indicator 0) — valid LC class letters + number + cutter patterns, with spacing variations
- **Dewey** (indicator 1) — 3-digit start with optional decimal and cutter
- **NLM** (indicator 2) — W and QS-QZ classes
- **SuDoc** (indicator 3) — colon-based detection, Y class, agency stem patterns
- **Shelving control** (indicator 4) — AV formats (CD/DVD/VHS/Video/Fiche), local collection schemes
- **LAC** (indicator 7) — FC (Canadian history), PS8000+ (Canadian literature)
- **Not a call number** — staff notes, equipment, format descriptors alone, test data
- Strips shelving prefixes (OVERSIZE, DOCS, FOLIO, etc.) before classification

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
- Workflow checklist for manual analysis
- Decision tree for quick reference

The Skill and the script should stay in sync — if classification logic changes in one, update the other.

## Reference Documents

1. **Ex Libris documentation**: "Understanding normalized call numbers in Analytics" by Simon Hunt (2019)
2. **LC MARC 21 Holdings**: https://www.loc.gov/marc/holdings/hd852.html
3. **LC Classification Outline**: https://www.loc.gov/catdir/cpso/lcco/

## What's Been Done

1. Created initial SKILL.md with classification detection logic
2. Added all 852 indicator values from LC documentation
3. Emphasized content-based identification over indicator trust
4. Built Python script to batch-analyze Excel exports
5. Processed a 25,000+ row Excel file of blank-indicator 852 fields
6. Generated suggested corrections with confidence levels
7. Reviewed misclassifications and fixed:
   - SuDoc regex to handle slashes/hyphens before colons
   - LC regex to handle space-before-decimal patterns (e.g., `E 185 .5 B58`)
   - Added LAC classification detection (FC, PS8000+) with indicator 7
   - Expanded AV shelving detection (Video disc/CD/DVD/VHS, Fiche, multi-word prefixes)
   - Added shelving prefix stripping (OVERSIZE, DOCS, FOLIO, etc.)
   - Improved not-a-call-number detection (equipment, format descriptors alone, "current issues")
   - Softened colon = SuDoc rule (colons are very strong signal, but rarely can be errors)

## Data Quality Issues Encountered

- LC call numbers miscoded as indicator 8
- SuDoc numbers with complex stems (slashes, hyphens) miscoded as LC
- Local prefixes (DVD, Folio, Reference, OVERSIZE, DOCS) confused with LC classes
- LAC classifications (FC, PS8000+) not in LC schedule but structurally identical
- Equipment/supplies entered in call number fields
- Periodical title + browsing notes in call number fields
- Excel auto-formatting issues (dates like `1980-4-5` being converted)
- Need for text-forcing with apostrophe prefixes in output

## Next Steps / Open Questions

- Run updated script against the original data to see improved results
- Test against additional report outputs
- Possible reference files to create: `lcc-classes.md`, `alma-analytics-normalization.md`
- Consider adding more local scheme patterns as they're discovered
