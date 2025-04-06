import streamlit as st
import zipfile
import os
import tempfile
import geopandas as gpd
import folium
from io import BytesIO
import matplotlib.pyplot as plt

def setup():
    st.set_page_config(layout="wide", page_title="Satellite imagery", page_icon='🛰️')
    st.header("🛰️Satellite Imagery")

def main():
    setup()

    row0_col1, row0_col2, row0_col3, row0_col4, row0_col5 = st.columns([1, 1, 1, 1, 1])
    row1_col1, row1_col2 = st.columns([5, 1])
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])

    # Create a map with folium
    m = folium.Map(location=[48.0196, 66.9237], zoom_start=5)

    st.sidebar.markdown("<h3 style='text-align: center; color: grey;'>OR</h3>", unsafe_allow_html=True)

    # Upload a zipped shapefile
    uploaded_shp_file = st.sidebar.file_uploader("Upload a Zipped Shapefile", type=["zip"])

    if uploaded_shp_file is not None:
        # Extract the zip file
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(uploaded_shp_file, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # Find the shapefile within the extracted files
            shapefile_path = None
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    if file.endswith(".shp"):
                        shapefile_path = os.path.join(root, file)
                        break

            if shapefile_path:
                # Read the shapefile into a GeoDataFrame
                gdf = gpd.read_file(shapefile_path)

                # Create the plot
                fig, ax = plt.subplots()
                gdf.plot(ax=ax)
                plt.xticks(rotation=90, fontsize=7)
                plt.yticks(fontsize=7)

                # Save the plot to a BytesIO object
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)

                # Display the plot in Streamlit
                with row2_col1:
                    st.image(buf, caption='Geopandas Plot')
            else:
                st.error("Shapefile (.shp) not found in the uploaded zip file.")

            # If the GeoDataFrame is not empty, add the shapefile to the map
            if not gdf.empty:
                # Add the GeoDataFrame as a layer to the map
                folium.GeoJson(gdf).add_to(m)

    with row1_col1:
        # Display the folium map using streamlit_folium
        from streamlit_folium import st_folium
        st_folium(m, width=700, height=600)

if __name__ == "__main__":
    main()
