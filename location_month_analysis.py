import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import streamlit as st

def accidents_by_tunnel_or_interchange_chart(df):
    """
    Create a bar chart showing the number of accidents by tunnel or interchange, grouped by month.
    Use the half_year_number column to dynamically determine the last half-year cycle.
    Place the average on the leftmost side of the chart and add data labels for each column.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'date', 'tunnel_or_interchange_number',
                         and 'half_year_number' columns.

    Returns:
    - None. Displays a grouped bar chart in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        required_columns = ['date', 'tunnel_or_interchange_number', 'half_year_number']
        if not all(col in df.columns for col in required_columns):
            st.error("The dataset must contain 'date', 'tunnel_or_interchange_number', and 'half_year_number' columns.")
            return

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Extract month-year for grouping
        df['month_year'] = df['date'].dt.to_period('M')

        # Get the maximum half_year_number to determine the current half-year
        current_half_year = df['half_year_number'].max()

        # Identify rows from the last half-year
        last_half_year_df = df[df['half_year_number'] == current_half_year]

        # Identify rows from all previous half-years
        pre_half_year_df = df[df['half_year_number'] < current_half_year]

        # Group by month-year and tunnel or interchange to count accidents
        last_half_year_counts = last_half_year_df.groupby(['month_year', 'tunnel_or_interchange_number']).size().unstack(fill_value=0)
        pre_half_year_counts = pre_half_year_df.groupby(['tunnel_or_interchange_number']).size()

        # Calculate the average for previous half-years
        pre_half_year_avg = pre_half_year_counts / pre_half_year_df['half_year_number'].nunique()

        # Create a new DataFrame for plotting
        plot_data = last_half_year_counts.copy()
        plot_data.loc['Avg. Sept 22 - June 24'] = pre_half_year_avg

        # Reorder the index to ensure the average is the first row
        plot_data = plot_data.sort_index(key=lambda x: x == 'Avg. Sept 22 - June 24', ascending=False)

        # Convert the month-year index to strings formatted as "Jan-24"
        plot_data.index = plot_data.index.astype(str)

        # Configure Matplotlib
        rcParams['font.family'] = 'Arial'

        # Plot the grouped bar chart
        ax = plot_data.plot(
            kind='bar',
            figsize=(16, 8),
            edgecolor='black',
            colormap='tab10',
            width=0.8
        )

        # Add data labels on top of each bar
        for container in ax.containers:
            for bar in container:
                height = bar.get_height()
                if height > 0:  # Only label bars with height greater than 0
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        height,
                        f'{height:.1f}' if height % 1 else f'{int(height)}',
                        ha='center',
                        va='bottom',
                        fontsize=8
                    )

        # Add titles, labels, and legend
        plt.title('תאונות דרכים - מנהרות ומחלפים לפי חודש', fontsize=14)
        plt.xlabel('חודש', fontsize=12)
        plt.ylabel('כמות התאונות', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(title='מנהרה או מחלף', fontsize=10, title_fontsize=12)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)

    except Exception as e:
        st.error(f"An error occurred: {e}")