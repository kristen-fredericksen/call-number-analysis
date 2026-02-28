# How Should We Code These 852 First Indicators?

## We need your help!

We're building a tool that looks at call numbers and suggests what the 852 first indicator *should* be, based on what's actually in the call number field. It works well for the straightforward cases -- LC, Dewey, SuDoc, NLM. But we're stuck on the gray area: items that have *something* in the call number field, but it's not a standard classification.

MARC gives us several options for these, and picking the right one turns out to be surprisingly tricky. We'd love cataloger input on how to handle the examples below.

---

## Quick refresher: the options

| Indicator | Meaning | Subfield | In plain English |
|-----------|---------|----------|------------------|
| 0 | LC | $h | Library of Congress call number |
| 1 | Dewey | $h | Dewey Decimal call number |
| 4 | Shelving control number | **$j** | Not a real classification -- just a number or code used to find the item on the shelf |
| 5 | Title | **$l** | Item is shelved by its title |
| 8 | Other scheme | **$h** | A real classification system, just not one of the big standard ones |

The important thing to notice: **indicators 4, 5, and 8 each use a different subfield.** This isn't just a technicality -- it reflects a real difference in what the data means:

- **$j** (indicator 4) says: "This is an arbitrary label for finding the item. It's not a classification."
- **$l** (indicator 5) says: "This item is shelved by its title."
- **$h** (indicator 8) says: "This is a classification system -- it organizes materials by subject or category -- it's just not LC, Dewey, or another named standard."

---

## The easy cases (we're not asking about these)

These are clear-cut, and the tool already handles them:

| What's in the call number field | Our suggested indicator | Why |
|---|---|---|
| `QA76.73.P98 Z55 2020` | **0** (LC) | Standard LC call number |
| `813.54 B` | **1** (Dewey) | Standard Dewey number |
| `C 55.281/2-2:IM 1/2` | **3** (SuDoc) | Government document number |
| `W1 AM335` | **2** (NLM) | National Library of Medicine number |

---

## The hard cases (this is where we need you!)

### Category A: Format + accession number

These are clearly indicator 4 (shelving control), right? There's no classification logic here -- it's just a format label and a sequential number so you can find the item.

| Example | Our suggestion |
|---|---|
| `DVD 2847` | 4 (shelving control) |
| `Video disc 1234` | 4 (shelving control) |
| `Fiche 500` | 4 (shelving control) |
| `CD 45892` | 4 (shelving control) |

**Question 1: Do you agree these are indicator 4? Are there any examples like these that you'd code differently?**

---

### Category B: Local classification schemes

Some libraries use simplified, homegrown classification systems. These aren't arbitrary shelf locations -- they represent a deliberate scheme for organizing materials by category. That sounds like indicator 8 (other scheme) to us.

| Example | What it means | Our suggestion |
|---|---|---|
| `Fic Adams` | Fiction, shelved by author | 8 (other scheme) |
| `Fic` | Fiction section | 8 (other scheme) |
| `M` (in a music library) | Music section | 8 (other scheme) |
| `Per` | Periodicals section | 8 (other scheme) |
| `Bio` | Biography section | 8 (other scheme) |
| `Easy` | Easy/picture books | 8 (other scheme) |
| `Juv Fic` | Juvenile fiction | 8 (other scheme) |
| `YA` | Young adult section | 8 (other scheme) |

The reasoning: even though these are simple, they're still *classifying* materials into subject or format categories. A cataloger (or someone) chose "Fic" because the item is fiction. That's a classification decision, which makes it indicator 8 ($h), not indicator 4 ($j).

**Question 2: Do you agree these are indicator 8? Or would you code some of them as indicator 4 (shelving control)?**

---

### Category C: "Periodical" as a call number

This one is especially confusing. Some records have the word "Periodical" (or "Periodicals", or "Serial") in the call number field. What indicator should that get?

We see three possibilities:

1. **Indicator 8** (other scheme in $h) -- "Periodical" is being used as a simplified classification, similar to "Fic" or "Bio" above.

2. **Indicator 5** (title in $l) -- The item is shelved by title, and "Periodical" is describing the shelving arrangement rather than classifying the item.

3. **Neither** -- "Periodical" isn't really a call number at all; it's a placeholder or note.

Right now, we're leaning toward **indicator 8**, since it seems parallel to "Fic" -- it's a one-word scheme that tells you where to look. But we're not confident.

**Question 3: When a record has "Periodical" in the call number field, what indicator would you assign? Does your answer change if the call number is just the word "Periodical" vs. something like `Per QA` or `Per Science`?**

---

### Category D: "Thesis" and "Dissertation"

Some records have "Thesis" or "Dissertation" in the call number field, sometimes followed by additional information (a year, a department, an author name).

| Example | What we're unsure about |
|---|---|
| `Thesis` | Is this a classification (indicator 8)? Or a shelving-by-title arrangement (indicator 5)? |
| `Thesis 2019` | Same question -- "Thesis" + year |
| `Dissertation LIT 2020` | "Dissertation" + department + year |

Our concern: indicator 5 means the item is *shelved by its title*, but "Thesis" isn't the title of the work -- it's a description of the format. That makes indicator 5 feel wrong. But is "Thesis" really a *classification scheme*? It doesn't organize by subject.

**Question 4: How would you code "Thesis" or "Dissertation" in the call number field? Indicator 4 (shelving control -- it's just a way to find the item), indicator 5 (title), or indicator 8 (other scheme)?**

---

### Category E: Things that aren't call numbers at all

Some records have text in the call number field that clearly isn't any kind of call number or shelving instruction:

| Example | Our suggestion |
|---|---|
| `Digital Projector` | Not a call number (equipment) |
| `Math Class Laptop Charger` | Not a call number (equipment) |
| `SHELVED UNDER TITLE` | Not a call number (staff note) |
| `IN PROCESS` | Not a call number (status note) |
| `Ask at desk` | Not a call number (instruction) |

**Question 5: Do you agree these aren't call numbers? Would you still assign an indicator (maybe indicator 4 as a catch-all), or leave the indicator blank?**

---

## Summary of what we're asking

| # | Question | Examples |
|---|----------|----------|
| 1 | Is `DVD 2847` indicator 4? | Format + number patterns |
| 2 | Is `Fic Adams` indicator 8? | Local classification schemes |
| 3 | What is `Periodical`? | Indicator 5, 8, or not a call number? |
| 4 | What is `Thesis`? | Indicator 4, 5, or 8? |
| 5 | Is `Digital Projector` not a call number? | Equipment, notes, status messages |

Any input is helpful -- even if it's "I'm not sure either" or "it depends on the library." We'd rather know where the genuine ambiguity is than guess.

Thank you!
