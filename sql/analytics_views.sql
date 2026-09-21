USE ecommerce_analytics;

-- Monthly performance view
CREATE OR REPLACE VIEW monthly_performance AS
SELECT
    year,
    month,
    month_name,
    COUNT(*) AS total_sessions,
    SUM(revenue) AS total_revenue,
    SUM(purchased) AS total_purchases,
    ROUND(AVG(time_on_site_min), 2) AS avg_session_minutes,
    ROUND(AVG(pages_viewed), 2) AS avg_pages_viewed
FROM ecommerce_transformed
GROUP BY
    year,
    month,
    month_name;


-- Marketing channel performance view
CREATE OR REPLACE VIEW marketing_performance AS
SELECT
    marketing_channel,
    COUNT(*) AS total_sessions,
    SUM(purchased) AS total_purchases,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(time_on_site_min), 2) AS avg_session_minutes,
    ROUND(
        SUM(purchased) * 100.0 / COUNT(*),
        2
    ) AS conversion_rate
FROM ecommerce_transformed
GROUP BY marketing_channel;


-- Product category performance view
CREATE OR REPLACE VIEW product_performance AS
SELECT
    product_category,
    COUNT(*) AS total_sessions,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price,
    ROUND(AVG(rating), 2) AS avg_rating
FROM ecommerce_transformed
GROUP BY product_category;
