import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"
OUTPUTS_DIR=BASE_DIR/"outputs"

df=pd.read_csv(DATA_DIR/"superstore_clean.csv")

order=["No Discount","Low (0-20%)","Medium (20-40%)","High (40%+)"]
bucket_margin=df.groupby("Discount Bucket")["Profit Margin"].mean().reindex(order)*100

fig,ax=plt.subplots(figsize=(8,5))
colors=["#4a90a4" if v>=0 else "#d64545" for v in bucket_margin.values]
bars=ax.bar(bucket_margin.index,bucket_margin.values,color=colors)
ax.axhline(0,color="black",linewidth=0.8)
ax.set_ylabel("Average Profit Margin (%)")
ax.set_title("The Discount Cliff: Profit Margin by Discount Level")

for bar in bars:
    height=bar.get_height()
    va="bottom" if height>=0 else "top"
    offset=3 if height>=0 else -3
    ax.annotate(f"{height:.1f}%",xy=(bar.get_x()+bar.get_width()/2,height),
                xytext=(0,offset),textcoords="offset points",
                ha="center",va=va,fontweight="bold")

plt.tight_layout()
plt.savefig(OUTPUTS_DIR/"discount_cliff.png",dpi=150)
plt.close()
print("Saved discount_cliff.png")

subcat_profit=df.groupby("Sub-Category")["Profit"].sum().sort_values()

fig,ax=plt.subplots(figsize=(9,7))
colors=["#d64545" if v<0 else "#4a90a4" for v in subcat_profit.values]
ax.barh(subcat_profit.index,subcat_profit.values,color=colors)
ax.axvline(0,color="black",linewidth=0.8)
ax.set_xlabel("Total Profit ($)")
ax.set_title("Total Profit by Sub-Category\n(red = losing money)")

plt.tight_layout()
plt.savefig(OUTPUTS_DIR/"profit_by_subcategory.png",dpi=150)
plt.close()
print("Saved profit_by_subcategory.png")