import zipfile
import os
import geopandas as gpd
import streamlit as st
import leafmap.foliumap as leafmap

# Путь к архиву
archive_path = "C:/Users/bekzh/Desktop/дипломка/agroclim_N_C_E.zip"

# Распаковываем архив
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    # Список всех файлов в архиве
    zip_ref.printdir()

    # Извлекаем все файлы
    zip_ref.extractall("extracted_files")  # Здесь файлы будут извлечены в папку "extracted_files"

# Проверяем содержимое извлеченной папки
extracted_files = os.listdir("extracted_files")
st.write("Извлеченные файлы:", extracted_files)

# Предположим, что шейп-файл называется "agroclim_data.shp"
shapefile_path = os.path.join("extracted_files", "agroclim_data.shp")

# Проверяем, существует ли шейп-файл
if os.path.exists(shapefile_path):
    # Загружаем шейп-файл с помощью geopandas
    gdf = gpd.read_file(shapefile_path)

    # Отображаем информацию о шейп-файле в Streamlit
    st.write(gdf)

    # Создаем карту с шейп-файлом
    st.title("Map with Shapefile Data")

    with st.expander("See source code"):
        with st.echo():
            # Создаем карту и добавляем шейп-файл
            m = leafmap.Map(center=[40, -100], zoom=4)
            m.add_gdf(gdf, layer_name="Shapefile Layer")

    m.to_streamlit(height=700)
else:
    st.error("Шейп-файл не найден в извлеченных данных.")
