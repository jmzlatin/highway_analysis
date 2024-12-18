import pandas as pd
import matplotlib.pyplot as plt
from bidi.algorithm import get_display
from datetime import datetime
from matplotlib import rcParams
import streamlit as st

def monthly_accidents_by_severity(df):
    """
    Create a column chart showing the number of accidents per month for each severity.
    Each severity has its own column, and the values are displayed on top of each column.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'date' and 'accident_severity' columns.

    Returns:
    - None. Displays a column chart in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        required_columns = ['date', 'accident_severity']
        if not all(col in df.columns for col in required_columns):
            st.error("The dataset must contain 'date' and 'accident_severity' columns.")
            return

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Extract month-year for grouping
        df['month_year'] = df['date'].dt.to_period('M')

        # Group by month-year and accident severity
        severity_counts = df.groupby(['month_year', 'accident_severity']).size().unstack(fill_value=0)

        # Convert the month-year index to strings formatted as "Jan-24"
        severity_counts.index = severity_counts.index.strftime('%b-%y')

        # Configure Matplotlib for Hebrew support
        rcParams['font.family'] = 'Arial'  # Ensure a font supporting Hebrew is used

        # Correct Hebrew labels for the legend
        severity_labels = [get_display(label) for label in severity_counts.columns]

        # Plot the column chart
        plt.figure(figsize=(12, 6))
        ax = severity_counts.plot(
            kind='bar',
            figsize=(12, 6),
            colormap='tab10',
            edgecolor='black',
            legend=True
        )

        # Add data labels on top of each bar
        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                if height > 0:  # Only label bars with height greater than 0
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height,
                        f'{int(height)}',
                        ha='center',
                        va='bottom',
                        fontsize=10
                    )



        # Update legend with Hebrew labels
        plt.legend(severity_labels, title=get_display('חומרת תאונה'), fontsize=10, title_fontsize=12)
        plt.title(get_display("תאונה לפי חומרה"), fontsize=14)
        plt.xlabel(get_display('חודש-שנה'), fontsize=12)
        plt.ylabel(get_display('מספר תאונות'), fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)

    except Exception as e:
        st.error(f"An error occurred: {e}")