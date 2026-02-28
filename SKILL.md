---
name: call-number-analysis
description: Analyze, parse, validate, and classify library call numbers including LC, Dewey, SuDoc, NLM, and LAC (Library and Archives Canada). Use this skill whenever working with call numbers, shelf locations, or bibliographic data containing call numbers. Triggers include any mention of LC call numbers, LCC, Dewey Decimal, SuDoc, government documents classification, NLM, LAC, FC class (Canadian history), PS8000 (Canadian literature), call number parsing, call number normalization, shelf order, classifying items by subject using call numbers, distinguishing local prefixes (like DVD, REF, OVERSIZE) from valid classification schemes, analyzing 852 MARC fields, identifying miscoded 852 indicators, or working with Alma/Ex Libris Analytics call number data. Also use when asked to identify subject areas from call numbers, validate whether a call number follows LC/Dewey/SuDoc conventions, or detect non-call-number data (notes, instructions) in call number fields. ALWAYS consult this skill before claiming any alphabetic prefix is or is not a valid LC class, and ALWAYS check for colons when distinguishing SuDoc from LC.
---

# Call Number Analysis Skill

## Purpose
Analyze, parse, validate, and normalize call numbers from library holdings data, with specific support for Alma Analytics normalized call number formats.

## When to Use
- Analyzing call numbers from MARC 852 fields
- Working with Alma Analytics reports containing normalized call numbers
- Filtering or querying call number ranges in Analytics
- Identifying miscoded call numbers (wrong 852 indicator)
- Sorting or comparing call numbers
- Validating classification scheme identification
- Detecting non-call-number data entered in call number fields

## Critical Principle: Content-Based Identification

**Do NOT trust the MARC 852 first indicator blindly.** The indicator is frequently miscoded in real-world data. Always:

1. **Analyze the call number content first** to determine the actual classification scheme
2. **Use the indicator only as a hint**, not as authoritative
3. **Flag mismatches** between indicator and content for review

### Consortium Environments

In consortium environments (like CUNY, SUNY, CSU, etc.), local schemes vary by campus. What looks like an unrecognized pattern may be a valid local scheme at one institution but not exist at others.

**Examples from CUNY campuses:**

| Institution | Local Pattern | Description |
|-------------|---------------|-------------|
| City College | `05 .S381 KB V.2` | Music library shelving scheme |
| City College | `102 102` | Numeric local scheme |
| Queens College | `BRL 200-11` | Special collection codes |
| Hunter College | `ALLIGER.1.BOOK` | Named collection |
| Hunter College | `81-1009` | Accession numbers |
| Hostos | `Browse D`, `Browse G` | Browsing collection by subject |
| Baruch | `.T46 1995` | Malformed LC (missing class letters) |

**Recommendations for consortium data:**

1. **Analyze by institution** — Break down "Other scheme" and "Unknown" categories by campus
2. **Look for patterns** — Multiple similar entries at one campus suggest a local scheme, not errors
3. **Check location codes** — The $$c subfield may indicate special collections with their own schemes
4. **Don't assume errors** — A pattern unfamiliar to you may be intentional at that campus
5. **Document campus-specific schemes** — Build a reference of known local patterns per institution

### Common Data Quality Issues
- LC call numbers coded as "Other scheme" (indicator 8 instead of 0)
- LC call numbers with irregular spacing (e.g., `BX 1758.2 M53`) still valid but may fail validation
- Local prefixes (DVD, Folio, Reference) mistaken for LC class letters
- SuDoc numbers coded as LC (and vice versa—especially problematic with single-letter classes)
- NLM call numbers (W, QS-QZ) coded incorrectly
- Staff notes or circulation instructions entered in call number fields

## Classification Scheme Identification

### By Content Analysis (Primary Method)

#### Key Differentiators

| Feature | LC | SuDoc | Dewey | NLM |
|---------|-----|-------|-------|-----|
| **Starts with** | Valid LC letters | Agency stem | 3 digits | W or QS-QZ |
| **Has colon (:)** | Never* | Almost always | Never | Never |
| **Class structure** | Letters + number + cutter | Agency.bureau:series | Number + decimal + cutter | Letters + number + cutter |

*\* LC call numbers do not use colons structurally. A colon in an LC-looking call number is almost always SuDoc; very rarely it may be a data entry error. See "The Colon Rule" below.*

#### SuDoc vs LC: The Colon Rule

**The colon (`:`) is the strongest single indicator of SuDoc classification.** A call number containing a colon is almost always SuDoc. LC call numbers do not use colons as part of their structure, so a colon in what looks like an LC call number is either SuDoc or (very rarely) a data entry error.

