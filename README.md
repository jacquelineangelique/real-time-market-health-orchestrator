# Real-Time Market Health Orchestrator

## Business Problem

Global organizations often rely on exchange rate and cryptocurrency market data when pricing products and services across international markets. In many organizations, this information is manually downloaded from external sources and maintained in spreadsheets, resulting in delayed insights, inconsistent reporting, and limited visibility into market volatility.

This project simulates a real-world data integration and business intelligence solution by automating the collection, transformation, modeling, and visualization of foreign exchange and cryptocurrency market data.

The solution enables business users to monitor market movement, identify volatility risks, and compare asset performance through interactive Tableau dashboards.

---

# Solution Overview

The Real-Time Market Health Orchestrator is an end-to-end ETL and analytics workflow that:

1. Extracts market data from external APIs.
2. Stores raw source responses for traceability.
3. Transforms and normalizes market data into a consistent analytical structure.
4. Builds a dimensional star schema optimized for Tableau.
5. Delivers interactive dashboards for volatility monitoring and comparative trend analysis.

The solution was designed to demonstrate:

* API integration
* ETL pipeline development
* Error handling and resiliency
* Data modeling
* Business intelligence dashboard development
* Data lineage documentation

---

# Architecture Overview

```text
Frankfurter API           CoinGecko API
      │                        │
      └────────────┬───────────┘
                   │
            API Extraction
                   │
            Raw JSON Storage
                   │
         Transformation Layer
                   │
         Analytical Dataset
                   │
          Star Schema Model
                   │
        Tableau Data Sources
                   │
          Tableau Dashboards
```

---

# API Source Strategy

## Frankfurter API

Purpose:

Retrieve foreign exchange rates for:

* EUR
* GBP

Base Currency:

```text
USD
```

Example Endpoint:

```text
https://api.frankfurter.dev/v2/rates
```

Usage:

```text
USD → EUR
USD → GBP
```

Returned Data:

```json
{
  "date": "2026-05-26",
  "base": "USD",
  "quote": "EUR",
  "rate": 0.85831
}
```

---

## CoinGecko API

Purpose:

Retrieve historical Bitcoin market prices.

Example Endpoint:

```text
https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range
```

Returned Data:

```json
{
  "prices": [
    [1716681600000, 77012.42]
  ]
}
```

Transformation Logic:

CoinGecko returns:

```text
1 BTC = X USD
```

The transformation layer converts this into:

```text
1 USD = X BTC
```

This creates a consistent exchange-rate model across all monitored assets.

---

# Data Lineage

The following data lineage documents the movement of data through the solution.

## Stage 1: Extraction Layer

Scripts:

```text
src/extract_market_data.py
```

Responsibilities:

* Connect to APIs
* Handle retries
* Handle rate limits
* Handle API failures
* Store raw JSON responses

Output:

```text
data/raw/
```

Examples:

```text
coingecko_btc_*.json
frankfurter_rates_*.json
```

---

## Stage 2: Transformation Layer

Scripts:

```text
src/transform_market_data.py
```

Responsibilities:

* Flatten JSON structures
* Convert timestamps to ISO-8601
* Normalize BTC exchange rates
* Calculate Base 100 Index
* Calculate Daily Percent Change

Output:

```text
data/processed/market_health_timeseries.csv
```

---

## Stage 3: Star Schema Layer

Scripts:

```text
src/build_star_schema.py
```

Responsibilities:

* Generate analytical fact table
* Generate supporting dimensions
* Create Tableau-ready model

Output:

```text
data/tableau/
```

---

# Star Schema Design

## Fact Table

### fact_market_rates.csv

Central analytical table containing:

* usd_value
* base_100_index
* daily_pct_change

Keys:

* market_rate_key
* date_key
* asset_key
* source_key

Grain:

```text
One record per asset per day
```

---

## Date Dimension

### dim_date.csv

Contains:

* full_date
* year
* month
* month_name
* day_of_month
* week_start_date
* day_sequence

Purpose:

Supports time-series analysis and Tableau date filtering.

---

## Asset Dimension

### dim_asset.csv

Contains:

* asset_code
* asset_name
* asset_type
* base_currency
* quote_currency

Assets:

```text
BTC
EUR
GBP
```

Purpose:

Provides descriptive metadata used for filtering and dashboard analysis.

---

## Source Dimension

### dim_source.csv

Contains:

* source_api
* source_type
* source_url

Purpose:

Maintains source system traceability and data lineage.

---

# Project Structure

```text
project-root
│
├── data
│   ├── raw
│   ├── processed
│   └── tableau
│
├── logs
│
├── src
│   ├── extract_market_data.py
│   ├── transform_market_data.py
│   ├── build_star_schema.py
│   ├── prepare_tableau_dataset.py
│   └── run_pipeline.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# Environment Configuration

Create a file named:

```text
.env
```

Example:

```env
COINGECKO_API_KEY=YOUR_API_KEY

ENVIRONMENT=dev
```

Notes:

* Frankfurter API does not require authentication.
* CoinGecko requires an API key for historical market data access.

---

# Installation

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Pipeline

Execute the full ETL workflow:

```bash
python src/run_pipeline.py
```

Pipeline execution performs:

1. API Extraction
2. Raw JSON Storage
3. Transformation Processing
4. Star Schema Generation
5. Tableau Dataset Creation

Generated outputs:

```text
data/raw/
data/processed/
data/tableau/
```

---

# Tableau Data Sources

The Tableau dashboards consume the following files:

```text
fact_market_rates.csv
dim_date.csv
dim_asset.csv
dim_source.csv
```

Recommended Relationships:

```text
fact_market_rates.date_key
    ↔ dim_date.date_key

fact_market_rates.asset_key
    ↔ dim_asset.asset_key

fact_market_rates.source_key
    ↔ dim_source.source_key
```

---

# Tableau Dashboards

## Dashboard 1: Market Health Overview

Provides:

* Current Asset Value KPI
* Current Exchange Rate KPI
* Exchange Rate Trend Analysis
* Base 100 Trend Comparison
* Interactive Currency Selection

Purpose:

Executive-level monitoring of market performance.

---

## Dashboard 2: Volatility & Risk Monitoring

Provides:

* Volatility Heatmap
* Risk Threshold Parameter
* Volatility Trigger Alerts
* Monthly Maximum Context (LOD)

Purpose:

Identify abnormal volatility and monitor market risk conditions.

---

# Technologies Used

* Python
* Pandas
* Requests
* CoinGecko API
* Frankfurter API
* Tableau Cloud
* Tableau Public
* GitHub
* GitHub Actions

---

# Future Enhancements

Potential improvements include:

* Automated scheduling
* Incremental loading
* Cloud data storage
* Database integration
* Alerting and notifications
* Additional cryptocurrency support
* Forecasting models
* Real-time streaming architecture

```
```
