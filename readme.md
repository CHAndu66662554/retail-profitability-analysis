# Retail Profitability Analysis: The Discount Cliff

## Overview

Revenue going up doesn't mean much if you're losing money on the way there. That's the tension at the heart of this project — a retail dataset of 9,994 orders where the headline numbers look fine (12.5% overall profit margin) but hide a much rougher reality once you look at individual orders: nearly 1 in 5 of them actually lose money.

This project traces that gap back to its source using statistical analysis in Python, then builds a Power BI dashboard that makes the pattern visible and actionable for a non-technical audience.

## The Problem

Discounting is one of those levers that feels harmless in isolation — a 20% markdown to move inventory, a promo to win a deal — but it compounds fast. The question I wanted to answer wasn't "do discounts hurt profit" (that's obvious), but something more useful for an actual business:

1. How strong is the relationship between discount level and profit margin, really — and can I put a number on it?
2. Is the damage evenly spread, or concentrated in specific products, regions, or discount ranges?
3. Where should a business actually intervene first?

## Dataset

**Source:** [Superstore Sales Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)

- 9,994 retail orders across 2014–2017
- Sales, discount, profit, region, category, and sub-category for every order

## How I Approached It

**1. Data cleaning.** The file came in as a Windows/Excel export using Latin-1 encoding rather than UTF-8 — a small thing, but reading it with the wrong encoding would have silently corrupted text fields instead of throwing an obvious error, so I caught that early. I also engineered a few fields that weren't in the raw data but mattered for the analysis: profit margin per order, an "unprofitable" flag, and discount buckets (No/Low/Medium/High) to make grouping cleaner than working with raw continuous discount values.

**2. Correlation and regression.** Rather than assuming discount hurts margin because that's the obvious story, I tested it. A Pearson correlation between discount and profit margin came back at **-0.86** — a strong negative relationship — and a linear regression showed discount alone explains **75% of the variance in profit margin** (R² = 0.75, p < 0.001). That's an unusually clean relationship for real-world retail data, which made it worth digging into further rather than treating it as a footnote.

**3. Segmentation.** Once the overall relationship was clear, I broke profitability down by discount bucket, sub-category, and region to find exactly where the damage was concentrated — because "discounting hurts margin" isn't actionable on its own; knowing *which* discounts, on *which* products, in *which* regions is.

## Key Findings

**The discount cliff is real, and it's steep.** Average profit margin by discount level:

- No discount: **34% margin**, 0% of orders unprofitable
- Low discount (0–20%): **17.4% margin**, 13.8% of orders unprofitable
- Medium discount (20–40%): **-16.7% margin**, 90.2% of orders unprofitable
- High discount (40%+): **-108.9% margin**, 100% of orders unprofitable

That last row is worth sitting with — at 40%+ discount, the business isn't just breaking even, it's losing more than the item's entire sale price on *every single order*. There's no ambiguity in that number; it's not a "maybe review this" finding, it's a "this needs to stop or be capped" finding.

**Total dollar impact:** across all unprofitable orders, the business lost **$156,131** — not a rounding error, and squarely something a finance or ops team would want flagged.

**Sub-category tells you exactly where to look.** Tables and Bookcases are the two categories actually losing money overall (not just occasionally dipping negative — net negative across all their orders), while Copiers, Phones, and Accessories are the strongest performers. If a merchandising team had to pick two product lines to review pricing and discount policy on first, this points straight at them.

**Region matters more than I expected going in.** Central region has the weakest overall margin (7.9%) despite decent sales volume, and it's driven by consistently heavier discounting rather than a fundamentally different customer base or product mix — Central Furniture is actually running a *negative* margin (-1.8%). Meanwhile West region runs the strongest margin (14.9%) with comparatively modest discounting. Same company, same products, meaningfully different discipline by region.

## Business Recommendations

1. **Cap discounts above 20% pending review, and treat 40%+ as an exception requiring approval.** The data doesn't support these as a routine pricing tool — every single order at that level loses money, so this isn't a "watch it more closely" recommendation, it's a "stop doing this by default" one.
2. **Audit pricing and discount policy specifically for Tables and Bookcases.** These aren't marginal underperformers, they're net-negative — something structural is likely wrong with how they're priced or discounted, not just an unlucky mix of orders.
3. **Investigate why Central region discounts more heavily than the other three.** Whether it's local competitive pressure, a sales incentive structure, or inconsistent policy enforcement, the fact that West achieves better margin with less discounting suggests it's a solvable, region-specific practice rather than an unavoidable market condition.

## Interactive Dashboard

Built a Power BI dashboard to make this analysis explorable without needing to read Python code — including a scatter plot with trend line that visually reproduces the regression finding (annotated directly on the chart with the correlation coefficient, R², and p-value), plus drill-downs by region, category, and discount bucket.

One detail I made sure to get right: profit margin is a ratio, so it has to be aggregated as `total profit ÷ total sales`, not summed row-by-row like a normal number — a common Power BI mistake that quietly produces meaningless figures if you're not paying attention to how ratios behave under aggregation.

<p align="center">
  <img src="outputs/power_bi_dashboard.png" width="900">
</p>

Dashboard includes: total sales, overall margin, % unprofitable orders, and total profit lost as headline KPIs; a discount-vs-margin scatter plot with trend line and statistical annotation; a profit-margin-by-discount-bucket chart; a region × category profitability matrix with conditional heatmap coloring; and a sub-category profit breakdown, plus slicers for region, category, and date range.

## Project Structure

```text
retail-profitability-analysis/
│
├── data/
│   ├── superstore_raw.csv
│   └── superstore_clean.csv
│
├── notebooks/
│   ├── 01_data_cleaning.py
│   ├── 02_statistical_analysis.py
│   └── 03_visualization.py
│
├── outputs/
│   ├── category_profitability.csv
│   ├── subcategory_profitability.csv
│   ├── region_profitability.csv
│   ├── discount_bucket_analysis.csv
│   ├── discount_cliff.png
│   ├── profit_by_subcategory.png
│   └── power_bi_dashboard.png
│
├── Dashboard_retail-profitability.pbix
│
└── README.md
```

## Technologies Used

Python, Pandas, NumPy, SciPy, Matplotlib, Power BI, DAX, Power Query

## What This Project Shows

The easy version of this project stops at "discounts hurt profit," which nobody needed a dataset to tell them. The useful version puts a number on exactly how much, proves it statistically rather than assuming it, and narrows it down to the specific products, discount ranges, and region where a business would actually get the most value from acting first.

## Resume Highlight

> Analyzed 9,994 retail transactions using Python (Pandas, SciPy) to quantify the discount-profitability relationship (Pearson r = -0.86, R² = 0.75, p < 0.001); found 18.7% of orders were unprofitable, representing $156K in lost profit concentrated in specific sub-categories and regions, and built an interactive Power BI dashboard with corrected ratio-aggregation DAX measures to surface these findings for stakeholder action.
