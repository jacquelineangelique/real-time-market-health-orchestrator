# Tableau Calculations

## Create Tableau Calculated Fields

This document defines the Tableau parameters and calculated fields used for volatility monitoring, threshold detection, and contextual KPI analysis.

---

## 1. Risk Threshold Parameter

### Name

```text
Risk Threshold %
````

### Data Type

```text
Float
```

### Current Value

```text
2.0
```

### Allowable Values

```text
Range
Minimum: 0
Maximum: 20
Step Size: 0.5
```

### Purpose

Allows dashboard users to dynamically define the percent-change threshold used to identify volatility events.

---

## 2. Volatility Trigger Calculated Field

### Field Name

```text
Volatility Trigger
```

### Tableau Formula

```tableau
ABS([daily_pct_change]) >= [Risk Threshold %]
```

### Purpose

Returns `TRUE` when the absolute daily percent change exceeds the selected risk threshold.

---

## 3. Volatility Status Calculated Field

### Field Name

```text
Volatility Status
```

### Tableau Formula

```tableau
IF ABS([daily_pct_change]) >= [Risk Threshold %]
THEN "Above Threshold"
ELSE "Normal"
END
```

### Purpose

Creates a categorical field for conditional formatting.

Recommended color logic:

```text
Above Threshold = Red
Normal = Neutral / Gray / Blue
```

---

## 4. Monthly Max Value LOD Expression

### Field Name

```text
Monthly Max Base 100 Index
```

### Tableau Formula

```tableau
{ FIXED [asset_code], DATETRUNC('month', [date]) : MAX([base_100_index]) }
```

### Purpose

Shows the maximum Base 100 Index value for each asset within each month.

This provides context alongside the daily value.

---

## 5. Daily Value vs Monthly Max Difference

### Field Name

```text
Distance From Monthly Max
```

### Tableau Formula

```tableau
[Monthly Max Base 100 Index] - [base_100_index]
```

### Purpose

Shows how far the current daily value is from that asset’s monthly peak.

---

## 6. Recommended Dashboard Usage

### Dashboard Page 1: Market Health Overview

Use:

```text
base_100_index
Monthly Max Base 100 Index
Distance From Monthly Max
asset_code
date
```

Recommended visuals:

```text
Line chart
KPI cards
Monthly max reference line
```

---

### Dashboard Page 2: Volatility Triggers

Use:

```text
daily_pct_change
Volatility Trigger
Volatility Status
Risk Threshold %
asset_code
date
```

Recommended visuals:

```text
Volatility heatmap
Risk threshold parameter control
Conditional red highlighting
Tooltip with daily percent change
```

---

## 7. Tooltip Recommendations

Suggested tooltip fields:

```text
Date
Asset Code
Asset Type
USD Value
Base 100 Index
Daily % Change
Risk Threshold %
Volatility Status
Monthly Max Base 100 Index
```

---

## 8. Validation Notes

Expected behavior:

* Increasing the Risk Threshold % should reduce the number of flagged volatility events.
* Decreasing the Risk Threshold % should increase the number of flagged volatility events.
* BTC should generally show larger swings than EUR or GBP.
* Monthly Max Base 100 Index should remain constant within each asset-month group.
