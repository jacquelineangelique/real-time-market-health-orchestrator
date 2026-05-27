"""
PR 04: add tableau-ready transformation and normalization workflow

Purpose:
Transform raw API responses from the extraction layer into a clean,
Tableau-ready analytical time-series dataset.

This script:
- reads raw JSON files
- flattens Frankfurter FX data
- flattens CoinGecko BTC data
- converts dates to ISO-8601 format
- reduces BTC to one daily value
- calculates Base 100 index
- calculates daily percent variance
- exports processed CSV
"""

import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd


# =====================================================
# Directory Setup
# =====================================================

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
LOG_DIR = Path("logs")

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Logging Setup
# =====================================================

logging.basicConfig(
    filename=LOG_DIR / "transformation.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# =====================================================
# File Helpers
# =====================================================

def get_latest_raw_file(source_prefix):
    """
    Finds the most recent raw JSON file for a given source.

    Example:
    source_prefix = "frankfurter_rates"
    matches files like:
    data/raw/frankfurter_rates_20260526T180000Z.json
    """

    matching_files = list(RAW_DATA_DIR.glob(f"{source_prefix}_*.json"))

    if not matching_files:
        raise FileNotFoundError(
            f"No raw files found for source prefix: {source_prefix}"
        )

    latest_file = max(matching_files, key=lambda file: file.stat().st_mtime)

    logging.info(f"Latest raw file selected: {latest_file}")

    return latest_file


def load_json(file_path):
    """
    Loads a raw JSON file from disk.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# =====================================================
# Frankfurter Transformation
# =====================================================

def transform_frankfurter_rates(raw_data):
    """
    Flattens Frankfurter raw JSON into the standard analytical schema.

    Expected raw structure:
    [
        {
            "date": "2026-05-26",
            "base": "USD",
            "quote": "EUR",
            "rate": 0.85831
        }
    ]

    Output grain:
    one row per date per fiat currency.
    """

    rows = []

    for item in raw_data:
        rows.append({
            "date": pd.to_datetime(item["date"]),
            "asset_code": item["quote"],
            "asset_type": "fiat",
            "base_currency": item["base"],
            "quote_currency": item["quote"],
            "usd_value": float(item["rate"]),
            "source_api": "Frankfurter"
        })

    df = pd.DataFrame(rows)

    logging.info(f"Frankfurter rows transformed: {len(df)}")

    return df


# =====================================================
# CoinGecko Transformation
# =====================================================

def transform_coingecko_btc(raw_data):
    """
    Flattens CoinGecko BTC raw JSON into the standard analytical schema.

    Expected raw structure:
    {
        "prices": [
            [timestamp_ms, price],
            [timestamp_ms, price]
        ]
    }

    CoinGecko can return multiple intraday BTC records.
    For Tableau daily volatility analysis, this function keeps the
    last available BTC price per calendar day.
    """

    rows = []

    for price_point in raw_data.get("prices", []):
        timestamp_ms = price_point[0]
        btc_price = price_point[1]

        rows.append({
            "datetime": pd.to_datetime(timestamp_ms, unit="ms"),
            "asset_code": "BTC",
            "asset_type": "crypto",
            "base_currency": "BTC",
            "quote_currency": "USD",
            "usd_value": float(btc_price),
            "source_api": "CoinGecko"
        })

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("CoinGecko BTC raw data returned no price records.")

    # Create one daily date from the intraday timestamp.
    df["date"] = df["datetime"].dt.normalize()

    # Keep the last available BTC price for each day.
    df = (
        df.sort_values("datetime")
        .groupby("date", as_index=False)
        .tail(1)
    )

    df = df[[
        "date",
        "asset_code",
        "asset_type",
        "base_currency",
        "quote_currency",
        "usd_value",
        "source_api"
    ]]

    logging.info(f"CoinGecko BTC daily rows transformed: {len(df)}")

    return df


# =====================================================
# Analytical Calculations
# =====================================================

def add_volatility_metrics(df):
    """
    Adds analytical fields required for Tableau.

    base_100_index:
    Normalizes each asset to a starting value of 100.

    daily_pct_change:
    Measures day-over-day percent variance for volatility analysis.
    """

    df = df.sort_values(["asset_code", "date"]).copy()

    first_value = (
        df.groupby("asset_code")["usd_value"]
        .transform("first")
    )

    df["base_100_index"] = (
        df["usd_value"] / first_value
    ) * 100

    df["daily_pct_change"] = (
        df.groupby("asset_code")["usd_value"]
        .pct_change()
    ) * 100

    return df


# =====================================================
# Validation Checks
# =====================================================

def validate_transformed_data(df):
    """
    Performs lightweight validation checks before export.

    These checks help prevent invalid data from reaching Tableau.
    """

    required_columns = [
        "date",
        "asset_code",
        "asset_type",
        "base_currency",
        "quote_currency",
        "usd_value",
        "base_100_index",
        "daily_pct_change",
        "source_api"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df.empty:
        raise ValueError("Transformed dataset is empty.")

    if df["usd_value"].isna().any():
        raise ValueError("usd_value contains null values.")

    duplicate_count = df.duplicated(
        subset=["date", "asset_code"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Duplicate date + asset_code records found: {duplicate_count}"
        )

    logging.info("Transformation validation checks passed.")


# =====================================================
# Final Transformation Workflow
# =====================================================

def run_transformation():
    """
    Main transformation workflow.

    Steps:
    1. Locate latest raw Frankfurter JSON
    2. Locate latest raw CoinGecko JSON
    3. Flatten both raw responses
    4. Standardize schema
    5. Add Base 100 and volatility metrics
    6. Validate output
    7. Export processed CSV
    """

    logging.info("Transformation workflow started.")

    frankfurter_file = get_latest_raw_file("frankfurter_rates")
    coingecko_file = get_latest_raw_file("coingecko_btc")

    frankfurter_raw = load_json(frankfurter_file)
    coingecko_raw = load_json(coingecko_file)

    frankfurter_df = transform_frankfurter_rates(frankfurter_raw)
    coingecko_df = transform_coingecko_btc(coingecko_raw)

    final_df = pd.concat(
        [frankfurter_df, coingecko_df],
        ignore_index=True
    )

    final_df = add_volatility_metrics(final_df)

    # ISO-8601 timestamp conversion for Tableau compatibility.
    final_df["date"] = (
        pd.to_datetime(final_df["date"])
        .dt.strftime("%Y-%m-%dT%H:%M:%S")
    )

    final_df["transformed_at_utc"] = datetime.utcnow().strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    final_df = final_df[[
        "date",
        "asset_code",
        "asset_type",
        "base_currency",
        "quote_currency",
        "usd_value",
        "base_100_index",
        "daily_pct_change",
        "source_api",
        "transformed_at_utc"
    ]]

    validate_transformed_data(final_df)

    output_file = PROCESSED_DATA_DIR / "market_health_timeseries.csv"

    final_df.to_csv(output_file, index=False)

    logging.info(f"Processed CSV exported: {output_file}")
    logging.info("Transformation workflow completed successfully.")

    print("Transformation completed successfully.")
    print(f"Processed file created: {output_file}")
    print(final_df.head(20))

    return output_file


if __name__ == "__main__":
    run_transformation()