**In practice:** Treat a colon as strong evidence of SuDoc, but not absolute proof. If the content before the colon matches a SuDoc agency stem pattern (letter(s) + number.number), it's SuDoc with high confidence. If the colon appears in an otherwise clearly LC-structured call number with no SuDoc stem pattern, flag it for review as a possible error.

| Call Number | Classification | Why |
|-------------|---------------|-----|
| `A 1.10:976` | SuDoc | Has colon, SuDoc agency stem pattern |
| `A 13.114/2:D 22/` | SuDoc | Has colon, SuDoc pattern |
| `Y 4.J 89/1:S 53/5` | SuDoc | Has colon (Y = Congressional) |
| `D 104.2:D 43/5` | SuDoc | Has colon, D = Defense |
| `GA 1.16/3-3: 996` | SuDoc | Has colon, GA = General Accounting Office |
| `HE 20.3152:` | SuDoc | Has colon, HE = HHS |
| `HE 20 .S37` | LC | No colon, valid LC class HE |
| `BX 1758.2 M53` | LC | No colon, valid LC class BX |
| `BX1758.2 .M53` | LC | Same as above, different spacing |

**Note:** Some SuDoc numbers have complex stems with slashes and hyphens before the colon (e.g., `C55.281/2-2:IM 1/2/CD`, `D 5.12/2: 6-03.7`). Always scan the full string for a colon, not just the portion immediately after the agency stem.

#### Valid LC Classification Letters

LC uses letters A-Z **except I, O, W, X, and Y**:
- **Valid single letters**: A, B, C, D, E, F, G, H, J, K, L, M, N, P, Q, R, S, T, U, V, Z
- **Invalid/Not used**: I, O, W, X, Y

**Y is always SuDoc** (Congressional documents), never LC.

Common LC two-letter classes include: AC, AE, AG, AI, AM, AN, AP, AS, AY, AZ, BC, BD, BF, BH, BJ, BL, BM, BP, BQ, BR, BS, BT, BV, BX, CB, CC, CD, CE, CJ, CN, CR, CS, CT, DA, DB, DC, DD, DE, DF, DG, DH, DJ, DK, DL, DP, DQ, DR, DS, DT, DU, DX, GA, GB, GC, GE, GF, GN, GR, GT, GV, HA, HB, HC, HD, HE, HF, HG, HJ, HM, HN, HQ, HS, HT, HV, HX, JA, JC, JF, JJ, JK, JL, JN, JQ, JS, JV, JX, JZ, KD-KZ series, LA, LB, LC, LD, LE, LF, LG, LH, LJ, LT, ML, MT, NA, NB, NC, ND, NE, NK, NX, PA, PB, PC, PD, PE, PF, PG, PH, PJ, PK, PL, PM, PN, PQ, PR, PS, PT, PZ, QA, QB, QC, QD, QE, QH, QK, QL, QM, QP, QR, RA, RB, RC, RD, RE, RF, RG, RJ, RK, RL, RM, RS, RT, RV, RX, RZ, SB, SD, SF, SH, SK, TA, TC, TD, TE, TF, TG, TH, TJ, TK, TL, TN, TP, TR, TS, TT, TX, UA, UB, UC, UD, UE, UF, UG, UH, VA, VB, VC, VD, VE, VF, VG, VK, VM, ZA.

#### NLM (National Library of Medicine)

NLM uses class letters that would otherwise be LC:
- **W** (and WA-WZ): Medicine and related subjects
- **QS-QZ**: Preclinical sciences (QS=Anatomy, QT=Physiology, QU=Biochemistry, QV=Pharmacology, QW=Microbiology, QX=Parasitology, QY=Clinical pathology, QZ=Pathology)

If a call number starts with W or QS-QZ followed by a number, it's likely NLM (indicator 2), not LC.

#### LAC (Library and Archives Canada)

LAC uses two classification ranges that overlap structurally with LC but are not part of the LC schedule:

| Class | Subject | Notes |
|-------|---------|-------|
| **FC** | Canadian history | Not a valid LC class — FC is not in the LC schedule at all |
| **PS8000+** | Canadian literature | PS is a valid LC class (American literature), but the 8000+ range is exclusively LAC |

These follow the same structural pattern as LC (letters + number + cutter), so they look like LC call numbers. The distinction matters for proper indicator coding:

| Call Number | Classification | Indicator |
|-------------|---------------|-----------|
| `FC3695 .B67 A74 2009` | LAC (Canadian history) | 7 (with $2) |
| `PS8001 .A77 Z88 1997` | LAC (Canadian literature) | 7 (with $2) |
| `PS3515 .E37 Z5 1970` | LC (American literature) | 0 |

