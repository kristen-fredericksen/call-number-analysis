# CUNY Call Number Cleanup

Tools for systematically cleaning up MARC 852 fields across all 23 CUNY campuses. Pulls holdings data from Alma Analytics, analyzes every call number by content to identify indicator errors and subfield problems, and generates reports for campus catalogers.

## The Problem

CUNY's 23 libraries have hundreds of thousands of holdings records with 852 field issues:

- **Wrong first indicators** -- An LC call number coded as indicator 8 ("Other scheme") causes Alma Analytics to normalize it incorrectly, producing garbled output like `8qa000000000024.d000000000056...` instead of `0qa!24 d56`
- **Subfield coding errors** -- Cutters placed in $j instead of $i, classification data in the wrong subfield, prefixes not in $k
- **Non-call-number data** -- Staff notes, equipment descriptions, and shelving instructions entered in call number fields

This project identifies all of these by analyzing what each call number actually looks like, rather than trusting the indicator value.

## Workflow

1. **Pull** -- Retrieve all 852 data for a school from Alma Analytics via the API
2. **Analyze** -- Classify every call number, compare current vs suggested indicator, flag subfield errors
3. **Report** -- Send reports to campus catalogers showing what changes will be made
4. **Correct** -- Apply uncontested corrections via the Holdings API (planned)

Schools are processed one at a time, starting with trusted cataloging departments (Kingsborough CC, BMCC) before expanding to campuses with known data quality issues.

## What's Included

| File | Purpose |
|------|---------|
| `src/pull_852_analytics.py` | Pulls 852 data from the Alma Analytics API with pagination |
| `src/analyze_852_indicators.py` | Classifies call numbers, compares indicators, flags errors |
| `SKILL.md` | Classification rules, decision tree, and reference material for Claude |
| `docs/analytics-report.md` | Analytics report setup (columns, filters, paths per school) |
| `api_keys.env` | IZ API keys per school (not in git) |

## Classification

The analysis script suggests the correct 852 first indicator based on content:

| Indicator | Scheme | Examples |
|-----------|--------|----------|
| 0 | Library of Congress (LC) | `QA76.73.P98`, `E 185 .5 B58` |
| 1 | Dewey Decimal | `813.54`, `005.133` |
| 2 | National Library of Medicine (NLM) | `W1`, `QS 504` |
| 3 | Superintendent of Documents (SuDoc) | `C55.281/2-2:IM 1/2/CD`, `Y 4.J 89/1:` |
| 4 | Shelving control number | `DVD 2847`, `Video disc 1234`, `Fiche 500` |
| 7 | Library and Archives Canada (LAC) | `FC3695`, `PS8921.A7` |
| 8 | Other scheme | Call numbers that don't match any known scheme |
| -- | Not a call number | `Digital Projector`, `SHELVED UNDER TITLE` |

The output flags each record as Change Needed (Yes/No/Review) with color coding, and separates subfield errors from classification notes.

## Usage

### Requirements

```bash
pip install pandas openpyxl requests
```

### Pull data

Each school needs an API key in `api_keys.env` and a report path in the script's `REPORT_PATHS` dict. See `docs/analytics-report.md` for report setup.

```bash
python src/pull_852_analytics.py KB           # Pull one school
python src/pull_852_analytics.py KB BM        # Pull multiple schools
python src/pull_852_analytics.py --all        # Pull all schools with keys
```

### Analyze

```bash
python src/analyze_852_indicators.py data/KB_852_data.xlsx data/KB_852_analyzed.xlsx
```

The script auto-detects whether the input is from the pull script or a manual Alma Analytics export.

### Output

A formatted Excel workbook with three sheets:

1. **852 Field Analysis** -- every record with current and suggested indicators, change needed flag, classification type, confidence, subfield changes, and notes
2. **Statistics** -- counts and percentages by classification type and confidence
3. **By Institution** -- breakdown per campus

## References

- [MARC 21 Holdings 852 field](https://www.loc.gov/marc/holdings/hd852.html) -- Library of Congress
- [LC Classification Outline](https://www.loc.gov/catdir/cpso/lcco/) -- Library of Congress
- [Understanding normalized call numbers in Analytics](https://knowledge.exlibrisgroup.com/Alma/Community_Knowledge/Understanding_Normalized_Call_Numbers_in_Analytics) -- Simon Hunt, Ex Libris Community Knowledge Center (2019)

## License

This project is open source. Developed by Kristen Fredericksen with Claude.
