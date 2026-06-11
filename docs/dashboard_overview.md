# Market Health Overview Dashboard

## Overview

The Market Health Overview Dashboard serves as the primary analytical landing page for the Real-Time Market Health Orchestrator.

The dashboard provides executive-level visibility into currency and cryptocurrency market behavior by combining exchange rate monitoring, normalized performance analysis, and key market indicators into a single interactive experience.

The dashboard was designed to support business stakeholders responsible for monitoring international pricing exposure and understanding market volatility trends.

---

## Business Objective

Organizations operating across multiple countries are exposed to fluctuations in foreign exchange markets and cryptocurrency volatility.

The purpose of this dashboard is to:

* Monitor exchange rate movement
* Compare asset performance over time
* Identify emerging market trends
* Provide a consistent view of fiat and cryptocurrency assets
* Support pricing and financial planning decisions

---

## Dashboard Components

### Current Asset Value KPI

Displays the most recent value for the selected asset.

The KPI dynamically updates based on the asset selected by the user and provides an immediate view of current market conditions.

Displayed metrics include:

* Current asset value
* Monthly performance change
* Asset identifier

---

### Current Exchange Rate KPI

Displays the latest exchange rate relative to USD.

Example:

```text
1 USD = X EUR
1 USD = X GBP
1 USD = X BTC
```

The KPI automatically updates based on the selected asset.

---

### Exchange Rate Over Time

This visualization displays historical exchange rate movement across the selected analysis period.

Purpose:

* Identify short-term trends
* Observe directional movement
* Understand exchange rate behavior over time

The chart allows users to evaluate whether an asset is strengthening or weakening relative to USD.

---

### Base 100 Trend Visualization

The Base 100 Index normalizes each asset to a starting value of 100 at the beginning of the analysis period.

Purpose:

* Compare assets with different price scales
* Visualize relative performance
* Measure percentage-based movement

Without normalization, Bitcoin values would significantly outweigh EUR and GBP values, making direct comparison difficult.

Base 100 indexing places all assets on an equal analytical scale.

---

## Interactive Controls

### Selected Currency

Allows users to switch between:

```text
BTC
EUR
GBP
```

All KPI cards and exchange rate visualizations update automatically based on the selected asset.

---

### Risk Threshold Parameter

Allows users to define a custom volatility threshold.

This parameter is shared with the Volatility & Risk Monitoring dashboard and supports threshold-based analysis across the solution.

---

## Analytical Methodology

### Exchange Rate Analysis

All monitored assets are modeled relative to USD.

Examples:

```text
USD → EUR
USD → GBP
USD → BTC
```

This standardization creates a consistent analytical framework across both fiat and cryptocurrency assets.

---

### Base 100 Index Formula

The Base 100 Index is calculated using:

```text
(Current Value / First Period Value) × 100
```

A value greater than 100 indicates appreciation relative to the start of the period.

A value below 100 indicates depreciation relative to the start of the period.

---

## Intended Audience

This dashboard is intended for:

* Executive Leadership
* Finance Teams
* Pricing Strategy Teams
* Business Intelligence Teams
* Operations Leadership

---

## Key Business Questions Answered

The dashboard helps answer:

* How are monitored assets performing relative to USD?
* Which assets are appreciating or depreciating?
* How does Bitcoin volatility compare to traditional currencies?
* What are the current exchange rates?
* Which assets have experienced the strongest movement during the analysis period?

---

## Dashboard Screenshot

![Market Health Overview Dashboard](screenshots/market-health-overview-dashboard.pdf)

---

## Related Dashboard

The Market Health Overview Dashboard should be used in conjunction with:

```text
Volatility & Risk Monitoring Dashboard
```

While this dashboard focuses on overall market performance and trends, the Volatility Dashboard focuses on risk detection, threshold monitoring, and volatility analysis.

Together, the two dashboards provide a complete view of market health and market risk.
