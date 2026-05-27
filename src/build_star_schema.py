"""
Build Tableau-ready star schema tables from the transformed market dataset.
"""

from pathlib import Path
import pandas as pd


PROCESSED_DATA_DIR = Path("data/processed")
TABLEAU_DATA_DIR = Path("data/tableau")

TABLEAU_DATA_DIR.mkdir(parents=True, exist_ok=True)


def build_star_schema():
    input_file = PROCESSED_DATA_DIR / "market_health_timeseries.csv"

    df = pd.read_csv(input_file)
    df["date"] = pd.to_datetime(df["date"])

    # -----------------------------
    # dim_date
    # -----------------------------
    dim_date = (
        df[["date"]]
        .drop_duplicates()
        .sort_values("date")
        .reset_index(drop=True)
    )

    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["full_date"] = dim_date["date"].dt.date
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day_of_month"] = dim_date["date"].dt.day
    dim_date["week_start_date"] = (
        dim_date["date"] - pd.to_timedelta(dim_date["date"].dt.weekday, unit="D")
    ).dt.date

    dim_date = dim_date[
        [
            "date_key",
            "full_date",
            "year",
            "month",
            "month_name",
            "day_of_month",
            "week_start_date",
        ]
    ]

    # -----------------------------
    # dim_asset
    # -----------------------------
    dim_asset = (
        df[
            [
                "asset_code",
                "asset_type",
                "base_currency",
                "quote_currency",
            ]
        ]
        .drop_duplicates()
        .sort_values("asset_code")
        .reset_index(drop=True)
    )

    dim_asset["asset_key"] = range(1, len(dim_asset) + 1)

    dim_asset["asset_name"] = dim_asset["asset_code"].map(
        {
            "BTC": "Bitcoin",
            "EUR": "Euro",
            "GBP": "British Pound",
        }
    )

    dim_asset = dim_asset[
        [
            "asset_key",
            "asset_code",
            "asset_name",
            "asset_type",
            "base_currency",
            "quote_currency",
        ]
    ]

    # -----------------------------
    # dim_source
    # -----------------------------
    dim_source = (
        df[["source_api"]]
        .drop_duplicates()
        .sort_values("source_api")
        .reset_index(drop=True)
    )

    dim_source["source_key"] = range(1, len(dim_source) + 1)

    dim_source["source_type"] = dim_source["source_api"].map(
        {
            "CoinGecko": "Crypto Market API",
            "Frankfurter": "Foreign Exchange API",
        }
    )

    dim_source["source_url"] = dim_source["source_api"].map(
        {
            "CoinGecko": "https://api.coingecko.com/api/v3",
            "Frankfurter": "https://api.frankfurter.dev/v2/rates",
        }
    )

    dim_source = dim_source[
        [
            "source_key",
            "source_api",
            "source_type",
            "source_url",
        ]
    ]

    # -----------------------------
    # fact_market_rates
    # -----------------------------
    fact_df = df.copy()

    fact_df["date_key"] = fact_df["date"].dt.strftime("%Y%m%d").astype(int)

    fact_df = fact_df.merge(
        dim_asset[["asset_key", "asset_code"]],
        on="asset_code",
        how="left",
    )

    fact_df = fact_df.merge(
        dim_source[["source_key", "source_api"]],
        on="source_api",
        how="left",
    )

    fact_market_rates = fact_df[
        [
            "date_key",
            "asset_key",
            "source_key",
            "usd_value",
            "base_100_index",
            "daily_pct_change",
        ]
    ].copy()

    fact_market_rates["market_rate_key"] = range(1, len(fact_market_rates) + 1)

    fact_market_rates = fact_market_rates[
        [
            "market_rate_key",
            "date_key",
            "asset_key",
            "source_key",
            "usd_value",
            "base_100_index",
            "daily_pct_change",
        ]
    ]

    # -----------------------------
    # Export
    # -----------------------------
    dim_date.to_csv(TABLEAU_DATA_DIR / "dim_date.csv", index=False)
    dim_asset.to_csv(TABLEAU_DATA_DIR / "dim_asset.csv", index=False)
    dim_source.to_csv(TABLEAU_DATA_DIR / "dim_source.csv", index=False)
    fact_market_rates.to_csv(
        TABLEAU_DATA_DIR / "fact_market_rates.csv",
        index=False,
    )

    print("Star schema tables created:")
    print(TABLEAU_DATA_DIR / "dim_date.csv")
    print(TABLEAU_DATA_DIR / "dim_asset.csv")
    print(TABLEAU_DATA_DIR / "dim_source.csv")
    print(TABLEAU_DATA_DIR / "fact_market_rates.csv")


if __name__ == "__main__":
    build_star_schema()