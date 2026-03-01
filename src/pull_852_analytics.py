#!/usr/bin/env python3
"""
Pull 852 field data from Alma Analytics via the REST API.

Retrieves the "852 Field Analysis - All Indicators" report for one or more
CUNY schools and saves the results as an Excel file compatible with
analyze_852_indicators.py.

Usage:
    python pull_852_analytics.py KB              # Pull Kingsborough only
    python pull_852_analytics.py KB BM           # Pull Kingsborough and BMCC
    python pull_852_analytics.py --all           # Pull all schools with keys

Output: data/{school_code}_852_data.xlsx (one file per school)

Requires: api_keys.env in the project root with IZ API keys.
"""

import os
import sys
import time
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font

# Project root (one level up from src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Analytics report paths per school. Add new schools here as reports are created.
REPORT_PATHS = {
    'BM': '/shared/Manhattan Community College 01CUNY_BM/Reports/852 Field Analysis - All Indicators',
    'KB': '/shared/Kingsborough Community College 01CUNY_KB/Cataloging/852 Field Analysis - All Indicators',
}

# Map school codes to their API key variable names in api_keys.env
SCHOOL_KEY_MAP = {
    'BB': 'BB_IZ_API_KEY',
    'BM': 'BM_IZ_API_KEY',
    'BX': 'BX_IZ_API_KEY',
    'BC': 'BC_IZ_API_KEY',
    'SI': 'SI_IZ_API_KEY',
    'GJ': 'GJ_IZ_API_KEY',
    'AL': 'AL_IZ_API_KEY',
    'GC': 'GC_IZ_API_KEY',
    'CL': 'CL_IZ_API_KEY',
    'NC': 'NC_IZ_API_KEY',
    'HO': 'HO_IZ_API_KEY',
    'HC': 'HC_IZ_API_KEY',
    'JJ': 'JJ_IZ_API_KEY',
    'KB': 'KB_IZ_API_KEY',
    'LG': 'LG_IZ_API_KEY',
    'LE': 'LE_IZ_API_KEY',
    'ME': 'ME_IZ_API_KEY',
    'NY': 'NY_IZ_API_KEY',
    'QC': 'QC_IZ_API_KEY',
    'QB': 'QB_IZ_API_KEY',
    'CC': 'CC_IZ_API_KEY',
    'YC': 'YC_IZ_API_KEY',
}

# Expected columns from the Analytics report (in the order Analytics returns
# them, which is alphabetical by full path). The dummy "Column 0" is skipped.
# These get mapped to the column names the analysis script expects.
ANALYTICS_TO_SCRIPT_COLUMNS = {
    'MMS Id': 'MMS Id',
    '852 MARC': '852 MARC',
    'Holdings ID': 'Holdings ID',
    'Normalized Call Number': 'Normalized Call Number',
    'Permanent Call Number Type': 'Permanent Call Number Type',
    'Permanent Call Number': 'Permanent Call Number',
    'Suppressed from Discovery': 'Suppressed',
    'Institution Name': 'Institution Name',
}


def load_env(env_path):
    """Load key=value pairs from an env file."""
    config = {}
    if not env_path.exists():
        return config
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def get_api_key(config, school_code):
    """Get the API key for a school from the loaded config."""
    key_name = SCHOOL_KEY_MAP.get(school_code)
    if not key_name:
        return None
    key = config.get(key_name, '')
    return key if key else None


