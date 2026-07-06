import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"
OUTPUTS_DIR=BASE_DIR/"outputs"

df=pd.read_csv(DATA_DIR/"superstore_clean.csv")

print("="*70)
print("CORRELATION: Discount vs Profit Margin")
print("="*70)

corr,p_value=stats.pearsonr(df["Discount"],df["Profit Margin"])
print(f"Pearson correlation: {corr:.3f} (p-value: {p_value:.2e})")
print("Interpretation:","strong negative" if corr<-0.5 else
      "moderate negative" if corr<-0.3 else "weak negative" if corr<0 else "positive")

print("\n"+"="*70)
print("LINEAR REGRESSION: Profit Margin ~ Discount")
print("="*70)

slope,intercept,r_value,p_value,std_err=stats.linregress(df["Discount"],df["Profit Margin"])
print(f"Profit Margin = {intercept:.3f} + ({slope:.3f}) * Discount")
print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.2e}")
print("\nInterpretation: every 10-percentage-point increase in discount is associated")
margin_change_per_10pct=slope*0.10
print(f"with a {abs(margin_change_per_10pct):.1%} {'decrease' if slope<0 else 'increase'} in profit margin")

print("\n"+"="*70)
print("PROFITABILITY BY CATEGORY")
print("="*70)

cat_summary=df.groupby("Category").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    avg_discount=("Discount","mean"),
    order_count=("Row ID","count")
).round(2)
cat_summary["profit_margin"]=(cat_summary["total_profit"]/cat_summary["total_sales"]).round(3)
print(cat_summary.sort_values("total_profit"))

print("\n"+"="*70)
print("PROFITABILITY BY SUB-CATEGORY (sorted worst to best)")
print("="*70)

subcat_summary=df.groupby("Sub-Category").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    avg_discount=("Discount","mean"),
    order_count=("Row ID","count")
).round(2)
subcat_summary["profit_margin"]=(subcat_summary["total_profit"]/subcat_summary["total_sales"]).round(3)
print(subcat_summary.sort_values("total_profit").to_string())

print("\n"+"="*70)
print("PROFITABILITY BY REGION")
print("="*70)

region_summary=df.groupby("Region").agg(
    total_sales=("Sales","sum"),
    total_profit=("Profit","sum"),
    avg_discount=("Discount","mean")
).round(2)
region_summary["profit_margin"]=(region_summary["total_profit"]/region_summary["total_sales"]).round(3)
print(region_summary.sort_values("total_profit"))

print("\n"+"="*70)
print("PROFIT MARGIN BY DISCOUNT BUCKET")
print("="*70)

discount_summary=df.groupby("Discount Bucket").agg(
    avg_profit_margin=("Profit Margin","mean"),
    total_profit=("Profit","sum"),
    order_count=("Row ID","count"),
    pct_unprofitable=("Is Unprofitable","mean")
).round(3)
print(discount_summary.reindex(["No Discount","Low (0-20%)","Medium (20-40%)","High (40%+)"]))

cat_summary.to_csv(OUTPUTS_DIR/"category_profitability.csv")
subcat_summary.to_csv(OUTPUTS_DIR/"subcategory_profitability.csv")
region_summary.to_csv(OUTPUTS_DIR/"region_profitability.csv")
discount_summary.to_csv(OUTPUTS_DIR/"discount_bucket_analysis.csv")

print("\nSaved all summary tables to /outputs")