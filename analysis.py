import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import streamlit as st

def monthly_accident_analysis(df):
    """
    Analyze monthly accidents and forecast using linear regression.
    Includes the equation of the regression line and highlights the current half-year.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with a 'date' column.

    Returns:
    - None. Displays a line graph, regression equation, and summary statistics in Streamlit.
    """
    # Ensure date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Extract month and year for grouping
    df['month_year'] = df['date'].dt.to_period('M')

    # Count accidents per month
    monthly_accidents = df.groupby('month_year').size()

    # Convert back to a DataFrame for further analysis
    monthly_accidents_df = monthly_accidents.reset_index(name='accident_count')
    monthly_accidents_df['month_year'] = monthly_accidents_df['month_year'].dt.to_timestamp()

    # Calculate monthly averages for different periods
    first_50_days = df[df['date'] <= df['date'].min() + pd.Timedelta(days=50)]
    subsequent_period = df[(df['date'] > df['date'].min() + pd.Timedelta(days=50)) & (df['date'] < '2024-07-01')]
    second_half_2024 = df[df['date'] >= '2024-07-01']

    # Average accidents
    avg_first_50_days = first_50_days.shape[0] / 2  # Approximation for two months
    avg_subsequent_period = subsequent_period.shape[0] / len(subsequent_period['date'].dt.to_period('M').unique())
    avg_second_half_2024 = second_half_2024.shape[0] / len(second_half_2024['date'].dt.to_period('M').unique())

    # Prepare data for regression
    monthly_accidents_df['month_numeric'] = np.arange(len(monthly_accidents_df))
    X = monthly_accidents_df[['month_numeric']]
    y = monthly_accidents_df['accident_count']

    # Linear regression
    model = LinearRegression()
    model.fit(X, y)
    monthly_accidents_df['predicted'] = model.predict(X)

    # Extract regression coefficients
    slope = model.coef_[0]
    intercept = model.intercept_
    regression_equation = f"Y = {slope:.4f}x + {intercept:.4f}"

    # Create the histogram
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        monthly_accidents_df['month_year'],
        monthly_accidents_df['accident_count'],
        color='skyblue',
        edgecolor='black'
    )

    # Add data labels
    for bar in bars:
        height = bar.get_height()
        if height > 0:  # Only label bars with height greater than 0
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10
            )

    # Plot regression line
    plt.plot(
        monthly_accidents_df['month_year'],
        monthly_accidents_df['predicted'],
        label='Forecast (Linear Regression)',
        linestyle='--',
        color='red'
    )

    # Highlight current half-year
    highlight_start = datetime(2024, 7, 1)
    highlight_end = datetime(2024, 12, 31)
    plt.axvspan(highlight_start, highlight_end, color='yellow', alpha=0.3, label='Current Half-Year')

    # Format the x-axis labels
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b-%y'))

    plt.title('Monthly Accident Counts (Sept 2022 - Dec 2024)')
    plt.xlabel('Month-Year')
    plt.ylabel('Number of Accidents')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    # Display graph in Streamlit
    st.pyplot(plt)

    # Display regression equation
    st.write("### Regression Analysis")
    st.write(f"**Regression Equation:** {regression_equation}")

    # Return averages as a summary
    st.write("### Accident Analysis Summary")

    st.write(f"{len(df['accident_severity'])} Accidents in {df['month_number'].nunique()} Months")
    st.write(f"Number of נזק בלבד Accidents {df['accident_severity'].value_counts()['נזק בלבד']}")
    st.write(f"Number of קלה Accidents {df['accident_severity'].value_counts()['קלה']}")
    st.write(f"Number of קשה Accidents {df['accident_severity'].value_counts()['קשה']}")
    st.write(f"Number of קשה Accidents {df['accident_severity'].value_counts()['קשה']}")
    st.write(f"Number of קטלנית Accidents {df['accident_severity'].value_counts()['קטלנית']}")