**Detection rules:**
- **FC** + number → always LAC (FC is not a valid LC class)
- **PS** + number ≥ 8000 → LAC (Canadian literature)
- **PS** + number < 8000 → LC (American literature)

#### Dewey Decimal Patterns

Dewey call numbers start with exactly 3 digits, with several format variations:

| Pattern | Example | Notes |
|---------|---------|-------|
| 3 digits + decimal | `394.26` | Standard Dewey |
| 3 digits + decimal + Cutter | `398.2 C198T` | Common format |
| 3 digits + Cutter | `394 S847G` | Compact format (no decimal) |
| 3 digits + decimal + Cutter + date | `629.22 T245C 2015` | With publication year |

**Note**: Three digits repeated (like `102 102` or `171 171`) are typically local shelving schemes, not Dewey.

#### SuDoc (Superintendent of Documents)

Common SuDoc agency stems:
- **A** = Agriculture
- **C** = Commerce  
- **D** = Defense
- **E** = Energy
- **ED** = Education
- **EP** = EPA
- **HE** = Health and Human Services
- **I** = Interior
- **J** = Justice
- **L** = Labor
- **S** = State
- **T** = Treasury
- **Y** = Congress (Y 1 = Congressional Record, Y 4 = Committee prints)

**Key pattern**: `Agency stem` + `number.number` + `:` + `item designation`

Examples: `A 1.10:976`, `Y 4.J 89/1:S 53/5`, `HE 20.3152:P 94`

### Detecting Non-Call-Numbers

Call number fields sometimes contain staff notes, circulation instructions, test data, or other non-classification data. Flag these for cleanup:

| Pattern | Examples |
|---------|----------|
| Access/availability notes | "Access for Bronx Community College users", "Access: Brooklyn Web workstations", "Access through Lehman WEB workstations" |
| Shelving instructions | "SHELVED BY TITLE", "SHELVED UNDER TITLE", "Shelved by Author" |
| Circulation notes | "ASK AT MICROFORMS DESK", "Please Inquire at the Circulation Desk" |
| Staff instructions | "See reference librarian", "Thesis Ask librarian for DVD" |
| Reserve/restriction notes | "Kept on Reserve Shelf", "Non-circulating", "1-week loan" |
| Cataloging notes | "CATALOGED SEPARATELY", "Cataloged separately" |
| URLs | Any value starting with `http://` or `https://` |
| Status notes | "Missing", "Withdrawn", "Superseded" |
| Volume-only notation | "* Vol. 10, no. 2 and 3 (1983)" (asterisk + volume, no classification) |
| Format descriptors | "CD ROM", "CD Rhymes", "DVD Video" (descriptive, not shelving numbers) |
| Encoding placeholders | "e-ur---" (MARC country/language codes entered in wrong field) |
| **Test/placeholder data** | "test", "sample", "dummy", "temp", "xxx", "zzz", "tbd", "n/a", "none" |
| **Punctuation-only** | "???", "...", "---" |
| **Equipment/supplies** | "Digital Projector", "Dry erase marker", "Laptop charger" (physical items, not information resources) |
| **Format descriptor alone** | "DVD", "CD", "VHS" (format name with no number — not a shelving scheme) |
| **Title + shelving instruction** | "SHELVED UNDER TITLE Current issues in periodicals", "Financial Times current issues" (periodical title with browsing note) |

These should be flagged as "Not a call number" rather than assigned an indicator.

### AV Format Prefixes vs. LC Classes

Some AV format prefixes are also valid LC class letters. Distinguish by structure:

| Call Number | Classification | Reasoning |
|-------------|---------------|-----------|
| `CD 1811` | Shelving control (4) | Format + accession number, no cutter |
| `CD 1812` | Shelving control (4) | Format + accession number, no cutter |
| `CD921 .S65` | LC (0) | Class CD (Diplomatics) + number + cutter |
| `DVD 456` | Shelving control (4) | Format + accession number |
| `DVD 792 .S65` | Ambiguous | Could be either—check context |

**Rule:** If the pattern is `[AV prefix] [number]` with no cutter or decimal subdivision, it's a shelving control number. Real LC class CD or similar would have `CD[number].[decimal]` or `CD[number] .[cutter]`.

#### Institutional AV/Media Shelving Schemes

Libraries often use multi-word prefixes combining institution/collection name + format + accession number:

