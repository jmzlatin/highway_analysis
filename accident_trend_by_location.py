import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from bidi.algorithm import get_display
import streamlit as st

def compare_accident_trends(df):
    """
    Create a grouped bar chart comparing the average number of accidents (previous periods)
    and the current half-year for each tunnel/interchange. Annotate the differences in percentages.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'tunnel_or_interchange_number', 'date', and 'half_year_number'.

    Returns:
    - None. Displays a bar chart with annotations in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        required_columns = ['date', 'tunnel_or_interchange_number', 'half_year_number']
        if not all(col in df.columns for col in required_columns):
            st.error("The dataset must contain 'date', 'tunnel_or_interchange_number', and 'half_year_number' columns.")
            return

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Identify the current half-year
        current_half_year = df['half_year_number'].max()

        # Filter data for current and previous half-years
        current_period = df[df['half_year_number'] == current_half_year]
        previous_periods = df[df['half_year_number'] < current_half_year]

        # Group by tunnel/interchange and calculate averages
        avg_previous = previous_periods.groupby('tunnel_or_interchange_number').size() / previous_periods['half_year_number'].nunique()
        current_counts = current_period.groupby('tunnel_or_interchange_number').size()

        # Align the indices to ensure consistent comparisons
        all_tunnels = sorted(set(avg_previous.index).union(set(current_counts.index)))
        avg_previous = avg_previous.reindex(all_tunnels, fill_value=0)
        current_counts = current_counts.reindex(all_tunnels, fill_value=0)

        # Apply bidi for Hebrew text rendering
        hebrew_labels = [get_display(label) for label in all_tunnels]

        # Calculate percentage change
        percentage_change = ((current_counts - avg_previous) / avg_previous.replace(0, np.nan)) * 100

        # Create a grouped bar chart
        x = np.arange(len(all_tunnels))  # X-axis positions
        width = 0.35  # Width of the bars

        fig, ax = plt.subplots(figsize=(12, 7))
        bars1 = ax.bar(x - width/2, avg_previous, width, label=get_display('ממוצע חציונים קודמים'), color='skyblue', edgecolor='black')
        bars2 = ax.bar(x + width/2, current_counts, width, label=get_display('חציון נוכחי'), color='orangered', edgecolor='black')

        # Annotate the percentage changes above the bars
        for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
            diff = percentage_change.iloc[i]
            if not np.isnan(diff):  # Skip annotations where the average is 0
                color = 'green' if diff < 0 else 'red'
                symbol = '-' if diff < 0 else '+'

                ax.annotate(
                    f"{symbol}{abs(diff):.1f}%",  # Format the percentage change
                    xy=(bar2.get_x() + bar2.get_width() / 2, bar2.get_height() + 0.1),
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color=color,
                    fontweight='bold'
                )

        # Add labels, title, and legend
        ax.set_title(get_display('מגמות חציוניות לפי מיקום'), fontsize=14, fontweight='bold')
        ax.set_xlabel(get_display('מיקום'), fontsize=12)
        ax.set_ylabel(get_display('ממוצע תאונות לתקופה'), fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(hebrew_labels, rotation=45, fontsize=10)
        ax.legend(fontsize=10)

        # Adjust layout and display in Streamlit
        plt.tight_layout()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")