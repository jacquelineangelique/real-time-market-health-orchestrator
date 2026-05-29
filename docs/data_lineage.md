# Data Lineage

## Overview

This document describes the end-to-end flow of data through the Real-Time Market Health Orchestrator solution.

The purpose of this document is to provide transparency into how data is sourced, transformed, modeled, and visualized.

---

## Source Systems

### CoinGecko API

Provides cryptocurrency market data.

Used for:

```text
Bitcoin (BTC)
```

Data retrieved:

```text
Historical BTC prices
```

---

### Frankfurter API

Provides foreign exchange rate data.

Used for:

```text
EUR
GBP
```

Data retrieved:

```text
USD/EUR
USD/GBP
```

exchange rates.

---

## Extraction Layer

Scripts:

```text
extract_market_data.py
```

Responsibilities:

* API connectivity
* Retry handling
* Rate-limit handling
* Error handling
* Raw JSON persistence

Outputs:

```text
data/raw/*.json
```

---

## Transformation Layer

Scripts:

```text
transform_market_data.py
```

Responsibilities:

* Flatten nested JSON
* Normalize asset schema
* Convert timestamps to ISO-8601
* Calculate Base 100 Index
* Calculate daily percent variance

Outputs:

```text
market_health_timeseries.csv
```

---

## Modeling Layer

Scripts:

```text
build_star_schema.py
```

Responsibilities:

* Create fact table
* Create date dimension
* Create asset dimension
* Create source dimension

Outputs:

```text
fact_market_rates.csv
dim_date.csv
dim_asset.csv
dim_source.csv
```

---

## Tableau Data Layer

The Tableau semantic model is constructed using relationships between:

```text
fact_market_rates
```

and

```text
dim_date
dim_asset
dim_source
```

Relationships:

```text
fact_market_rates.date_key
    → dim_date.date_key

fact_market_rates.asset_key
    → dim_asset.asset_key

fact_market_rates.source_key
    → dim_source.source_key
```

---

## Visualization Layer

### Dashboard 1

Market Health Overview

Purpose:

* KPI monitoring
* Exchange rate trends
* Base 100 comparison

---

### Dashboard 2

Volatility & Risk Monitoring

Purpose:

* Volatility heatmaps
* Threshold monitoring
* Monthly context analysis

---

## End-to-End Data Flow

```text
CoinGecko API
Frankfurter API
        │
        ▼
Extraction Layer
        │
        ▼
Raw JSON Storage
        │
        ▼
Transformation Layer
        │
        ▼
Star Schema Modeling
        │
        ▼
Tableau Data Sources
        │
        ▼
Interactive Dashboards
```

---

## Governance Considerations

The solution maintains:

* Source traceability
* Reproducible processing
* Dimensional modeling standards
* Clear separation of raw and transformed data
* Documented transformation logic
