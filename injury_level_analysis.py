import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import streamlit as st

def monthly_injuries_fatalities_chart(df):
    """
    Create a column chart showing the monthly number of minor injuries, serious injuries, and fatalities.
    Each category has its own column, and the values are displayed on top of each column.
    The last half-year is highlighted.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'date', 'minor_injuries', 'serious_injuries', and 'fatalities' columns.

    Returns:
    - None. Displays a column chart in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        required_columns = ['date', 'minor_injuries', 'serious_injuries', 'fatalities']
        if not all(col in df.columns for col in required_columns):
            st.error("The dataset must contain 'date', 'minor_injuries', 'serious_injuries', and 'fatalities' columns.")
            return

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Convert injury and fatality columns to numeric, replacing non-numeric values with NaN
        for col in ['minor_injuries', 'serious_injuries', 'fatalities']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Extract month-year for grouping
        df['month_year'] = df['date'].dt.to_period('M')

        # Group by month-year and sum injuries and fatalities
        injuries_fatalities_counts = df.groupby('month_year')[['minor_injuries', 'serious_injuries', 'fatalities']].sum()

        # Convert the month-year index to strings formatted as "Jan-24"
        injuries_fatalities_counts.index = injuries_fatalities_counts.index.strftime('%b-%y')

        # Configure Matplotlib
        rcParams['font.family'] = 'Arial'

  

        # Plot the column chart
        plt.figure(figsize=(16, 8))
        ax = injuries_fatalities_counts.plot(
            kind='bar',
            figsize=(16, 8),
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

        

        # Update legend
        plt.legend(['Minor Injuries', 'Serious Injuries', 'Fatalities'], title='Category', fontsize=10, title_fontsize=12)
        plt.title('Monthly Injuries and Fatalities', fontsize=14)
        plt.xlabel('Month-Year', fontsize=12)
        plt.ylabel('Number of People', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)

    except Exception as e:
        st.error(f"An error occurred: {e}")