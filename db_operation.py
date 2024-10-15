import psycopg2
import streamlit as st
import config

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="your_db_name",
            user="your_user",
            password="your_db_password",
            host="192.168.50.241",
            port=5432
        )
        return connection
    except Exception as e:
        st.error(f"Произошла ошибка при подключении к базе данных: {str(e)}")
        return None

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