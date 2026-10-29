# Power BI dashboard build guide

## Import
1. Open Power BI Desktop > Home > Get data > Text/CSV.
2. Select `data/orders_cleaned.csv` and click **Load**.
3. In the model, set `order_date` to Date, numeric amount columns to Decimal Number, and `quantity` to Whole Number.
4. Rename the table to `Orders`.

## DAX measures (Modeling > New measure)
```dax
Delivered Orders = CALCULATE(DISTINCTCOUNT(Orders[order_id]), Orders[order_status] = "Delivered")
Revenue = SUM(Orders[recognized_revenue])
Profit = SUM(Orders[recognized_profit])
Average Order Value = DIVIDE([Revenue], [Delivered Orders])
Profit Margin % = DIVIDE([Total Profit], [Revenue])
Customers = CALCULATE(DISTINCTCOUNT(Orders[customer_id]), Orders[order_status] = "Delivered")
Return Rate % = DIVIDE(CALCULATE(COUNTROWS(Orders), Orders[order_status] = "Returned"), COUNTROWS(Orders))
```

## Suggested layout
- Top: 5 KPI cards (Revenue, Profit, Orders, Average Order Value, Profit Margin %).
- Middle left: line chart, `order_month` vs Revenue (sort ascending).
- Middle right: clustered bar chart, `category` vs Revenue.
- Bottom left: bar chart, `city` vs Revenue.
- Bottom right: bar chart, `product_name` vs Revenue (Top N filter = 8).
- Slicers: city, category, sales_channel, order_status. **Note:** KPI measures always count delivered revenue regardless of slicer selection on status.
- Format currency in INR (₹), percentages appropriately, add descriptive titles.

## Validation
Compare total Revenue, Profit, and Delivered Orders to `data/kpi_summary.json` before publishing.
Save your local `.pbix` to `dashboard/` and export a screenshot to `visualizations/` before uploading to GitHub. This ZIP includes the instructions, **not a prebuilt `.pbix` file**.
