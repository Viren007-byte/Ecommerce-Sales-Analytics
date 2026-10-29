"""Reproducible e-commerce analysis. Run: python src/analyze.py"""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CHARTS = ROOT / "visualizations"
CHARTS.mkdir(exist_ok=True)

def load_and_clean():
    df = pd.read_csv(DATA / "orders_raw.csv", parse_dates=["order_date"])
    df = df.drop_duplicates(subset=["order_id"]).copy()
    required = ["order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price", "discount_pct", "unit_cost", "order_status"]
    df = df.dropna(subset=required)
    df = df[(df.quantity > 0) & (df.unit_price >= 0) & (df.unit_cost >= 0) & df.discount_pct.between(0, 1)]
    df["gross_sales"] = (df.quantity * df.unit_price).round(2)
    df["discount_amount"] = (df.gross_sales * df.discount_pct).round(2)
    df["net_sales"] = (df.gross_sales - df.discount_amount).round(2)
    df["total_cost"] = (df.quantity * df.unit_cost).round(2)
    df["profit"] = (df.net_sales - df.total_cost).round(2)
    # Only delivered orders contribute to recognized sales and profit.
    df["recognized_revenue"] = df.net_sales.where(df.order_status == "Delivered", 0.0)
    df["recognized_profit"] = df.profit.where(df.order_status == "Delivered", 0.0)
    df["order_month"] = df.order_date.dt.to_period("M").astype(str)
    df.to_csv(DATA / "orders_cleaned.csv", index=False)
    return df

def save_bar(series, title, filename, ylabel="INR"):
    ax = series.plot(kind="bar", figsize=(10, 5), color="#2574A9")
    ax.set_title(title); ax.set_ylabel(ylabel); ax.set_xlabel("")
    plt.xticks(rotation=35, ha="right"); plt.tight_layout()
    plt.savefig(CHARTS / filename, dpi=160); plt.close()

def main():
    df = load_and_clean()
    delivered = df[df.order_status == "Delivered"].copy()
    monthly = delivered.groupby("order_month").agg(revenue=("net_sales","sum"),profit=("profit","sum"),orders=("order_id","nunique")).reset_index()
    monthly["mom_growth_pct"] = (monthly.revenue.pct_change() * 100).round(2)
    monthly.to_csv(DATA / "monthly_summary.csv", index=False)
    categories = delivered.groupby("category").net_sales.sum().sort_values(ascending=False)
    cities = delivered.groupby("city").net_sales.sum().sort_values(ascending=False)
    products = delivered.groupby("product_name").net_sales.sum().sort_values(ascending=False)
    save_bar(categories,"Revenue by product category","category_revenue.png")
    save_bar(cities,"Revenue by city","city_revenue.png")
    save_bar(products.head(8),"Top 8 products by revenue","top_products.png")
    ax = monthly.plot(x="order_month",y="revenue",kind="line",marker="o",figsize=(10,5),legend=False,color="#2574A9")
    ax.set(title="Monthly recognized revenue",xlabel="Month",ylabel="INR")
    plt.xticks(rotation=45,ha="right");plt.tight_layout();plt.savefig(CHARTS / "monthly_revenue.png",dpi=160);plt.close()
    metrics = {
        "total_orders": int(df.order_id.nunique()),
        "delivered_orders": int(delivered.order_id.nunique()),
        "recognized_revenue_inr": round(float(delivered.net_sales.sum()),2),
        "recognized_profit_inr": round(float(delivered.profit.sum()),2),
        "average_order_value_inr": round(float(delivered.net_sales.mean()),2),
        "unique_delivered_customers": int(delivered.customer_id.nunique()),
        "cancelled_orders": int((df.order_status=="Cancelled").sum()),
        "returned_orders": int((df.order_status=="Returned").sum()),
        "repeat_customers": int((delivered.groupby("customer_id").order_id.nunique() > 1).sum()),
    }
    import json
    (DATA / "kpi_summary.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    print("Analysis completed. KPIs:")
    print(json.dumps(metrics,indent=2))
    print("Charts saved to",CHARTS)

if __name__ == "__main__":
    main()