def fetch_analytics_report(base_url, api_key, report_path, limit=1000):
    """
    Fetch an Alma Analytics report with pagination.

    Returns a list of dicts, one per row, with column names as keys.
    """
    url = f"{base_url}/almaws/v1/analytics/reports"
    all_rows = []
    column_names = None
    token = None
    page = 0

    while True:
        page += 1
        params = {
            'apikey': api_key,
            'limit': limit,
            'col_names': 'true',
        }

        if token:
            params['token'] = token
        else:
            params['path'] = report_path

        print(f"  Fetching page {page}...", end=' ', flush=True)
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"ERROR (HTTP {response.status_code})")
            print(f"  Response: {response.text[:500]}")
            sys.exit(1)

        root = ET.fromstring(response.text)

        # Check if finished
        is_finished_el = root.find('.//IsFinished')
        is_finished = is_finished_el is not None and is_finished_el.text == 'true'

        # Find the result XML — it may be nested inside a namespace
        result_xml = root.find('.//ResultXml')
        if result_xml is None:
            print("ERROR: No ResultXml in response")
            print(f"  Response: {response.text[:500]}")
            sys.exit(1)

        # The actual data is inside a rowset element (may have namespace)
        # Find all elements regardless of namespace
        rowset = None
        for elem in result_xml.iter():
            if 'rowset' in elem.tag.lower():
                rowset = elem
                break

        if rowset is None:
            # Try without namespace
            rowset = result_xml

        # Extract column names from the first page
        if column_names is None:
            # Column names come from the schema or the first Row's structure
            # In Analytics API, column headers are in a separate element
            # or we extract them from the xsd:schema
            column_names = _extract_column_names(root)
            if column_names:
                print(f"({len(column_names)} columns)", end=' ')

        # Extract rows
        rows_found = 0
        for row_elem in rowset.iter():
            if 'Row' in row_elem.tag and row_elem.tag != rowset.tag:
                # Skip the Row tag itself, get its children (Column elements)
                values = []
                for col_elem in row_elem:
                    values.append(col_elem.text if col_elem.text else '')
                if values:
                    all_rows.append(values)
                    rows_found += 1

        print(f"{rows_found} rows")

        if is_finished:
            break

        # Get resumption token
        token_el = root.find('.//ResumptionToken')
        if token_el is None or not token_el.text:
            print("  Warning: No resumption token but IsFinished is false. Stopping.")
            break
        token = token_el.text

        # Brief pause to be polite to the API
        time.sleep(0.5)

    return column_names, all_rows


def _extract_column_names(root):
    """
    Extract column names from the Analytics API response.

    The response contains an XSD schema with column definitions.
    Column names appear as 'name' attributes on elements, or as
    'saw-sql:columnHeading' attributes.
    """
    names = []

    # Strategy 1: Look for columnHeading attributes in the schema
    for elem in root.iter():
        heading = elem.attrib.get('{urn:saw-sql}columnHeading')
        if not heading:
            # Try without namespace prefix
            for attr_name, attr_val in elem.attrib.items():
                if 'columnHeading' in attr_name:
                    heading = attr_val
                    break
        if heading:
            names.append(heading)

    if names:
        return names

    # Strategy 2: Look for Column/Name elements
    for elem in root.iter():
        if elem.tag.endswith('Column') or elem.tag == 'Column':
            name_el = elem.find('Name')
            if name_el is not None and name_el.text:
                names.append(name_el.text)

    return names if names else None


def rows_to_dataframe(column_names, rows):
    """
    Convert raw Analytics rows to a DataFrame with the columns the
    analysis script expects.
    """
    if not column_names:
        # Fall back to positional mapping based on the known report structure.
        # Analytics returns columns alphabetically by full path, plus a
        # leading dummy "Column 0". The report has 8 real columns:
        #   s_0 (dummy), s_1 MMS Id, s_2 852 MARC, s_3 Holdings ID,
        #   s_4 Normalized Call Number, s_5 Permanent Call Number Type,
        #   s_6 Permanent Call Number, s_7 Suppressed, s_8 Institution Name
        # But the API may reorder alphabetically. Use positional fallback.
        print("  Warning: Could not extract column names. Using positional mapping.")
        expected = [
            'Dummy', 'MMS Id', '852 MARC', 'Holdings ID',
            'Normalized Call Number', 'Permanent Call Number Type',
            'Permanent Call Number', 'Suppressed', 'Institution Name',
            'Institution Code'
        ]
        # Trim to match actual column count
        col_count = len(rows[0]) if rows else 0
        column_names = expected[:col_count]

    df = pd.DataFrame(rows, columns=column_names[:len(rows[0])] if rows else column_names)

    # Drop dummy columns (Column 0, numeric-only columns, DESCRIPTOR_IDOF)
    for col in list(df.columns):
        if col in ('Column 0', '0', 'Dummy') or 'DESCRIPTOR' in str(col).upper():
            df = df.drop(columns=[col])

    # Rename columns to match what the analysis script expects
    rename_map = {}
    for analytics_name, script_name in ANALYTICS_TO_SCRIPT_COLUMNS.items():
        # Find the column (may be exact match or contained in a longer name)
        for col in df.columns:
            if analytics_name in str(col):
                rename_map[col] = script_name
                break
    df = df.rename(columns=rename_map)

    return df


