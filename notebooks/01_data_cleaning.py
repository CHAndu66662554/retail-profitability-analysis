import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
DATA_DIR=BASE_DIR/"data"
OUTPUTS_DIR=BASE_DIR/"outputs"

df=pd.read_csv(DATA_DIR/"superstore_raw.csv",encoding="latin-1")

print("Raw shape:",df.shape)
print("\nColumn dtypes:\n",df.dtypes)

df["Order Date"]=pd.to_datetime(df["Order Date"],format="%m/%d/%Y")
df["Ship Date"]=pd.to_datetime(df["Ship Date"],format="%m/%d/%Y")
df["Shipping Days"]=(df["Ship Date"]-df["Order Date"]).dt.days

print("\nDuplicate rows:",df.duplicated().sum())
print("\nNull values per column:\n",df.isnull().sum()[df.isnull().sum()>0])

df["Profit Margin"]=np.where(df["Sales"]!=0,df["Profit"]/df["Sales"],0)
df["Is Unprofitable"]=df["Profit"]<0

def bucket_discount(d):
    if d==0:
        return "No Discount"
    elif d<=0.2:
        return "Low (0-20%)"
    elif d<=0.4:
        return "Medium (20-40%)"
    else:
        return "High (40%+)"

df["Discount Bucket"]=df["Discount"].apply(bucket_discount)
df["Order Year"]=df["Order Date"].dt.year
df["Order Month"]=df["Order Date"].dt.month
df["Order Year-Month"]=df["Order Date"].dt.to_period("M").astype(str)

print("\nOverall profit margin: {:.1%}".format(df["Profit"].sum()/df["Sales"].sum()))
print("Unprofitable orders: {} ({:.1%} of all orders)".format(
    df["Is Unprofitable"].sum(),df["Is Unprofitable"].mean()
))
print("Date range:",df["Order Date"].min().date(),"to",df["Order Date"].max().date())

df.to_csv(DATA_DIR/"superstore_clean.csv",index=False)
print("\nSaved cleaned dataset. Final shape:",df.shape)