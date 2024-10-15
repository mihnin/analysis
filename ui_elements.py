import streamlit as st
import pandas as pd
import data_processing as dp
import db_operations as dbo

def upload_historical_data():
    st.header("Загрузка исторических данных")
    historical_file = st.file_uploader("Выберите Excel файл с историческими данными", type=["xlsx"], key="historical_uploader")

    if historical_file is not None:
        st.session_state.historical_df = pd.read_excel(historical_file)
        st.success("Файл с историческими данными успешно загружен!")

    if st.session_state.historical_df is not None:
        st.write("Первые несколько строк загруженных исторических данных:")
        st.write(st.session_state.historical_df.head())

def upload_forecast_data():
    st.header("Загрузка прогнозируемых данных")
    forecast_file = st.file_uploader("Выберите Excel файл с прогнозируемыми данными", type=["xlsx"], key="forecast_uploader")

    if forecast_file is not None:
        st.session_state.forecast_df = pd.read_excel(forecast_file)
        st.success("Файл с прогнозируемыми данными успешно загружен!")

    if st.session_state.forecast_df is not None:
        st.write("Первые несколько строк загруженных прогнозных данных:")
        st.write(st.session_state.forecast_df.head())