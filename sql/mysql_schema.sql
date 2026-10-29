-- MySQL 8+; load data/orders_cleaned.csv with MySQL Workbench Table Data Import Wizard.
CREATE DATABASE IF NOT EXISTS ecommerce_analytics;
USE ecommerce_analytics;
CREATE TABLE IF NOT EXISTS orders (
 order_id VARCHAR(12) PRIMARY KEY, order_date DATE NOT NULL, customer_id VARCHAR(12),
 product_id VARCHAR(12), product_name VARCHAR(120), category VARCHAR(80),
 city VARCHAR(80), sales_channel VARCHAR(40), quantity INT, unit_price DECIMAL(12,2),
 discount_pct DECIMAL(5,2), unit_cost DECIMAL(12,2), order_status VARCHAR(20),
 gross_sales DECIMAL(14,2), discount_amount DECIMAL(14,2), net_sales DECIMAL(14,2),
 total_cost DECIMAL(14,2), profit DECIMAL(14,2), recognized_revenue DECIMAL(14,2),
 recognized_profit DECIMAL(14,2), order_month VARCHAR(7)
);