| Pattern | Examples | Structure |
|---------|----------|-----------|
| Institution + Video + format + number | `DSI Video CD 18`, `DSI Video DVD 22`, `DSI Video VHS 53` | Collection + media type + format + accession |
| Collection + Video + disc + number | `City College CWE Video - disc 58`, `CohenLib Video disc 110` | Named collection + disc number |
| Fiche + number | `Fiche 414`, `Fiche 685` | Microfiche shelving |
| Dual-format entries | `DSI video VHS 59/DVD 89` | Two formats for same content |

All of these are shelving control numbers (indicator 4).

### CD-ROM and DVD-ROM Call Numbers

"CD ROM" requires context to classify correctly:

| Call Number | Classification | Context Clue |
|-------------|---------------|--------------|
| `CD ROM` | Not a call number | Format descriptor alone, no shelving number |
| `CD-ROM` | Not a call number | Format descriptor alone |
| `CD ROM 003` | Shelving control (4) | Format + accession number = shelving scheme |
| `BRL CD ROM 071` | Shelving control (4) | Collection prefix + format + number |
| `DVD ROM 015` | Shelving control (4) | Format + accession number |

**Rule:** 
- "CD ROM" or "DVD ROM" **alone** = format descriptor, not a call number
- "CD ROM" or "DVD ROM" **followed by a number** = shelving control number for physical media

### By 852 Indicator (Secondary/Verification)

| Indicator | Meaning |
|-----------|---------|
| # (blank) | No information provided |
| 0 | Library of Congress classification |
| 1 | Dewey Decimal classification |
| 2 | National Library of Medicine classification |
| 3 | Superintendent of Documents classification |
| 4 | Shelving control number (uses $j instead of $h) |
| 5 | Title (uses $l for shelving form of title) |
| 6 | Shelved separately |
| 7 | Source specified in subfield $2 |
| 8 | Other scheme |

