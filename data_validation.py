import pandas as pd
import numpy as np

def validate_historical_data(df, date_column, branch_column, material_column, 
                             start_quantity_column, end_quantity_column, end_cost_column):
    """
    Проверяет корректность исторических данных.
    """
    errors = []

    # Проверка наличия всех необходимых столбцов
    required_columns = [date_column, branch_column, material_column, 
                        start_quantity_column, end_quantity_column, end_cost_column]
    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Отсутствует обязательный столбец: {column}")

    if not errors:
        # Проверка типов данных
        if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
            errors.append(f"Столбец {date_column} должен быть типа datetime")
        
        numeric_columns = [start_quantity_column, end_quantity_column, end_cost_column]
        for column in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                errors.append(f"Столбец {column} должен содержать числовые значения")

        # Проверка на отрицательные значения
        for column in numeric_columns:
            if (df[column] < 0).any():
                errors.append(f"Обнаружены отрицательные значения в столбце {column}")

        # Проверка на пропущенные значения
        for column in required_columns:
            if df[column].isnull().any():
                errors.append(f"Обнаружены пропущенные значения в столбце {column}")

        # Проверка логической корректности данных
        if (df[end_quantity_column] > df[start_quantity_column]).any():
            errors.append("Обнаружены случаи, где конечное количество больше начального")

        if (df[end_cost_column] / df[end_quantity_column] > 1000000).any():
            errors.append("Обнаружены подозрительно высокие значения стоимости единицы товара")

    return errors

def validate_forecast_data(df, date_column, branch_column, material_column, forecast_quantity_column):
    """
    Проверяет корректность прогнозных данных.
    """
    errors = []

    # Проверка наличия всех необходимых столбцов
    required_columns = [date_column, branch_column, material_column, forecast_quantity_column]
    for column in required_columns:
        if column not in df.columns:
            errors.append(f"Отсутствует обязательный столбец: {column}")

    if not errors:
        # Проверка типов данных
        if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
            errors.append(f"Столбец {date_column} должен быть типа datetime")
        
        if not pd.api.types.is_numeric_dtype(df[forecast_quantity_column]):
            errors.append(f"Столбец {forecast_quantity_column} должен содержать числовые значения")

        # Проверка на отрицательные значения
        if (df[forecast_quantity_column] < 0).any():
            errors.append(f"Обнаружены отрицательные значения в столбце {forecast_quantity_column}")

        # Проверка на пропущенные значения
        for column in required_columns:
            if df[column].isnull().any():
                errors.append(f"Обнаружены пропущенные значения в столбце {column}")

        # Проверка на будущие даты
        if (df[date_column] < pd.Timestamp.now()).any():
            errors.append("Обнаружены прошедшие даты в прогнозных данных")

    return errors

def validate_data(historical_df, forecast_df, historical_columns, forecast_columns):
    """
    Проверяет корректность исторических и прогнозных данных.
    """
    historical_errors = validate_historical_data(historical_df, *historical_columns)
    forecast_errors = validate_forecast_data(forecast_df, *forecast_columns)

    return historical_errors, forecast_errors