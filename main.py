import pandas as pd
import streamlit as st

# Import analysis functions
from column_editor import edit_column_names
from analysis import monthly_accident_analysis
from injury_analysis import analyze_injuries
from share_of_accidents_per_location import accidents_by_location_pie_chart
from map_playging_around import plot_accidents_on_map
from Accident_count_by_severity import monthly_accidents_by_severity
from injury_level_analysis import monthly_injuries_fatalities_chart
from location_month_analysis import accidents_by_tunnel_or_interchange_chart
from accident_trend_by_location import compare_accident_trends
from t4_scatterplot_graph_8 import t4_tunnel_scatter_plot
from t2_scatterplot_graph_9 import t2_tunnel_scatter_plot
from map_folium_test import plot_coordinates_on_map_folium

# Set Streamlit page configuration
st.set_page_config(
    page_title="Dashboard for Accident Analysis",
    layout="wide"  # Enables a wide layout
)

def main():
    # Title and Description

    st.title("לוח מחוונים לניתוח תאונות ונפגעים")
    st.sidebar.image(
        "logo.png",  # Path to your hard-coded logo file
        caption="סדנת התנועה בע״מ",
        use_column_width=True
    )
    st.sidebar.title("ניווט בלוח המחוונים")
    # Sidebar File Uploader
    uploaded_file = st.sidebar.file_uploader("העלה קובץ אקסל", type=["xlsx"])

    if uploaded_file is not None:
        st.sidebar.success("הקובץ נטען בהצלחה!")

        # Step 1: Load the uploaded file
        df = pd.read_excel(uploaded_file)

        # Step 2: Edit column names
        df = edit_column_names(df)

        # Navigation in Sidebar
        options = st.sidebar.radio(
            "בחר גרף לניתוח:",
            (
                "נתונים לאחר שינוי שמות עמודות",
                "ניתוח חודשי של תאונות",
                "ניתוח נתוני נפגעים",
                "תאונה לפי חומרה",
                "נפגעים לפי חומרה",
                "תאונות דרכים - מיקום וחודש",
                "מגמות חציוניות לפי מיקום",
                "תאונות במנהרות - לפי שעה ביממה (מנהרת T4)",
                "תאונות במנהרות - לפי שעה ביממה (מנהרת T2)",
                "יחס מיקומי תאונות - מפתיחת הכביש",
                "מפה אינטראקטיבית",
                "מפת Folium"
            )
        )
        st.sidebar.write(" ")
        st.sidebar.write("---")  # Adds a horizontal line for separation
        st.sidebar.text("Created by Jordan M. Zlatin")
        st.sidebar.text("jmzlatin@gmail.com")
        # Display DataFrame after renaming columns
        if options == "נתונים לאחר שינוי שמות עמודות":
            st.write("### נתונים לאחר שינוי שמות עמודות")
            st.dataframe(df.head())

        # Perform Monthly Accident Analysis
        elif options == "ניתוח חודשי של תאונות":
            st.write("## ניתוח חודשי של תאונות")
            st.write("Graph 1")
            monthly_accident_analysis(df)

        # Perform Injury Analysis
        elif options == "ניתוח נתוני נפגעים":
            st.write("## ניתוח נתוני נפגעים")
            st.write("Graph 2")
            analyze_injuries(df)

        # Accident Count by Severity
        elif options == "תאונה לפי חומרה":
            st.write("## תאונה לפי חומרה")
            st.write("Graph 3")
            monthly_accidents_by_severity(df)

        # Injuries by Severity
        elif options == "נפגעים לפי חומרה":
            st.write("## נפגעים לפי חומרה")
            st.write("Graph 5")
            monthly_injuries_fatalities_chart(df)

        # Accidents by Location and Month
        elif options == "תאונות דרכים - מיקום וחודש":
            st.write("## תאונות דרכים - מיקום וחודש")
            st.write("Graph 6")
            accidents_by_tunnel_or_interchange_chart(df)

        # Trends by Location
        elif options == "מגמות חציוניות לפי מיקום":
            st.write("## מגמות חציוניות לפי מיקום")
            st.write("Graph 7")
            compare_accident_trends(df)

        # Tunnel T4 Scatter Plot
        elif options == "תאונות במנהרות - לפי שעה ביממה (מנהרת T4)":
            st.write('## תאונות במנהרות - לפי שעה ביממה (מנהרת T4)')
            st.write("Graph 8")
            t4_tunnel_scatter_plot(df)

        # Tunnel T2 Scatter Plot
        elif options == "תאונות במנהרות - לפי שעה ביממה (מנהרת T2)":
            st.write('## תאונות במנהרות - לפי שעה ביממה (מנהרת T2)')
            st.write("Graph 9")
            t2_tunnel_scatter_plot(df)

        # Accident Locations Pie Chart
        elif options == "יחס מיקומי תאונות - מפתיחת הכביש":
            st.write('## יחס מיקומי תאונות - מפתיחת הכביש ')
            st.write("Graph 10")
            accidents_by_location_pie_chart(df)

        # Interactive Map with Map Playing
        elif options == "מפה אינטראקטיבית":
            st.write('## מפה אינטראקטיבית')
            plot_accidents_on_map(df)

        # Folium Map Test
        elif options == "מפת Folium":
            st.write("## מפת Folium")
            plot_coordinates_on_map_folium(df)

    else:
        st.sidebar.info("העלה קובץ כדי להמשיך")

if __name__ == "__main__":
    main()