import zipfile
import os
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap

# Путь к архиву
archive_path = ""C:\Users\bekzh\Desktop\дипломка\agroclim_N_C_E.zip

# Распаковываем архив
with zipfile.ZipFile(archive_path, 'r') as zip_ref:
    # Список всех файлов в архиве
    zip_ref.printdir()

    # Извлекаем все файлы
    zip_ref.extractall("extracted_files")  # Здесь файлы будут извлечены в папку "extracted_files"

# Предположим, что один из файлов - это CSV
csv_file_path = os.path.join("extracted_files", "your_data.csv")

# Загружаем CSV в DataFrame
df = pd.read_csv(csv_file_path)

# Отображаем данные в Streamlit
st.write(df)

# Создаем карту с тепловой картой
st.title("Heatmap")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(center=[40, -100], zoom=4)
        m.add_heatmap(
            csv_file_path,
            latitude="latitude",
            longitude="longitude",
            value="pop_max",
            name="Heat map",
            radius=20,
        )
m.to_streamlit(height=700)
