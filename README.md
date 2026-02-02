# Comprehensive Banking Client Portfolio Dashboard

## Description
The **Comprehensive Banking Client Portfolio Dashboard** is a robust Business Intelligence (BI) tool designed to provide deep insights into bank client data. Built using **Python** and **Streamlit**, this application integrates disparate data sources—including client demographics, financial assets, investment interactions, and advisor performance—into a unified analytical interface.

It empowers banking relationship managers and executives to:
- **Analyze Client Segments**: Understand the distribution of clients across different relationship types, loyalty tiers, and risk profiles.
- **Track Portfolio Health**: Monitor critical KPIs such as Total Assets Under Management (AUM), Loan Exposure, and Client Tenure.
- **Evaluate Performance**: Assess the efficiency and risk handling of Investment Advisors.

By transforming raw CSV data into interactive visualizations, this project facilitates data-driven decision-making for customer retention, asset allocation, and risk management strategies.

## Key Features

### 1. Data Integration & Automated Processing
- **Multi-Source Merging**: Automatically loads and joins data from multiple CSV files, linking Client Fact tables with Dimension tables for Gender, Investment Advisors, and Banking Relationships.
- **Dynamic Feature Engineering**: Computes real-time metrics such as *Client Tenure (Years)* and *Total AUM* by aggregating multiple asset columns (Deposits, Savings, Foreign Currency, etc.).

### 2. Advanced Segmentation and Filtering
- **Interactive Sidebar controls**: Users can filter the entire dashboard by:
  - **Relationship Type** (e.g., Premium, Standard)
  - **Investment Advisor**
  - **Loyalty Classification**
  - **Risk Weighting**
  - **Age Range** (via slider)
- **Context-Aware Analytics**: All charts and KPIs update instantly based on the applied filters.

### 3. Executive KPI Dashboard
- **High-Level Metrics**: distinct cards displaying:
  - **Total Clients** (with percentage of firm total)
  - **Total AUM** (in Millions USD)
  - **Average Risk Weighting**
  - **Average Client Tenure**

### 4. Rich Interactive Visualizations
- **Demographics Tab**:
  - *Bar Chart*: Client distribution by Relationship & Gender.
  - *Scatter Plot*: Correlation between Age, Estimated Income, and Loyalty status.
- **Advisor Performance Tab**:
  - *Leaderboard*: Advisors ranked by Total AUM.
  - *Bubble Chart*: Advisor efficiency analysis comparing Client Load vs. Average Portfolio Risk.
- **Asset Allocation Tab**:
  - *Stacked Bar Chart*: Detailed breakdown of key assets (Checking, Savings, Business Lending) by Relationship type.
  - *Loan Exposure Meter*: Calculates and displays the Loan-to-Value ratio across the portfolio.

### 5. Data Transparency
- **Raw Data Viewer**: A dedicated section to inspect the underlying filtered dataset in a tabular format, ensuring transparency and allowing for granular record checks.

## Installation

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
