USE ecommerce_analytics;
-- Sales KPIs: only delivered orders count as revenue.
SELECT COUNT(*) delivered_orders, ROUND(SUM(net_sales),2) revenue_inr,
 ROUND(SUM(profit),2) profit_inr, ROUND(AVG(net_sales),2) avg_order_value_inr
FROM orders WHERE order_status='Delivered';

-- Monthly revenue and profit
SELECT DATE_FORMAT(order_date,'%Y-%m') month, ROUND(SUM(net_sales),2) revenue,
 ROUND(SUM(profit),2) profit, COUNT(*) orders
FROM orders WHERE order_status='Delivered'
GROUP BY DATE_FORMAT(order_date,'%Y-%m') ORDER BY month;

-- Month-on-month revenue growth with window function
WITH monthly AS (
 SELECT DATE_FORMAT(order_date,'%Y-%m') month, SUM(net_sales) revenue
 FROM orders WHERE order_status='Delivered' GROUP BY DATE_FORMAT(order_date,'%Y-%m')
)
SELECT month, ROUND(revenue,2) revenue,
 ROUND(100*(revenue-LAG(revenue) OVER(ORDER BY month)) /
 NULLIF(LAG(revenue) OVER(ORDER BY month),0),2) mom_growth_pct
FROM monthly ORDER BY month;

-- Top 10 products
SELECT product_name, SUM(quantity) units, ROUND(SUM(net_sales),2) revenue
FROM orders WHERE order_status='Delivered'
GROUP BY product_name ORDER BY revenue DESC LIMIT 10;

-- Category profitability
SELECT category, ROUND(SUM(net_sales),2) revenue,
 ROUND(SUM(profit),2) profit,
 ROUND(100*SUM(profit)/NULLIF(SUM(net_sales),0),2) margin_pct
FROM orders WHERE order_status='Delivered' GROUP BY category ORDER BY revenue DESC;

-- City performance
SELECT city, COUNT(*) orders, ROUND(SUM(net_sales),2) revenue
FROM orders WHERE order_status='Delivered' GROUP BY city ORDER BY revenue DESC;

-- Repeat customers and purchase frequency
SELECT customer_id, COUNT(*) completed_orders, ROUND(SUM(net_sales),2) lifetime_revenue
FROM orders WHERE order_status='Delivered' GROUP BY customer_id
HAVING COUNT(*) > 1 ORDER BY lifetime_revenue DESC LIMIT 20;

-- Order outcomes
SELECT order_status, COUNT(*) order_count,
 ROUND(100*COUNT(*)/(SELECT COUNT(*) FROM orders),2) share_pct
FROM orders GROUP BY order_status ORDER BY order_count DESC;

-- Channel revenue
SELECT sales_channel, ROUND(SUM(net_sales),2) revenue, COUNT(*) orders
FROM orders WHERE order_status='Delivered' GROUP BY sales_channel ORDER BY revenue DESC;
