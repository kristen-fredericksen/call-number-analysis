# Call Number Analysis

Detect miscoded MARC 852 first indicators by analyzing call number content rather than trusting the indicator value.

## The Problem

The MARC 852 field's first indicator declares what classification scheme a call number uses (0 = LC, 1 = Dewey, 3 = SuDoc, etc.). In real-world library data, these indicators are frequently wrong. When Alma Analytics normalizes call numbers, it relies on the indicator to decide *how* to normalize -- so a miscoded indicator produces garbled output. For example, an LC call number like `QA24.D56` coded as indicator 8 ("Other scheme") gets zero-padded into `8qa000000000024.d000000000056...` instead of the correct `0qa!24 d56`.

This project detects these mismatches using content-based analysis: examining what the call number actually looks like rather than what the indicator says it is.

## What's Included

### Claude Skill (`SKILL.md`)

A standalone skill document containing classification rules, a decision tree, Alma Analytics normalization details, and a workflow checklist. Can be used directly with Claude to analyze call numbers interactively. Also contributed to [cuny-libraries/claude-skills](https://github.com/cuny-libraries/claude-skills).

### Python Script (`src/analyze_852_indicators.py`)

A batch analysis script that implements the skill's classification logic against Excel exports from Alma Analytics. It reads an input spreadsheet, classifies every call number, and produces a formatted output workbook with three sheets: detailed analysis, statistics, and institution breakdown.

## Suggested Indicators

For each call number, the script and skill suggest the correct 852 first indicator based on content analysis:

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

Additional features:
- Strips shelving prefixes (OVERSIZE, DOCS, FOLIO, REF, etc.) before classification
- Detects equipment, format descriptors, staff notes, and test data in call number fields
- Reports confidence levels (High, Medium, Low) for each classification
- Handles consortium data with per-institution breakdowns

## Usage

### Requirements

- Python 3.x
- pandas
- openpyxl

```bash
pip install pandas openpyxl
```

### Running the Script

```bash
python src/analyze_852_indicators.py input.xlsx output.xlsx
```

### Input Format

Excel (.xlsx) exports from Alma Analytics with these columns:

| Column | Description |
|--------|-------------|
| Permanent Call Number | The call number as stored |
| Permanent Call Number Type | Alma's classification type |
| 852 MARC | Full MARC 852 field with subfields |
| Normalized Call Number | Alma's normalized form |
| Institution Name | Owning institution |
| MMS Id | Alma record identifier |

The script skips 2 header rows and 1 sub-header row typical of Alma Analytics exports.

### Output

A formatted Excel workbook with three sheets:

1. **Analysis** -- every record with suggested indicator, classification type, confidence level, and explanatory notes
2. **Statistics** -- counts and percentages by classification type and confidence
3. **By Institution** -- breakdown of classifications per institution (useful for consortium data)

## References

- [MARC 21 Holdings 852 field](https://www.loc.gov/marc/holdings/hd852.html) -- Library of Congress
- [LC Classification Outline](https://www.loc.gov/catdir/cpso/lcco/) -- Library of Congress
- [Understanding normalized call numbers in Analytics](https://knowledge.exlibrisgroup.com/Alma/Community_Knowledge/Understanding_Normalized_Call_Numbers_in_Analytics) -- Simon Hunt, Ex Libris Community Knowledge Center (2019)

## License

This project is open source. Developed by Kristen Fredericksen with Claude.
