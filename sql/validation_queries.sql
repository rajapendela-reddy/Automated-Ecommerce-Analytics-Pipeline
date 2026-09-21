USE ecommerce_analytics;

-- Check total number of records
SELECT COUNT(*) AS total_rows
FROM ecommerce_transformed;


-- Check for duplicate session records
SELECT
    session_id,
    COUNT(*) AS record_count
FROM ecommerce_transformed
GROUP BY session_id
HAVING COUNT(*) > 1;


-- Check for missing values in key fields
SELECT
    SUM(customer_id IS NULL) AS missing_customer_id,
    SUM(session_id IS NULL) AS missing_session_id,
    SUM(visit_date IS NULL) AS missing_visit_date,
    SUM(revenue IS NULL) AS missing_revenue,
    SUM(product_id IS NULL) AS missing_product_id
FROM ecommerce_transformed;


-- Check for invalid numeric values
SELECT
    SUM(revenue < 0) AS negative_revenue,
    SUM(unit_price < 0) AS negative_unit_price,
    SUM(quantity < 0) AS negative_quantity,
    SUM(discount_amount < 0) AS negative_discount,
    SUM(pages_viewed <= 0) AS invalid_page_views,
    SUM(time_on_site_sec < 0) AS negative_session_time
FROM ecommerce_transformed;
