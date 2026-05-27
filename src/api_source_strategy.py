"""
PR 02: API Source Strategy

Purpose:
Document the planned API sources, request patterns, assumptions,
and target analytical schema for the Real-Time Market Health Orchestrator.

This file defines the API strategy and expected output structures.
"""

from datetime import datetime, timedelta


# =====================================================
# Date Window Strategy
# =====================================================

LOOKBACK_DAYS = 30

end_date = datetime.today()
start_date = end_date - timedelta(days=LOOKBACK_DAYS)

FROM_DATE = start_date.strftime("%Y-%m-%d")
TO_DATE = end_date.strftime("%Y-%m-%d")

FROM_UNIX = int(start_date.timestamp())
TO_UNIX = int(end_date.timestamp())


# =====================================================
# API Source Strategy
# =====================================================

API_SOURCES = {
    "frankfurter": {
        "source_name": "Frankfurter API",
        "purpose": "Retrieve fiat exchange rates for EUR and GBP using USD as the base currency.",
        "base_url": "https://api.frankfurter.dev/v2/rates",
        "requires_api_key": False,
        "base_currency": "USD",
        "target_currencies": ["EUR", "GBP"],
        "expected_grain": "One row per date per fiat quote currency",
        "request_parameters": {
            "from": FROM_DATE,
            "to": TO_DATE,
            "base": "USD",
            "quotes": "EUR,GBP",
        },
        "sample_request": (
            "https://api.frankfurter.dev/v2/rates"
            f"?from={FROM_DATE}&to={TO_DATE}&base=USD&quotes=EUR,GBP"
        ),
    },
    "coingecko": {
        "source_name": "CoinGecko API",
        "purpose": "Retrieve BTC historical price data quoted in USD.",
        "base_url": "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range",
        "requires_api_key": True,
        "asset": "BTC",
        "quote_currency": "USD",
        "expected_grain": "Multiple intraday BTC records that will later be reduced to one row per day",
        "request_parameters": {
            "vs_currency": "usd",
            "from": FROM_UNIX,
            "to": TO_UNIX,
            "x_cg_demo_api_key": "loaded from .env",
        },
        "sample_request": (
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
            f"?vs_currency=usd&from={FROM_UNIX}&to={TO_UNIX}&x_cg_demo_api_key=<COINGECKO_API_KEY>"
        ),
    },
}


# =====================================================
# Target Time-Series Analytical Schema
# =====================================================

TARGET_SCHEMA = [
    {
        "column_name": "date",
        "data_type": "datetime",
        "description": "ISO-8601 date used for time-series analysis.",
    },
    {
        "column_name": "asset_code",
        "data_type": "string",
        "description": "Currency or asset code such as EUR, GBP, or BTC.",
    },
    {
        "column_name": "asset_type",
        "data_type": "string",
        "description": "Classifies the asset as fiat or crypto.",
    },
    {
        "column_name": "usd_value",
        "data_type": "decimal",
        "description": "Exchange rate or asset value relative to USD.",
    },
    {
        "column_name": "base_100_index",
        "data_type": "decimal",
        "description": "Normalized index used to compare BTC volatility against fiat currencies.",
    },
    {
        "column_name": "daily_pct_change",
        "data_type": "decimal",
        "description": "Day-over-day percent change used for volatility analysis.",
    },
    {
        "column_name": "source_api",
        "data_type": "string",
        "description": "Identifies whether the record came from Frankfurter or CoinGecko.",
    },
    {
        "column_name": "extracted_at_utc",
        "data_type": "datetime",
        "description": "UTC timestamp showing when the data was extracted.",
    },
]


# =====================================================
# Expected Raw Outputs
# =====================================================

EXPECTED_RAW_OUTPUTS = {
    "frankfurter": {
        "format": "JSON list",
        "example_fields": ["date", "base", "quote", "rate"],
    },
    "coingecko": {
        "format": "JSON object",
        "example_fields": ["prices", "market_caps", "total_volumes"],
        "price_array_format": "[timestamp_ms, price]",
    },
}


# =====================================================
# API Assumptions and Constraints
# =====================================================

API_ASSUMPTIONS = [
    "Frankfurter does not require an API key.",
    "CoinGecko demo access requires an API key stored in the .env file.",
    "Frankfurter returns one fiat exchange rate row per date and quote currency.",
    "CoinGecko may return multiple intraday BTC prices for a 30-day range.",
    "BTC data will later be aggregated to one daily value before Tableau export.",
    "The initial implementation assumes the 30-day API responses fit in a single request.",
    "Pagination is not currently required, but later extraction code will include pagination-ready structure.",
    "Rate limit handling and retry logic will be implemented in the extraction phase.",
]


# =====================================================
# Simple Strategy Preview
# =====================================================

if __name__ == "__main__":
    print("API Source Strategy")
    print("===================")

    print(f"\nDate Range: {FROM_DATE} to {TO_DATE}")

    print("\nPlanned API Sources:")
    for source_key, source_details in API_SOURCES.items():
        print(f"\n- {source_details['source_name']}")
        print(f"  Purpose: {source_details['purpose']}")
        print(f"  Sample Request: {source_details['sample_request']}")

    print("\nTarget Analytical Schema:")
    for column in TARGET_SCHEMA:
        print(f"- {column['column_name']} ({column['data_type']}): {column['description']}")

    print("\nAPI Assumptions:")
    for assumption in API_ASSUMPTIONS:
        print(f"- {assumption}")
