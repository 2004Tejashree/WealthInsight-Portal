import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# --- 1. CONFIGURATION AND DATA LOADING ---
st.set_page_config(
    page_title="Comprehensive Client Portfolio Dashboard",
    page_icon=":bank:",
    layout="wide", 
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_and_merge_data():
    """
    Loads all CSV files and merges them into a single analytical DataFrame,
    performing necessary data cleaning and feature engineering.
    """
    try:
        # Load Fact Table (Main client data) - Using 'banking-clients.csv'
        df_clients = pd.read_csv("datasets/banking-clients.csv")
        
        # Load Dimension Tables (Lookup data)
        df_relationships = pd.read_csv("datasets/banking-realtionships.csv")
        df_gender = pd.read_csv("datasets/gender.csv")
        df_advisors = pd.read_csv("datasets/investment-advisiors.csv")

        # --- Data Cleaning and Feature Engineering ---
        
        # Convert 'Joined Bank' to datetime format
        df_clients['Joined Bank'] = pd.to_datetime(df_clients['Joined Bank'], format='%d-%m-%Y', errors='coerce')
        
        # Calculate Client Tenure (Years)
        # Assuming current date for simplicity in a dashboard context
        today = pd.Timestamp(date.today())
        df_clients['Tenure_Years'] = (today - df_clients['Joined Bank']).dt.days / 365.25
        
        # Calculate Total Assets Under Management (AUM) for each client
        # Summing key asset columns
        asset_cols = ['Bank Deposits', 'Checking Accounts', 'Saving Accounts', 'Foreign Currency Account', 'Business Lending']
        # Fill NA with 0 before summing to ensure accurate calculation
        df_clients[asset_cols] = df_clients[asset_cols].fillna(0) 
        df_clients['Total_AUM'] = df_clients[asset_cols].sum(axis=1)
        
        # --- Merging (JOINs) ---
        
        # Merge 1: Banking Relationship (using BRId)
        df = pd.merge(df_clients, df_relationships, on='BRId', how='left')
        
        # Merge 2: Gender (using GenderId)
        df = pd.merge(df, df_gender, on='GenderId', how='left')
        
        # Merge 3: Investment Advisor (using IAId)
        df = pd.merge(df, df_advisors, on='IAId', how='left')
        
        # Clean up column names and fill missing values for presentation
        df['Banking Relationship'] = df['Banking Relationship'].fillna('Unknown')
        df['Gender'] = df['Gender'].fillna('Not Specified')
        df['Investment Advisor'] = df['Investment Advisor'].fillna('Unassigned')
        
        return df
    
    except FileNotFoundError as e:
        st.error(f"FATAL ERROR: One or more data files were not found. Please ensure all CSVs are in the 'banking_bi_project' folder. Missing file details: {e}")
        return pd.DataFrame() # Return empty DataFrame on failure

# Load the data
df_raw = load_and_merge_data()

# Stop if data loading failed
if df_raw.empty:
    st.stop()


# --- 2. SIDEBAR FILTERS ---
with st.sidebar:
    st.title("Client Segmentation Filters")
    st.markdown("---")
    
    # Banking Relationship Filter
    all_br = df_raw['Banking Relationship'].unique()
    selected_br = st.multiselect(
        "1. Relationship Type",
        options=all_br,
        default=all_br
    )

    # Investment Advisor Filter
    all_advisors = df_raw['Investment Advisor'].unique()
    selected_advisors = st.multiselect(
        "2. Investment Advisor",
        options=all_advisors,
        default=all_advisors
    )
    
    # Loyalty Classification Filter
    all_loyalty = df_raw['Loyalty Classification'].unique()
    selected_loyalty = st.multiselect(
        "3. Loyalty Tier",
        options=all_loyalty,
        default=all_loyalty
    )

    # Risk Weighting Filter
    all_risks = sorted(df_raw['Risk Weighting'].unique())
    selected_risks = st.multiselect(
        "4. Risk Weighting (1=Low, 3=High)",
        options=all_risks,
        default=all_risks
    )
    
    # Age Slider
    min_age, max_age = int(df_raw['Age'].min()), int(df_raw['Age'].max())
    age_range = st.slider(
        "5. Age Range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )

# --- 3. FILTERING THE DATA ---
df_filtered = df_raw[
    (df_raw['Banking Relationship'].isin(selected_br)) &
    (df_raw['Loyalty Classification'].isin(selected_loyalty)) &
    (df_raw['Investment Advisor'].isin(selected_advisors)) &
    (df_raw['Risk Weighting'].isin(selected_risks)) &
    (df_raw['Age'] >= age_range[0]) &
    (df_raw['Age'] <= age_range[1])
]

# Check if data is empty after filtering
if df_filtered.empty:
    st.warning("No client data matches the current filter selection. Adjust your sidebar filters.")
    st.stop()


# --- 4. DASHBOARD HEADER AND KEY PERFORMANCE INDICATORS (KPIs) ---
st.header("Banking Client Portfolio Summary")
st.markdown("This dashboard analyzes client demographics, asset allocation, and advisor performance.")
st.markdown("---")

# Calculate KPI values
total_clients = len(df_filtered)
total_portfolio_value = df_filtered['Total_AUM'].sum() / 1_000_000 # In Millions
avg_risk = df_filtered['Risk Weighting'].mean()
avg_tenure = df_filtered['Tenure_Years'].mean()

# Create KPI cards using columns
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.metric(
        label="Total Clients Selected",
        value=f"{total_clients:,}",
        delta=f"{(total_clients / len(df_raw) * 100):.1f}% of Firm Total"
    )

with kpi_col2:
    st.metric(
        label="Total AUM (Assets Under Management)",
        value=f"${total_portfolio_value:,.2f}M",
        delta="Aggregate Portfolio Value"
    )

with kpi_col3:
    st.metric(
        label="Average Client Risk Weighting",
        value=f"{avg_risk:.2f}",
        delta="Targeting high-value, medium-risk clients"
    )

with kpi_col4:
    st.metric(
        label="Average Client Tenure",
        value=f"{avg_tenure:.1f} Years",
        delta="Client Loyalty Indicator"
    )

st.markdown("---")


# --- 5. MAIN CONTENT (VISUALIZATIONS) ---

tab_segmentation, tab_advisor, tab_assets, tab_raw = st.tabs(["📊 Segmentation & Demographics", "👤 Advisor Performance", "💰 Asset Allocation", "🗃 Raw Data"])

with tab_segmentation:
    st.subheader("Client Demographic and Relationship Breakdown")
    col1, col2 = st.columns(2)
    
    # 1. Bar Chart: Client Count by Banking Relationship and Gender
    with col1:
        st.markdown("##### Client Count by Relationship & Gender")
        df_rel_gender = df_filtered.groupby(['Banking Relationship', 'Gender']).size().reset_index(name='Client Count')
        fig_rel_gender = px.bar(
            df_rel_gender,
            x='Banking Relationship',
            y='Client Count',
            color='Gender',
            title='Relationship Type by Gender',
            template='plotly_white',
            height=450
        )
        st.plotly_chart(fig_rel_gender, use_container_width=True)

    # 2. Scatter Plot: Age vs. Estimated Income, Colored by Loyalty
    with col2:
        st.markdown("##### Age vs. Estimated Income")
        fig_age_income = px.scatter(
            df_filtered,
            x='Age',
            y='Estimated Income',
            color='Loyalty Classification',
            size='Total_AUM',
            hover_data=['Name', 'Banking Relationship'],
            title='Age, Income, and Loyalty',
            labels={'Estimated Income': 'Estimated Income (USD)', 'Total_AUM': 'Total AUM'},
            template='plotly_white',
            height=450
        )
        st.plotly_chart(fig_age_income, use_container_width=True)


with tab_advisor:
    st.subheader("Investment Advisor Performance & Risk Analysis")

    # Group data by Advisor and calculate key metrics
    df_advisor_summary = df_filtered.groupby('Investment Advisor').agg(
        Total_AUM=('Total_AUM', 'sum'),
        Avg_Risk=('Risk Weighting', 'mean'),
        Client_Count=('Client ID', 'count'),
        Avg_Income=('Estimated Income', 'mean')
    ).reset_index().sort_values(by='Total_AUM', ascending=False)

    col3, col4 = st.columns(2)
    
    # 3. Bar Chart: Total AUM by Investment Advisor
    with col3:
        st.markdown("##### Total Assets Under Management (AUM) by Advisor")
        fig_aum_advisor = px.bar(
            df_advisor_summary,
            x='Investment Advisor',
            y='Total_AUM',
            color='Avg_Risk',
            color_continuous_scale=px.colors.sequential.Oranges,
            title='AUM by Advisor (Colored by Avg. Risk)',
            template='plotly_white',
            height=450
        )
        st.plotly_chart(fig_aum_advisor, use_container_width=True)

    # 4. Bubble Chart: Advisor Efficiency (Risk vs. Client Count)
    with col4:
        st.markdown("##### Advisor Risk Profile vs. Client Load")
        fig_risk_load = px.scatter(
            df_advisor_summary,
            x='Client_Count',
            y='Avg_Risk',
            size='Total_AUM',
            color='Investment Advisor',
            hover_name='Investment Advisor',
            title='Client Load vs. Average Portfolio Risk',
            template='plotly_white',
            height=450
        )
        st.plotly_chart(fig_risk_load, use_container_width=True)


with tab_assets:
    st.subheader("Asset and Loan Breakdown")
    
    # 5. Asset Allocation: Stacked Bar Chart of Asset Types
    asset_cols = ['Bank Deposits', 'Checking Accounts', 'Saving Accounts', 'Foreign Currency Account', 'Business Lending']
    
    df_assets_long = df_filtered.melt(
        id_vars=['Client ID', 'Banking Relationship'],
        value_vars=asset_cols,
        var_name='Asset_Type',
        value_name='Value'
    )
    
    # Group by asset type and relationship
    df_asset_summary = df_assets_long.groupby(['Asset_Type', 'Banking Relationship'])['Value'].sum().reset_index()

    st.markdown("##### Total Asset Allocation by Type and Relationship")
    fig_assets = px.bar(
        df_asset_summary,
        x='Asset_Type',
        y='Value',
        color='Banking Relationship',
        title='Total Value Across Core Asset Accounts, Segmented by Relationship',
        template='plotly_white',
        height=500
    )
    st.plotly_chart(fig_assets, use_container_width=True)
    
    # 6. Loan Exposure Meter
    total_loans = df_filtered['Bank Loans'].sum()
    total_aum = df_filtered['Total_AUM'].sum()
    loan_ratio = total_loans / (total_aum + total_loans) if (total_aum + total_loans) > 0 else 0
    
    st.markdown("---")
    st.markdown("##### Loan Exposure Ratio")
    st.metric(
        label="Total Bank Loans (USD)",
        value=f"${total_loans:,.0f}",
        delta=f"Loan Exposure Ratio: {loan_ratio:.2%}"
    )


with tab_raw:
    st.subheader("Filtered Client Data (Merged Table)")
    # Select columns to display in the raw data table
    display_cols = ['Client ID', 'Name', 'Age', 'Nationality', 'Occupation', 'Estimated Income', 
                    'Loyalty Classification', 'Banking Relationship', 'Total_AUM', 'Risk Weighting', 'Investment Advisor']
    
    st.dataframe(df_filtered[display_cols])

# --- END OF APP.PY ---
