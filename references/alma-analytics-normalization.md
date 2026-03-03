# Alma Analytics Call Number Normalization

Alma Analytics creates normalized call numbers for sorting and range filtering. Understanding this format is essential for querying Analytics reports and for identifying miscoded records.

## LC Call Numbers (Indicator 0)

**Structure:** `0` + class (lowercase) + normalizing char + class number + space + cutter + space + additional elements

### Normalizing Character

The normalizing character is selected based on the number of digits in the class number. Decimal portions are NOT counted.

| Digits in class number | Normalizing character |
|------------------------|----------------------|
| 1 | (space) |
| 2 | ! |
| 3 | " |
| 4 | # |

### Examples

| Original | Normalized | Explanation |
|----------|------------|-------------|
| QA24.D56 T72 1958 | `0qa!24 d56 t72 1958` | QA = class, 24 = 2 digits so `!`, decimal .D56 = cutter |
| Folio QA24.D56 T72 1958 | `0qa!24 d56 t72 1958 folio 0` | Prefix appears at end |
| M457.2 .A27 op. 35 | `0m"457.2 a27 op 35` | M = class, 457 = 3 digits so `"` |
| BX1758.2 .M53 | `0bx#1758.2 m53` | BX = class, 1758 = 4 digits so `#` |
| E185.5 .B58 | `0e"185.5 b58` | E = class, 185 = 3 digits so `"` |

### Trailing ` 0` Rule

If the normalized string ends in a letter (such as a date like 1900z or a call number prefix), append ` 0` at the end.

## Other Scheme Call Numbers (Indicator 8)

**Structure:** `8` + alphanumeric content with numbers zero-padded to 12 digits

### Rules

- Numbers are padded with leading zeros to 12 places
- Numbers separated by letters, decimals, or dashes are treated as separate numbers
- Spacing is removed after the first space-delimited segment
- Prefix appears at end (lowercase)

### Examples

| Original | Normalized |
|----------|------------|
| 36 | `8000000000036` |
| Music Lib Media Audio CD 405.1 | `8000000000405.000000000001music lib media audio cd` |
| BLH A622 | `8blh a000000000622` |
| PPR C646 R4 | `8ppr c000000000646r000000000004` |

## Dewey Call Numbers (Indicator 1)

**Structure:** `1` + class number + space + cutter

Follows similar principles to LC normalization but prefixed with `1`.

## SuDoc Call Numbers (Indicator 3)

**Structure:** `3` + agency stem + normalized remainder

SuDoc normalization preserves the agency hierarchy structure.

## Detecting Miscoded Records via Normalization

An LC call number miscoded with indicator 8 produces obviously wrong normalization because of the 12-digit zero-padding:

| Original | Indicator | Normalized Result |
|----------|-----------|-------------------|
| Z43.A2 H4 1931 | 0 (correct) | `0z!43 a2 h4 1931` |
| Z43.A2 H4 1931 | 8 (wrong) | `8z000000000043.a000000000002h000000000004000000001931` |

**Detection heuristic:** If a normalized call number starting with `8` contains patterns like `000000000` followed by small numbers that would make sense as LC class numbers, it may be a miscoded LC call number.

## Using Normalized Call Numbers for Range Filtering

In Analytics, use the "is between" operator on the Normalized Call Number field.

### Building Filter Values

1. Identify the class letters (lowercase them)
2. Count digits in the class number to select the normalizing character
3. Assemble: `0` + letters + normalizing char + number

### Example

To find all titles in PC5401-PC5499:
- Filter: Normalized Call Number **is between** `0pc#5401` and `0pc#5499`

To find all titles in QA1-QA99:
- Filter: Normalized Call Number **is between** `0qa 1` and `0qa!99`

(Note the different normalizing characters: QA1 has 1 digit = space, QA99 has 2 digits = `!`)

## Source

Based on "Understanding normalized call numbers in Analytics" by Simon Hunt (2019), Ex Libris.
