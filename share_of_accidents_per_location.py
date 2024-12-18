import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from bidi.algorithm import get_display
from matplotlib import rcParams

def accidents_by_location_pie_chart(df):
    """
    Create a pie chart showing the percentage of accidents by tunnel/interchange
    with a color-matching legend that includes the percentages.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'tunnel_or_interchange_number' column.

    Returns:
    - None. Displays a pie chart in the Streamlit app.
    """
    try:
        # Ensure required column exists
        if 'tunnel_or_interchange_number' not in df.columns:
            st.error("The 'tunnel_or_interchange_number' column is missing from the dataset.")
            return

        # Count accidents by location
        location_counts = df['tunnel_or_interchange_number'].value_counts()

        # Apply bidi algorithm to render Hebrew text properly
        location_labels = [get_display(label) for label in location_counts.index]

        # Configure Matplotlib for Hebrew support
        rcParams['font.family'] = 'Arial'

        # Define colors using tab20 colormap
        colors = plt.cm.tab20.colors[:len(location_counts)]

        # Create a pie chart without autopct
        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, _ = ax.pie(
            location_counts,
            labels=None,  # No direct labels on the chart
            startangle=140,
            colors=colors,
            wedgeprops={'edgecolor': 'black'}
        )

        # Create a custom legend with percentages
        legend_labels = [
            f"{label} - {count / location_counts.sum() * 100:.1f}%"
            for label, count in zip(location_labels, location_counts)
        ]
        ax.legend(
            wedges,
            legend_labels,
            title=get_display("מיקום"),
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=10,
            title_fontsize=12
        )

        # Set the title
        plt.title(get_display('יחס מקומי תאונות - מפתיחת הכביש'), fontsize=14, weight='bold')
        plt.tight_layout()

        # Display the pie chart in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")