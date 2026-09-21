# Automated E-commerce Analytics Pipeline

An end-to-end analytics pipeline that automates e-commerce data processing, validation, transformation, SQL-based analysis, and Power BI reporting.

## Project Overview

This project demonstrates an automated workflow for converting raw e-commerce data into business-ready insights.

The pipeline processes 25,000+ records and combines Python ETL, SQL analytics, Power BI visualization, and scheduled automation.

## Architecture

Raw Excel Data
        ↓
Python ETL Pipeline
        ↓
Data Validation & Transformation
        ↓
Reporting CSV
        ↓
SQL Analytics Layer
        ↓
Power BI Dashboard

Scheduled using Windows Task Scheduler

## Tech Stack

- Python
- Pandas
- SQL / MySQL
- Power BI
- DAX
- Excel
- Windows Task Scheduler
- GitHub

## Data Pipeline

### 1. Extract

The pipeline automatically identifies the input Excel file and loads the raw e-commerce dataset using Pandas.

### 2. Validate

Automated data-quality checks are performed for:

- Missing values
- Duplicate records
- Negative revenue
- Invalid prices
- Invalid quantities
- Invalid page views
- Negative session duration

### 3. Transform

The pipeline creates reporting-ready fields including:

- Gross transaction value
- Conversion flag
- Abandonment flag
- Session duration in minutes
- Actual discount rate
- Year
- Month
- Month name
- Weekday
- Week

### 4. SQL Analytics

SQL queries and views are used to create reusable analytical datasets for:

- Monthly performance
- Marketing-channel performance
- Product-category performance

### 5. Power BI

The final dashboard provides:

- Total Revenue
- Total Sessions
- Total Purchases
- Conversion Rate
- Average Session Time
- Monthly Revenue Trend
- Marketing Channel Performance
- Product Category Performance
- Interactive filtering

### 6. Automation

Windows Task Scheduler executes the Python ETL pipeline on a recurring schedule.

The pipeline also maintains an execution log containing:

- Execution timestamp
- Pipeline status
- Row count
- Validation results
- Error information

## Repository Structure

```text
Automated-Ecommerce-Analytics-Pipeline/
│
├── python/
│   └── automated_etl.py
│
├── sql/
│   ├── validation_queries.sql
│   └── analytics_views.sql
│
├── data/
│   └── sample/
│       └── Ecommerce_sample.xlsx
│
├── output/
│   └── ecommerce_reporting_sample.csv
│
├── logs/
│   └── pipeline_log_sample.csv
│
├── powerbi/
│   └── Ecommerce_Analytics.pbix
│
└── README.md
