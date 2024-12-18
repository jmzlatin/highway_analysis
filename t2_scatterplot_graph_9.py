import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from bidi.algorithm import get_display
import streamlit as st

def t2_tunnel_scatter_plot(df):
    """
    Create a scatter plot showing accidents in Tunnel T4.
    X-axis: months (dates), Y-axis: hours of the day (as total seconds since midnight).

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'tunnel_or_interchange_number',
                         'date', and 'exact_hour' columns.

    Returns:
    - None. Displays a scatter plot in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        required_columns = ['date', 'tunnel_or_interchange_number', 'exact_hour']
        if not all(col in df.columns for col in required_columns):
            st.error("The dataset must contain 'date', 'tunnel_or_interchange_number', and 'exact_hour' columns.")
            return

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Clean and convert the 'exact_hour' column
        df['exact_hour'] = df['exact_hour'].astype(str).str.strip()  # Remove spaces and convert to string
        df['exact_hour'] = pd.to_datetime(df['exact_hour'], format='%H:%M:%S', errors='coerce').dt.time

        # Drop rows with NaT values in 'exact_hour'
        df = df.dropna(subset=['exact_hour'])

        # Convert 'exact_hour' to total seconds since midnight
        df['hour_seconds'] = df['exact_hour'].apply(lambda t: t.hour * 3600 + t.minute * 60 + t.second)

        # Filter data for Tunnel T4
        t2_data = df[df['tunnel_or_interchange_number'] == 'T2']

        if t2_data.empty:
            st.warning(get_display("אין נתונים זמינים עבור מנהרת T2."))
            return

        # Configure Matplotlib for Hebrew support
        rcParams['font.family'] = 'Arial'

        # Plot the scatter plot
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(t2_data['date'], t2_data['hour_seconds'], color='green', s=50)

        # Highlight specific time range (12:00 to 20:00)
        ax.axhspan(12 * 3600, 20 * 3600, color='red', alpha=0.2, label=get_display('הדגשה: 12:00-20:00'))

        # Add labels, title, and grid
        ax.set_title(get_display("מנהרת T2"), fontsize=14, fontweight='bold')
        ax.set_xlabel(get_display("תאריך"), fontsize=12)
        ax.set_ylabel(get_display("שעה מדויקת (שניות מאז חצות)"), fontsize=12)
        ax.set_yticks([i * 3600 for i in range(0, 25, 4)])  # Tick marks every 4 hours
        ax.set_yticklabels([f"{i}:00" for i in range(0, 25, 4)])  # Format Y-axis labels as hours
        ax.legend()
        ax.grid(True)

        # Format X-axis to display months
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b/%Y'))
        plt.xticks(rotation=45)

        # Display the plot in Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"An error occurred: {e}")