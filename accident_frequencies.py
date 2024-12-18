import pandas as pd
import streamlit as st

def calculate_accident_frequencies_with_selection(df):

    """
    Calculate accident frequencies by hours and days for a selected half-year and compare it to data since the road opened.
    Uses the unique values from the 'half_year' column.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with 'half_year' and 'rounded_hour'.

    Returns:
    - None. Displays the table in the Streamlit app.
    """
    try:
        # Ensure required columns exist
        if 'half_year' not in df.columns or 'rounded_hour' not in df.columns:
            st.error("Columns 'half_year' and 'rounded_hour' must be present in the dataset.")
            return

        # Streamlit selection for comparison
        unique_half_years = df['half_year'].dropna().unique().tolist()
        selected_half_year = st.selectbox("Select Half-Year for Comparison", sorted(unique_half_years))

        # Filter for each period
        since_road_opening = df
        selected_period = df[df['half_year'] == selected_half_year]

        # Calculate hourly accident frequencies
        hourly_freq_opening = since_road_opening['rounded_hour'].value_counts().sort_index()
        hourly_freq_selected = selected_period['rounded_hour'].value_counts().sort_index()

        # Map days to Hebrew and calculate daily frequencies
        hebrew_days = {
            "Sunday": "יום ראשון",
            "Monday": "יום שני",
            "Tuesday": "יום שלישי",
            "Wednesday": "יום רביעי",
            "Thursday": "יום חמישי",
            "Friday": "יום שישי",
            "Saturday": "שבת",
        }

        since_road_opening['day_of_week'] = since_road_opening['date'].dt.day_name().map(hebrew_days)
        selected_period['day_of_week'] = selected_period['date'].dt.day_name().map(hebrew_days)

        daily_freq_opening = since_road_opening['day_of_week'].value_counts()
        daily_freq_selected = selected_period['day_of_week'].value_counts()

        # Reindex to maintain day order in Hebrew
        day_order = list(hebrew_days.values())
        daily_freq_opening = daily_freq_opening.reindex(day_order, fill_value=0)
        daily_freq_selected = daily_freq_selected.reindex(day_order, fill_value=0)

        # Combine results into tables
        hourly_comparison = pd.DataFrame({
            'Since Road Opening': hourly_freq_opening,
            selected_half_year: hourly_freq_selected
        }).fillna(0).astype(int)

        daily_comparison = pd.DataFrame({
            'Since Road Opening': daily_freq_opening,
            selected_half_year: daily_freq_selected
        }).fillna(0).astype(int)

        # Display results in Streamlit
        st.write("### Table 1: Accident Frequencies by Hour")
        st.table(hourly_comparison)

        st.write("### Table 2: Accident Frequencies by Day of Week")
        st.table(daily_comparison)

    except Exception as e:
        st.error(f"An error occurred: {e}")
