# Amazon Marketplace Intelligence Platform

## Overview

Amazon Marketplace Intelligence Platform is a cloud-based solution built to automate Amazon product monitoring, seller classification, price tracking, and reporting.

The platform collects product information from Amazon, stores historical price data, classifies sellers based on business rules, and provides a searchable dashboard for business users.

---

## Problem Statement

Marketplace teams often spend significant time manually:

* Searching Amazon listings
* Tracking product prices
* Monitoring sellers
* Maintaining spreadsheets
* Generating reports

This process becomes difficult to scale as the number of tracked products increases.

---

## Solution

The platform automates the complete monitoring workflow:

1. Collects product information using ASINs
2. Updates centralized cloud-based records
3. Maintains historical price data
4. Classifies sellers using business rules
5. Generates automated reports
6. Provides a searchable dashboard

---

## Features

### Automated Data Collection

* Amazon ASIN monitoring
* Cloud-based execution
* Scheduled automation

### Seller Classification

Business rules:

| Seller         | Partner Type | Official Partner |
| -------------- | ------------ | ---------------- |
| The Pop Market | Official     | SMG              |
| Novus Retail   | Official     | Bathla           |
| Others         | Unofficial   | N/A              |

### Historical Price Tracking

* Daily price snapshots
* Historical price repository
* Trend analysis support

### Dashboard

Users can:

* Search products by ASIN
* View product details
* View seller information
* View partner classification
* View price history
* View price trend charts

### Reporting

* Google Sheets integration
* Excel report generation
* Automated email distribution

---

## Architecture

Amazon Listings

↓

Python Scraper

↓

GitHub Actions

↓

Google Sheets Database

↓

Historical Price Repository

↓

Streamlit Dashboard

↓

Business Users

---

## Tech Stack

* Python
* Streamlit
* Google Sheets API
* GitHub Actions
* Pandas
* GSpread

---

## Business Impact

### Before

* Manual Amazon searches
* Spreadsheet maintenance
* No centralized history
* Time-consuming reporting

### After

* Automated marketplace monitoring
* Historical pricing visibility
* Centralized cloud access
* Self-service reporting dashboard

---

## Future Roadmap

### Phase 2

* Product name search
* Advanced filtering
* Downloadable reports

### Phase 3

* Price drop alerts
* Competitor monitoring
* Analytics dashboard

### Phase 4

* Multi-marketplace support
* API integrations
* Enterprise reporting

---

## Live Demo

Streamlit Dashboard: https://amazon-asin-report-ytpevjgwfvmqfumbs7pfjy.streamlit.app/
---

## Author

Kushagra Bachhil

Marketplace Intelligence & Analytics Project
