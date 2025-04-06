import streamlit as st
import leafmap.foliumap as leafmap
import zipfile
import os
import tempfile
import geopandas as gpd
import matplotlib.pyplot as plt
from io import BytesIO
import geemap

# Streamlit page configuration
st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.gishub.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")

st.sidebar.info(
    """
    Qiusheng Wu at [wetlands.io](https://wetlands.io) | [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://youtube.com/@giswqs) | [LinkedIn](https://www.linkedin.com/in/giswqs)
    """
)

st.title("Heatmap")

# File uploader for zipped shapefile
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
            st.image(buf, caption='Geopandas Plot')

            # Convert the GeoDataFrame to Earth Engine (if not empty)
            if not gdf.empty:
                roi = geemap.geopandas_to_ee(gdf)
                st.write("Region of Interest (ROI) in Earth Engine:", roi)
        else:
            st.error("Shapefile (.shp) not found in the uploaded zip file.")

# Leafmap heatmap example
with st.expander("See source code for heatmap"):
    with st.echo():
        filepath = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
        m = leafmap.Map(center=[40, -100], zoom=4)
        m.add_heatmap(
            filepath,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
m.to_streamlit(height=700)
