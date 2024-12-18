import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

def plot_coordinates_on_map_folium(df):
    """
    Plot accident coordinates on an interactive map using Streamlit and Folium.

    Parameters:
    - df (pd.DataFrame): DataFrame containing a 'coordinates' column with latitude and longitude.

    Returns:
    - None. Displays an interactive map in the Streamlit app.
    """
    try:
        # Ensure the 'coordinates' column exists
        if 'coordinates' not in df.columns:
            st.error("The dataset must contain a 'coordinates' column.")
            return

        # Extract latitude and longitude from the 'coordinates' column
        def parse_coordinates(coord):
            match = re.match(r'^\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)\s*$', str(coord))
            if match:
                return float(match.group(1)), float(match.group(2))
            return None, None

        df['latitude'], df['longitude'] = zip(*df['coordinates'].apply(parse_coordinates))

        # Drop rows with invalid coordinates
        df = df.dropna(subset=['latitude', 'longitude'])

        if df.empty:
            st.warning("No valid coordinates found in the dataset.")
            return

        # Calculate the center of the map based on the coordinates
        map_center = [df['latitude'].mean(), df['longitude'].mean()]

        # Create a Folium map
        m = folium.Map(location=map_center, zoom_start=12)

        # Add markers to the map for each coordinate
        for _, row in df.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"Location: {row['coordinates']}",
                tooltip="Click for details"
            ).add_to(m)

        # Display the map in Streamlit
        st.write("### Accident Locations Map")
        st_folium(m, width=700, height=500)

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Example Streamlit usage
if __name__ == "__main__":
    st.title("Interactive Accident Location Map")

    # Example DataFrame upload
    uploaded_file = st.file_uploader("Upload a CSV or Excel file containing accident data", type=["csv", "xlsx"])
    if uploaded_file:
        # Read file into DataFrame
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Call the plotting function
        plot_coordinates_on_map(df)