import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import streamlit as st

def analyze_injuries(df):
    """
    Analyze the monthly variation in injury counts, identify peak months, and compare injuries
    to accident counts with statistical correlations. Generate a graph of monthly accidents vs. injuries.
    
    Parameters:
    - df (pd.DataFrame): DataFrame with 'date' and 'total_injuries' columns.

    Returns:
    - None. Displays a graph and summary statistics in the Streamlit app.
    """
    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Extract month and year for grouping
    df['month_year'] = df['date'].dt.to_period('M')

    # Count accidents and sum injuries per month
    monthly_data = df.groupby('month_year').agg(
        accident_count=('date', 'size'),
        total_injuries=('total_injuries', 'sum')
    ).reset_index()
    monthly_data['month_year'] = monthly_data['month_year'].dt.to_timestamp()

    # Statistical correlation between accidents and injuries
    correlation = monthly_data['accident_count'].corr(monthly_data['total_injuries'])

    # Prepare data for regression (optional for trend visualization)
    monthly_data['month_numeric'] = np.arange(len(monthly_data))
    X = monthly_data[['month_numeric']]
    y_accidents = monthly_data['accident_count']
    y_injuries = monthly_data['total_injuries']

    # Linear regression for accident trends
    model_accidents = LinearRegression()
    model_accidents.fit(X, y_accidents)
    monthly_data['accident_predicted'] = model_accidents.predict(X)

    # Linear regression for injury trends
    model_injuries = LinearRegression()
    model_injuries.fit(X, y_injuries)
    monthly_data['injury_predicted'] = model_injuries.predict(X)

    # Plot Graph 2
    plt.figure(figsize=(12, 7))
    plt.plot(monthly_data['month_year'], monthly_data['accident_count'], label='Monthly Accidents', marker='o')
    plt.plot(monthly_data['month_year'], monthly_data['total_injuries'], label='Monthly Injuries', marker='o', color='red')
    plt.plot(monthly_data['month_year'], monthly_data['accident_predicted'], linestyle='--', label='Accident Trend')
    plt.plot(monthly_data['month_year'], monthly_data['injury_predicted'], linestyle='--', label='Injury Trend', color='orange')

    # Calculate the start and end dates for the last half-year dynamically
    latest_date = df['date'].max()  # Get the most recent date in the data
    highlight_start = (latest_date - pd.offsets.MonthBegin(6)).date()  # Start of the last 6 months
    highlight_end = latest_date.date()  # End of the current/latest period

    # Highlight the last half-year on the chart
    plt.axvspan(highlight_start, highlight_end, color='yellow', alpha=0.3, label='Current Half-Year')

    plt.title('Monthly Accidents vs. Injuries (Sept 2022 - Dec 2024)')
    plt.xlabel('Month-Year')
    plt.ylabel('Counts')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the graph in Streamlit
    st.pyplot(plt)

    # Display summary statistics
    st.write("### Injury Analysis Summary")
    st.write(f"**Peak Months for Injuries:**")
    st.write(monthly_data.loc[monthly_data['total_injuries'].idxmax(), ['month_year', 'total_injuries']])
    st.write(f"**Correlation between Accidents and Injuries:** {correlation:.2f}")
