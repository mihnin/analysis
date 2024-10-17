import psycopg2
import streamlit as st
import config

def get_db_connection():
    return config.connect_to_db()

def load_historical_data_to_db(data):
    connection = get_db_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        # Ваш код для загрузки данных в базу данных
        cursor.close()
        connection.commit()
    except Exception as e:
        st.error(f"Произошла ошибка при загрузке исторических данных в базу данных: {str(e)}")
    finally:
        if connection is not None:
            connection.close()
