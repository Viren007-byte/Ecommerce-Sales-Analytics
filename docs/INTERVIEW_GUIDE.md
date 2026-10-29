# Interview walkthrough

**Problem:** Understand which products, cities and channels drive e-commerce sales and profits.

**Data:** 2,400 synthetic single-product orders in 2025, generated for portfolio demonstration. This is NOT a real company's data.

**Method:** Validate dates, remove duplicate IDs and invalid records, compute discounted sales and costs, recognize revenue only for delivered orders, group by month/category/city/product, visualize KPIs.

**Key definitions:** Net sales = quantity × unit price × (1 - discount). Profit = net sales - quantity × unit cost. AOV = delivered net sales / delivered orders. Return rate = returned orders / all orders.

**Why exclude cancellations and returns?** This simplified project recognizes only delivered orders. Real accounting can require refund dates, partial returns, shipping, tax and revenue recognition policies.

**Interview questions to practice:**
1. Why did you choose Pandas instead of SQL for cleaning?
2. How do you handle duplicates, missing values and negative quantities?
3. What is the difference between revenue and profit?
4. Explain GROUP BY, HAVING, and LAG in your SQL queries.
5. Why is AOV calculated only on delivered orders?
6. How would you handle orders with multiple line items?
7. How would you automate the pipeline for daily refreshes?
8. What limitations does synthetic data introduce?

**Before describing this as your own work:** run the scripts, reproduce the KPIs, understand every chart, and customize the analysis. Credit any outside help appropriately.
