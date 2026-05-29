# Volatility & Risk Monitoring Dashboard

## Overview

The Volatility & Risk Monitoring Dashboard provides operational visibility into day-over-day market fluctuations across monitored assets including Bitcoin (BTC), Euro (EUR), and British Pound (GBP).

The dashboard is designed to identify unusual market movements, highlight periods of elevated volatility, and provide business users with a configurable risk monitoring experience.

---

## Business Objective

International SaaS subscription pricing can be affected by currency fluctuations and cryptocurrency market volatility.

The purpose of this dashboard is to:

* Monitor daily market volatility
* Identify abnormal market behavior
* Support pricing strategy decisions
* Provide visibility into emerging market risks
* Enable threshold-based alerting analysis

---

## Key Features

### Volatility Heatmap

The heatmap visualizes daily percentage variance for each monitored asset.

Each cell represents:

```text
Asset + Date
```

and displays the corresponding day-over-day percentage change.

Users can quickly identify periods of elevated volatility through color intensity and threshold highlighting.

---

### Risk Threshold Parameter

Users can dynamically adjust the acceptable volatility threshold using a Tableau parameter.

Example:

```text
0.5%
1.0%
2.0%
5.0%
```

As the threshold changes, the dashboard automatically updates to identify days exceeding the selected risk tolerance.

---

### Volatility Trigger Logic

Days exceeding the selected threshold are categorized as:

```text
Above Threshold
```

All other observations are categorized as:

```text
Normal
```

This logic enables rapid identification of potentially impactful market movements.

---

### Monthly Context Using LOD Expressions

The dashboard includes a FIXED Level of Detail (LOD) calculation that identifies the maximum normalized value for each asset within a given month.

This allows users to compare daily performance against monthly peaks.

---

## Analytical Metrics

### Daily Percent Change

Measures day-over-day percentage movement.

Formula:

```text
(Current Value - Prior Value) / Prior Value
```

---

### Base 100 Index

Normalizes all assets to a common starting value of 100.

This enables meaningful comparisons between assets with significantly different price scales.

---

## Intended Audience

* Business Intelligence Teams
* Finance Teams
* Pricing Strategy Teams
* Executive Leadership
* Product Management
* Operations Leadership

---

## Screenshot

![Volatility Dashboard](docs/screenshots/volatility-and-risk-monitoring.pdf)
