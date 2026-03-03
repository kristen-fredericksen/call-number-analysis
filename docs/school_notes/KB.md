# Kingsborough Community College (KB)

## Overview

- Institution code: 01CUNY_KB
- Analytics path: `/shared/Kingsborough Community College 01CUNY_KB/Cataloging/852 Field Analysis - All Indicators`
- Cataloging quality: Generally reliable. Errors are likely typos, not systematic problems.

## Local Schemes

### Reserve textbook labels

Items in reserve locations (SMRES, RES4H, RES7D) use abbreviated title codes instead of standard call numbers.

| Pattern | Examples | Indicator |
|---------|----------|-----------|
| Abbreviation + year + edition | `Am 2014 4th Ed`, `CJ 2017 3rd Ed` | 8 |
| Abbreviation + number + year | `RM 30 2016`, `RM 31 2017` | 8 |

These look like LC classes (AM, AS, CJ, RM are all valid) but the structure is wrong — no cutter, and the numbers are edition/volume identifiers, not class numbers.

## Known Subfield Issues

### DVD location: dual schemes in one 852 field

~397 records in the DVD location have both a Dewey call number in $h and a shelving control number in $j:

```
852_4 $$c DVD $$j DVD 521 $$h 289 A517
852_4 $$c DVD $$j DVD 639 $$h 070.1/95
852_4 $$c DVD $$j DVD 546 $$h 174.2 $$i R74
```

The indicator is set to 4 (shelving control), which matches the $j content, but $h/$i shouldn't be populated with indicator 4. The Dewey number and the DVD shelving number are two different schemes in one field. Flagged for review — KB catalogers should decide what to keep.

### DVD without a number

Some DVD records have just "DVD" in $j with no accession number:

```
852#_ $$c DVD $$j DVD
```

These are format descriptors, not call numbers. Likely records where the DVD number was never assigned.

## Locations to Watch

| Location | Code | Notes |
|----------|------|-------|
| DVD | DVD | Dual-scheme $h/$j issue; some records missing DVD number |
| Semester Reserves | SMRES | Local abbreviated title labels |
| 4-Hour Reserves | RES4H | Local abbreviated title labels |
| 7-Day Reserves | RES7D | Local abbreviated title labels |