def save_to_excel(df, output_path):
    """Save DataFrame to Excel with 12pt Arial formatting."""
    data_font = Font(name='Arial', size=12)
    header_font = Font(name='Arial', size=12, bold=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Analytics Data"

    # Write headers
    for col_idx, col_name in enumerate(df.columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font

    # Write data
    for row_idx, row in df.iterrows():
        for col_idx, value in enumerate(row, 1):
            cell = ws.cell(row=row_idx + 2, column=col_idx, value=value)
            cell.font = data_font

    # Auto-width columns
    for col_idx, col_name in enumerate(df.columns, 1):
        col_letter = chr(64 + col_idx) if col_idx <= 26 else 'A'
        ws.column_dimensions[col_letter].width = max(15, len(str(col_name)) + 5)

    wb.save(output_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pull_852_analytics.py <school_code> [school_code ...]")
        print("       python pull_852_analytics.py --all")
        print()
        print("School codes: BB, BM, BX, BC, SI, GJ, AL, GC, CL, NC, HO,")
        print("              HC, JJ, KB, LG, LE, ME, NY, QC, QB, CC, YC")
        sys.exit(1)

    # Load API keys
    env_path = PROJECT_ROOT / 'api_keys.env'
    config = load_env(env_path)
    if not config:
        print(f"Error: Could not load {env_path}")
        print("Make sure api_keys.env exists in the project root.")
        sys.exit(1)

    base_url = config.get('ALMA_API_BASE_URL', 'https://api-na.hosted.exlibrisgroup.com')

    # Determine which schools to pull
    if '--all' in sys.argv:
        schools = [code for code in SCHOOL_KEY_MAP if get_api_key(config, code)]
    else:
        schools = [code.upper() for code in sys.argv[1:]]

    # Validate
    for code in schools:
        if code not in SCHOOL_KEY_MAP:
            print(f"Error: Unknown school code '{code}'")
            sys.exit(1)
        if not get_api_key(config, code):
            print(f"Warning: No API key for {code}. Skipping.")
            schools = [s for s in schools if s != code]
        if code not in REPORT_PATHS:
            print(f"Error: No Analytics report path configured for {code}.")
            print(f"Add the path to REPORT_PATHS in this script.")
            sys.exit(1)

    if not schools:
        print("No schools to process.")
        sys.exit(1)

    # Process each school
    data_dir = PROJECT_ROOT / 'data'
    data_dir.mkdir(exist_ok=True)

    for code in schools:
        api_key = get_api_key(config, code)
        report_path = REPORT_PATHS[code]

        print(f"\n{'='*60}")
        print(f"Pulling data for {code}")
        print(f"Report: {report_path}")
        print(f"{'='*60}")

        column_names, rows = fetch_analytics_report(base_url, api_key, report_path)

        if not rows:
            print(f"  No data returned for {code}.")
            continue

        print(f"\n  Total rows: {len(rows)}")

        # Convert to DataFrame
        df = rows_to_dataframe(column_names, rows)
        print(f"  Columns: {list(df.columns)}")
        print(f"  Records after cleanup: {len(df)}")

        # Save
        output_path = data_dir / f"{code}_852_data.xlsx"
        save_to_excel(df, output_path)
        print(f"  Saved to: {output_path}")

    print("\nDone!")


if __name__ == '__main__':
    main()
