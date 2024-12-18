import pandas as pd
import folium
from streamlit_folium import st_folium
import streamlit as st

def plot_accidents_on_map(df):
    """
    Plot accident locations on an interactive map using Folium.

    Parameters:
    - df (pd.DataFrame): DataFrame containing accident data with a 'coordinates' column.

    Returns:
    - None. Displays an interactive map in the Streamlit app.
    """
    try:
        # Ensure the coordinates column exists
        if 'coordinates' not in df.columns:
            st.error("The dataset must contain a 'coordinates' column in 'latitude, longitude' format.")
            return

        # Parse the coordinates column to extract latitude and longitude
        coordinates_split = df['coordinates'].str.split(',', expand=True)
        df['latitude'] = pd.to_numeric(coordinates_split[0], errors='coerce')
        df['longitude'] = pd.to_numeric(coordinates_split[1], errors='coerce')

        # Remove rows with invalid or missing coordinates
        valid_coords = df.dropna(subset=['latitude', 'longitude'])

        # Check if there are valid coordinates to plot
        if valid_coords.empty:
            st.error("No valid coordinates available to plot.")
            return

        # Create a map centered at the mean latitude and longitude
        avg_lat = valid_coords['latitude'].mean()
        avg_lon = valid_coords['longitude'].mean()
        accident_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=10)

        # Add markers for each accident
        for _, row in valid_coords.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Coordinates: {row['coordinates']}"
            ).add_to(accident_map)

        # Display the map in Streamlit
        st.write("### Accident Locations Map")
        st_folium(accident_map, width=800, height=500)

    except Exception as e:
        st.error(f"An error occurred: {e}")