Source: [MARC 21 Format for Holdings Data: 852](https://www.loc.gov/marc/holdings/hd852.html)

### 852 Subfields for Call Numbers

**Critical: Always parse the 852 MARC field to extract the actual call number.** Display fields like "Permanent Call Number" often concatenate prefixes, which can cause misclassification.

| Subfield | Name | Use |
|----------|------|-----|
| **$$h** | Classification part | The classification portion (e.g., `N620 .F6` for LC) |
| **$$i** | Item part | Cutter, date, volume (e.g., `A85 2015`) — append to $$h |
| **$$j** | Shelving control number | Used *instead of* $$h/$$i for indicator 4 |
| **$$k** | Call number prefix | Shelving prefix (e.g., `FOLIO`, `REF`, `OVERSIZE`) — **ignore for classification** |
| **$$l** | Shelving form of title | Used for indicator 5 (title shelving) |
| **$$m** | Call number suffix | Append after $$i if present |
| **$$2** | Source of classification | Required when indicator = 7 |

**Example:**
```
Permanent Call Number: FOLIO N620 .F6 A85
852 MARC: 852_0 $$a NBC $$b BC001 $$c FOLIO $$h N620 .F6 $$i A85 $$k FOLIO
```

- **Wrong approach**: Analyze "FOLIO N620 .F6 A85" → might see FOLIO as class letters
- **Correct approach**: Extract $$h + $$i = "N620 .F6 A85" → clearly LC class N (Fine Arts)

**Extraction logic:**
1. If $$j exists → use $$j (shelving control number)
2. Otherwise → use $$h + $$i (classification + item)
3. Always ignore $$k (prefix) for classification purposes
4. The prefix may appear at the end of normalized call numbers but doesn't affect scheme identification

## Alma Analytics Normalization

Alma Analytics creates normalized call numbers for sorting and range filtering. Understanding this format is essential for querying and for identifying miscoded records.

### LC Call Numbers (Indicator 0)

**Structure:** `0` + class (lowercase) + normalizing char + class number + space + cutter + space + additional elements

**Normalizing character based on digits in class number:**
| Digits | Character |
|--------|-----------|
| 1 | [space] |
| 2 | ! |
| 3 | " |
| 4 | # |

**Important:** Decimal portions of class numbers are NOT counted when selecting the normalizing character.

**Examples:**
| Original | Normalized |
|----------|------------|
| QA24.D56 T72 1958 | `0qa!24 d56 t72 1958` |
| Folio QA24.D56 T72 1958 | `0qa!24 d56 t72 1958 folio 0` |
| M457.2 .A27 op. 35 | `0m"457.2 a27 op 35` |

**Trailing ` 0` rule:** If the normalized string ends in a letter (date like 1900z or a call number prefix), append ` 0` at the end.

### Other Scheme Call Numbers (Indicator 8)

**Structure:** `8` + alphanumeric content with numbers zero-padded to 12 digits

**Rules:**
- Numbers are padded with leading zeros to 12 places
- Numbers separated by letters, decimals, or dashes are treated as separate numbers
- Spacing is removed after the first space-delimited segment
- Prefix appears at end (lowercase)

**Examples:**
| Original | Normalized |
|----------|------------|
| 36 | `8000000000036` |
| Music Lib Media Audio CD 405.1 | `8000000000405.000000000001music lib media audio cd` |
| BLH A622 | `8blh a000000000622` |
| PPR C646 R4 | `8ppr c000000000646r000000000004` |

### Detecting Miscoded Records

An LC call number miscoded with indicator 8 produces obviously wrong normalization:

| Original | Indicator | Normalized Result |
|----------|-----------|-------------------|
| Z43.A2 H4 1931 | 0 (correct) | `0z!43 a2 h4 1931` |
| Z43.A2 H4 1931 | 8 (wrong) | `8z000000000043.a000000000002h000000000004000000001931` |

**Detection heuristic:** If a normalized call number starting with `8` contains patterns like `000000000` followed by small numbers that would make sense as LC class numbers, it may be a miscoded LC call number.

### Using Normalized Call Numbers for Range Filtering

In Analytics, use "is between" operator on Normalized Call Number field:

**Example:** To find all titles in PC5401-PC5499:
- Filter: Normalized Call Number is between `0pc#5401` and `0pc#5499`

**Building filter values:**
1. Identify the class letters (lowercase them)
2. Count digits in the class number to select normalizing character
3. Assemble: `0` + letters + normalizing char + number

## Workflow Checklist

When analyzing call numbers:

1. [ ] **Check for non-call-numbers first** (notes, instructions, URLs, equipment, format descriptors alone)
2. [ ] **Look for colons** — presence of `:` strongly indicates SuDoc (very rarely a data entry error)
3. [ ] **Examine the starting letters** against valid LC classes (remember: no I, O, W, X, Y in LC)
4. [ ] **Check for NLM patterns** (W, QS-QZ followed by numbers)
5. [ ] **Check for LAC patterns** (FC + number, or PS + number ≥ 8000)
6. [ ] **Check for Dewey patterns** (3 digits at start, with or without decimal)
7. [ ] For LC patterns, accept spacing variations (`BX1758` = `BX 1758` = `BX 1758.2`)
8. [ ] Compare content-based identification with 852 indicator
9. [ ] **Flag mismatches** for data quality review
10. [ ] If working with Analytics data, verify normalization matches expected pattern
11. [ ] For range queries, construct proper normalized filter values

## Quick Reference: Classification Decision Tree

```
START
  │
  ├─ Contains staff notes/instructions/equipment? → NOT A CALL NUMBER
  │
  ├─ Format descriptor alone (DVD, CD, VHS)? → NOT A CALL NUMBER
  │
  ├─ AV/media shelving (DVD/CD/VHS/Video/Fiche + number)? → Shelving control (indicator 4)
  │
  ├─ [Strip shelving prefixes: OVERSIZE, DOCS, FOLIO, REF, etc.]
  │
  ├─ Contains colon (:)? → Likely SUDOC (indicator 3)
  │   └─ If no SuDoc stem pattern, flag for review (may be data entry error)
  │
  ├─ Starts with Y + number? → SUDOC (indicator 3) [Congressional]
  │
  ├─ Starts with W or QS-QZ + number? → NLM (indicator 2)
  │
  ├─ Starts with FC + number? → LAC Canadian history (indicator 7, $2)
  │
  ├─ Starts with PS + number ≥ 8000? → LAC Canadian literature (indicator 7, $2)
  │
  ├─ Starts with 3 digits? → DEWEY (indicator 1)
  │
  ├─ Starts with valid LC letters + number?
  │   (A-H, J-N, P-V, Z — not I, O, W, X, Y)
  │   → LC (indicator 0)
  │
  ├─ Matches known local collection pattern? → Shelving control (indicator 4)
  │
  ├─ Matches other local scheme? → Local scheme (indicator 7 with $2, or 8)
  │
  └─ Otherwise → Other/Review needed (indicator 8)
```

## References

- `references/lcc-classes.md` - Valid Library of Congress classification letters
- `references/alma-analytics-normalization.md` - Full details on Alma's normalization algorithm
- LC documentation: https://www.loc.gov/catdir/cpso/lcco/
- MARC 852: https://www.loc.gov/marc/holdings/hd852.html
- Ex Libris source: "Understanding normalized call numbers in Analytics" by Simon Hunt (2019)
