"""
PR 03: Add Market Data Extraction Layer

Purpose:
Retrieve raw market data from Frankfurter and CoinGecko APIs,
handle API instability, and persist raw JSON responses for later
transformation steps.

This script does NOT transform data for Tableau yet.
"""

import os
import json
import time
import logging
import requests

from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv


# =====================================================
# Environment Setup
# =====================================================

load_dotenv()

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

if not COINGECKO_API_KEY:
    raise ValueError("Missing COINGECKO_API_KEY in .env file.")


# =====================================================
# Directory Setup
# =====================================================

RAW_DATA_DIR = Path("data/raw")
LOG_DIR = Path("logs")

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# Logging Setup
# =====================================================

logging.basicConfig(
    filename=LOG_DIR / "extraction.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# =====================================================
# Date Window
# =====================================================

LOOKBACK_DAYS = 30

end_date = datetime.today()
start_date = end_date - timedelta(days=LOOKBACK_DAYS)

FROM_DATE = start_date.strftime("%Y-%m-%d")
TO_DATE = end_date.strftime("%Y-%m-%d")

FROM_UNIX = int(start_date.timestamp())
TO_UNIX = int(end_date.timestamp())


# =====================================================
# Reusable API Request Helper
# =====================================================

def get_with_retries(url, max_retries=3, timeout=10):
    """
    Sends a GET request with retry handling.

    Handles:
    - 429 rate-limit responses
    - 500-level server errors
    - timeouts
    - temporary connection issues
    """

    for attempt in range(1, max_retries + 1):

        try:
            logging.info(f"Request attempt {attempt}: {url}")

            response = requests.get(url, timeout=timeout)

            # ---------------------------------------------
            # Rate limit handling
            # ---------------------------------------------
            # 429 means the API is throttling requests.
            # If Retry-After is provided, use it.
            # Otherwise, wait longer on each retry.
            # ---------------------------------------------

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait_time = int(retry_after) if retry_after else 5 * attempt

                logging.warning(
                    f"Rate limit hit. Waiting {wait_time} seconds."
                )

                time.sleep(wait_time)
                continue

            # ---------------------------------------------
            # Server error handling
            # ---------------------------------------------
            # 500, 502, 503, and 504 are usually temporary.
            # Retry using exponential backoff.
            # ---------------------------------------------

            if response.status_code in [500, 502, 503, 504]:
                wait_time = 2 ** attempt

                logging.warning(
                    f"Server error {response.status_code}. "
                    f"Retrying in {wait_time} seconds."
                )

                time.sleep(wait_time)
                continue

            # ---------------------------------------------
            # Non-retryable HTTP errors
            # ---------------------------------------------

            response.raise_for_status()

            logging.info("Request successful.")

            return response.json()

        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt

            logging.warning(
                f"Request timed out. Retrying in {wait_time} seconds."
            )

            time.sleep(wait_time)

        except requests.exceptions.ConnectionError:
            wait_time = 2 ** attempt

            logging.warning(
                f"Connection error. Retrying in {wait_time} seconds."
            )

            time.sleep(wait_time)

        except requests.exceptions.RequestException as error:
            logging.error(f"Non-retryable request error: {error}")
            raise

    raise RuntimeError(f"API request failed after {max_retries} attempts.")


# =====================================================
# Raw JSON Persistence
# =====================================================

def save_raw_json(data, source_name):
    """
    Saves raw API response exactly as received.

    Raw files are stored separately from transformed outputs
    to preserve source lineage and support reproducibility.
    """

    extraction_timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    output_path = RAW_DATA_DIR / f"{source_name}_{extraction_timestamp}.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    logging.info(f"Raw JSON saved: {output_path}")

    return output_path


# =====================================================
# Frankfurter Extraction
# =====================================================

def extract_frankfurter_rates():
    """
    Retrieves fiat exchange rates for EUR and GBP
    using USD as the base currency.

    Expected raw output:
    - date
    - base
    - quote
    - rate
    """

    base_currency = "USD"
    quote_currencies = "EUR,GBP"

    url = (
        "https://api.frankfurter.dev/v2/rates"
        f"?from={FROM_DATE}"
        f"&to={TO_DATE}"
        f"&base={base_currency}"
        f"&quotes={quote_currencies}"
    )

    logging.info("Starting Frankfurter extraction.")

    data = get_with_retries(url)

    output_path = save_raw_json(
        data=data,
        source_name="frankfurter_rates"
    )

    logging.info("Frankfurter extraction completed.")

    return output_path


# =====================================================
# CoinGecko Extraction
# =====================================================

def extract_coingecko_btc():
    """
    Retrieves BTC historical market data quoted in USD.

    Expected raw output:
    - prices
    - market_caps
    - total_volumes

    Note:
    CoinGecko may return multiple intraday values for a
    30-day range. Daily aggregation happens later in PR 04.
    """

    url = (
        "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"
        f"?vs_currency=usd"
        f"&from={FROM_UNIX}"
        f"&to={TO_UNIX}"
        f"&x_cg_demo_api_key={COINGECKO_API_KEY}"
    )

    logging.info("Starting CoinGecko BTC extraction.")

    data = get_with_retries(url)

    output_path = save_raw_json(
        data=data,
        source_name="coingecko_btc"
    )

    logging.info("CoinGecko BTC extraction completed.")

    return output_path


# =====================================================
# Main Extraction Runner
# =====================================================

def main():
    """
    Runs the extraction layer.

    Pipeline scope for PR 03:
    1. Retrieve raw FX rates
    2. Retrieve raw BTC prices
    3. Save raw JSON responses
    4. Log extraction results
    """

    logging.info("Market data extraction started.")

    frankfurter_file = extract_frankfurter_rates()
    coingecko_file = extract_coingecko_btc()

    logging.info("Market data extraction completed successfully.")

    print("Extraction completed successfully.")
    print(f"Frankfurter raw file: {frankfurter_file}")
    print(f"CoinGecko raw file: {coingecko_file}")


if __name__ == "__main__":
    main()
