# Опциональный импорт streamlit (только для web версии)
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    # Заглушка для desktop версии
    class st:
        @staticmethod
        def columns(*args, **kwargs):
            return [None] * (args[0] if args else 1)
        @staticmethod
        def selectbox(*args, **kwargs):
            return kwargs.get('index', 0) if 'options' in kwargs else None
import pandas as pd
from src.utils import data_processing as dp
import db_operations as dbo

import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

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