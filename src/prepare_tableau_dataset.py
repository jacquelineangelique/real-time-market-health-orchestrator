"""
PR 08: build tableau data source

Purpose:
Validate and finalize the processed analytical dataset used by Tableau.

This workflow:
- validates Tableau-ready field formatting
- verifies analytical schema consistency
- standardizes data types
- cleans dataset formatting
- exports finalized Tableau-ready CSV
"""

import logging
from pathlib import Path
from datetime import datetime

import pandas as pd


# =====================================================
# Directory Setup
# =====================================================

PROCESSED_DATA_DIR = Path("data/processed")
TABLEAU_DATA_DIR = Path("data/tableau")
LOG_DIR = Path("logs")

TABLEAU_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Logging Setup
# =====================================================

logging.basicConfig(
    filename=LOG_DIR / "tableau_data_source.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# =====================================================
# Tableau Analytical Schema Definition
# =====================================================

TABLEAU_SCHEMA = {
    "date": "datetime64[ns]",
    "asset_code": "object",
    "asset_type": "object",
    "base_currency": "object",
    "quote_currency": "object",
    "usd_value": "float64",
    "base_100_index": "float64",
    "daily_pct_change": "float64",
    "source_api": "object",
    "transformed_at_utc": "object"
}


# =====================================================
# Tableau Field Mapping Documentation
# =====================================================

TABLEAU_FIELD_MAPPING = {
    "date": "Time-series date field used on Tableau Columns shelf.",
    "asset_code": "Currency or asset identifier such as BTC, EUR, GBP.",
    "asset_type": "Distinguishes fiat currencies from crypto assets.",
    "base_currency": "Source currency used for exchange calculation.",
    "quote_currency": "Target currency quoted against the base currency.",
    "usd_value": "Raw exchange rate or BTC market price.",
    "base_100_index": "Normalized comparison index for volatility visualization.",
    "daily_pct_change": "Daily percent variance used for heatmaps and threshold analysis.",
    "source_api": "Identifies originating API source.",
    "transformed_at_utc": "UTC timestamp showing transformation execution time."
}


# =====================================================
# Load Processed Dataset
# =====================================================

def load_processed_dataset():
    """
    Loads the processed analytical dataset created in PR 04.
    """

    input_file = (
        PROCESSED_DATA_DIR /
        "market_health_timeseries.csv"
    )

    if not input_file.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {input_file}"
        )

    logging.info(f"Loading processed dataset: {input_file}")

    df = pd.read_csv(input_file)

    return df


# =====================================================
# Analytical Schema Verification
# =====================================================

def validate_schema(df):
    """
    Validates required Tableau-ready columns exist.
    """

    required_columns = list(TABLEAU_SCHEMA.keys())

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required Tableau columns: {missing_columns}"
        )

    logging.info("Analytical schema verification passed.")


# =====================================================
# Data Type Standardization
# =====================================================

def standardize_data_types(df):
    """
    Ensures consistent Tableau-compatible field types.
    """

    logging.info("Standardizing Tableau data types.")

    df["date"] = pd.to_datetime(df["date"])

    numeric_columns = [
        "usd_value",
        "base_100_index",
        "daily_pct_change"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    string_columns = [
        "asset_code",
        "asset_type",
        "base_currency",
        "quote_currency",
        "source_api",
        "transformed_at_utc"
    ]

    for column in string_columns:
        df[column] = df[column].astype(str)

    return df


# =====================================================
# Dataset Formatting Cleanup
# =====================================================

def clean_dataset(df):
    """
    Applies Tableau-focused formatting cleanup.

    Includes:
    - duplicate removal
    - null handling
    - sorting
    - precision formatting
    """

    logging.info("Applying dataset formatting cleanup.")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove records missing critical analytical fields
    df = df.dropna(subset=[
        "date",
        "asset_code",
        "usd_value"
    ])

    # Sort for consistent Tableau ingestion
    df = df.sort_values([
        "asset_code",
        "date"
    ])

    # Round analytical metrics for readability
    df["usd_value"] = df["usd_value"].round(6)
    df["base_100_index"] = df["base_100_index"].round(4)
    df["daily_pct_change"] = df["daily_pct_change"].round(4)

    return df


# =====================================================
# Processed Export Validation
# =====================================================

def validate_export(df):
    """
    Performs lightweight export validation checks.
    """

    if df.empty:
        raise ValueError("Final Tableau dataset is empty.")

    duplicate_count = df.duplicated(
        subset=["date", "asset_code"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Duplicate Tableau records detected: {duplicate_count}"
        )

    asset_count = df["asset_code"].nunique()

    if asset_count < 3:
        raise ValueError(
            "Expected at least 3 analytical assets."
        )

    logging.info("Processed CSV export validation passed.")


# =====================================================
# Tableau Export
# =====================================================

def export_tableau_dataset(df):
    """
    Exports finalized Tableau-ready dataset.
    """

    output_file = (
        TABLEAU_DATA_DIR /
        "tableau_market_health_dataset.csv"
    )

    df.to_csv(output_file, index=False)

    logging.info(
        f"Tableau-ready dataset exported: {output_file}"
    )

    return output_file


# =====================================================
# Field Mapping Documentation Output
# =====================================================

def print_tableau_mapping():
    """
    Prints Tableau field mapping documentation.
    """

    print("\nTableau Field Mapping")
    print("======================")

    for field, description in TABLEAU_FIELD_MAPPING.items():
        print(f"\n{field}")
        print(f"  {description}")


# =====================================================
# Main Workflow
# =====================================================

def main():
    """
    Main Tableau data source preparation workflow.

    Steps:
    1. Load processed analytical dataset
    2. Validate schema
    3. Standardize data types
    4. Clean dataset formatting
    5. Validate export readiness
    6. Export finalized Tableau dataset
    """

    logging.info("Tableau data source preparation started.")

    df = load_processed_dataset()

    validate_schema(df)

    df = standardize_data_types(df)

    df = clean_dataset(df)

    validate_export(df)

    output_file = export_tableau_dataset(df)

    logging.info("Tableau data source preparation completed.")

    print("\nTableau-ready dataset created successfully.")
    print(f"Output file: {output_file}")

    print_tableau_mapping()

    print("\nDataset Preview:")
    print(df.head(20))

    return output_file


# =====================================================
# Script Entry Point
# =====================================================

if __name__ == "__main__":
    main()
