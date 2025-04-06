import streamlit as st
import zipfile
import os
import tempfile
import geopandas as gpd
import leafmap.foliumap as leafmap
from streamlit_folium import st_folium

# Настройка страницы Streamlit
st.set_page_config(layout="wide")

# Информация в боковой панели
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

st.title("Interactive Map with Heatmap")

# Изначально показываем карту с центром на Казахстане
m = leafmap.Map(center=[48.0196, 66.9237], zoom=5)
st_folium(m, width=700)


# Функция загрузки архива с шейп-файлами
uploaded_shp_file = st.sidebar.file_uploader("Upload a Zipped Shapefile", type=["zip"])

if uploaded_shp_file is not None:
    # Распаковываем архив
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(uploaded_shp_file, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        # Ищем шейп-файлы (.shp)
        shapefile_path = None
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".shp"):
                    shapefile_path = os.path.join(root, file)
                    break

        if shapefile_path:
            # Загружаем шейп-файл с помощью geopandas
            gdf = gpd.read_file(shapefile_path)

            # Отображаем обновленную карту
            st.subheader("Map with Shapefile Data")
            st_folium(m, width=700)

            # Отображаем данные о шейп-файле в Streamlit
            st.write("Data from Shapefile:")
            st.write(gdf)

            # Обновляем карту с шейп-файлом на Казахстане
            m.add_gdf(gdf, layer_name="Shapefile Layer")

        else:
            st.error("Шейп-файл (.shp) не найден в загруженном архиве.")
