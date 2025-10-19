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


# ====================================================================
# НОВЫЕ ФУНКЦИИ ДЛЯ ОБРАБОТКИ РАЗНЫХ КОНВЕНЦИЙ СПИСАНИЯ
# ====================================================================

def detect_consumption_convention(df, consumption_column, start_column, end_column, arrival_column=None):
    """
    Автоматически определяет конвенцию списания:
    - POSITIVE: списание = положительное число (расход товара)
    - NEGATIVE: списание = отрицательное число (уменьшение запаса)

    Логика определения:
    1. Проверяем баланс: начало + приход - списание = конец
    2. Если баланс сходится с положительным списанием → POSITIVE
    3. Если баланс сходится с отрицательным списанием → NEGATIVE
    4. Если баланс не сходится → проверяем знак большинства значений
    """

    result = {
        'convention': None,
        'confidence': 0.0,
        'negative_count': 0,
        'positive_count': 0,
        'zero_count': 0,
        'balance_check_positive': 0,
        'balance_check_negative': 0,
        'recommendation': None
    }

    if consumption_column not in df.columns:
        result['recommendation'] = "Колонка списания не найдена"
        return result

    consumption = df[consumption_column]

    # Подсчет знаков
    result['negative_count'] = (consumption < 0).sum()
    result['positive_count'] = (consumption > 0).sum()
    result['zero_count'] = (consumption == 0).sum()

    total = len(consumption)
    negative_pct = result['negative_count'] / total * 100 if total > 0 else 0
    positive_pct = result['positive_count'] / total * 100 if total > 0 else 0

    # Проверка баланса если есть все необходимые колонки
    if arrival_column and arrival_column in df.columns:
        # Баланс: начало + приход - списание = конец

        # Тест 1: списание как положительное число
        calculated_end_pos = df[start_column] + df[arrival_column] - df[consumption_column]
        balance_pos = np.abs(calculated_end_pos - df[end_column]) < 0.01
        result['balance_check_positive'] = balance_pos.sum()

        # Тест 2: списание как отрицательное число (нужно ПРИБАВИТЬ)
        calculated_end_neg = df[start_column] + df[arrival_column] + df[consumption_column]  # + потому что consumption уже отрицательное
        balance_neg = np.abs(calculated_end_neg - df[end_column]) < 0.01
        result['balance_check_negative'] = balance_neg.sum()

        # Определяем конвенцию по балансу
        if result['balance_check_positive'] > result['balance_check_negative']:
            result['convention'] = 'POSITIVE'
            result['confidence'] = result['balance_check_positive'] / total * 100
            result['recommendation'] = f"Списание как ПОЛОЖИТЕЛЬНОЕ число (баланс сходится в {result['confidence']:.1f}% случаев)"
        elif result['balance_check_negative'] > result['balance_check_positive']:
            result['convention'] = 'NEGATIVE'
            result['confidence'] = result['balance_check_negative'] / total * 100
            result['recommendation'] = f"Списание как ОТРИЦАТЕЛЬНОЕ число (баланс сходится в {result['confidence']:.1f}% случаев)"
        else:
            # Баланс не помог, используем знак большинства
            result['convention'] = 'AMBIGUOUS'
            result['confidence'] = 50.0
            result['recommendation'] = "Не удалось определить конвенцию по балансу"

    # Если нет колонки прихода или баланс не помог, смотрим на знак большинства
    if result['convention'] is None or result['convention'] == 'AMBIGUOUS':
        if negative_pct > 80:
            result['convention'] = 'NEGATIVE'
            result['confidence'] = negative_pct
            result['recommendation'] = f"Списание как ОТРИЦАТЕЛЬНОЕ число ({negative_pct:.1f}% значений отрицательные)"
        elif positive_pct > 80:
            result['convention'] = 'POSITIVE'
            result['confidence'] = positive_pct
            result['recommendation'] = f"Списание как ПОЛОЖИТЕЛЬНОЕ число ({positive_pct:.1f}% значений положительные)"
        elif negative_pct > 50:
            result['convention'] = 'MOSTLY_NEGATIVE'
            result['confidence'] = negative_pct
            result['recommendation'] = f"Преимущественно ОТРИЦАТЕЛЬНОЕ ({negative_pct:.1f}% отрицательных)"
        elif positive_pct > 50:
            result['convention'] = 'MOSTLY_POSITIVE'
            result['confidence'] = positive_pct
            result['recommendation'] = f"Преимущественно ПОЛОЖИТЕЛЬНОЕ ({positive_pct:.1f}% положительных)"
        else:
            result['convention'] = 'MIXED'
            result['confidence'] = 0.0
            result['recommendation'] = f"СМЕШАННЫЕ данные: {positive_pct:.1f}% положительных, {negative_pct:.1f}% отрицательных"

    return result


def normalize_consumption(df, consumption_column, convention='AUTO', start_column=None, end_column=None, arrival_column=None):
    """
    Нормализует колонку списания к единой конвенции:
    - ВСЕГДА возвращает ПОЛОЖИТЕЛЬНЫЕ значения (расход = положительное число)

    Parameters:
    -----------
    convention : str
        'AUTO' - автоматическое определение
        'POSITIVE' - данные уже в правильном формате
        'NEGATIVE' - данные в отрицательном формате, нужно инвертировать
        'ABS' - просто взять модуль всех значений
    """

    if consumption_column not in df.columns:
        raise ValueError(f"Колонка '{consumption_column}' не найдена в данных")

    df_normalized = df.copy()

    if convention == 'AUTO':
        # Автоматическое определение
        detection = detect_consumption_convention(df, consumption_column, start_column, end_column, arrival_column)

        if detection['convention'] in ['NEGATIVE', 'MOSTLY_NEGATIVE']:
            # Инвертируем отрицательные значения
            df_normalized[consumption_column] = df_normalized[consumption_column].abs()
            return df_normalized, detection
        elif detection['convention'] in ['POSITIVE', 'MOSTLY_POSITIVE']:
            # Уже в правильном формате, но применим abs для безопасности
            df_normalized[consumption_column] = df_normalized[consumption_column].abs()
            return df_normalized, detection
        elif detection['convention'] == 'MIXED':
            # Смешанные данные - берем модуль
            df_normalized[consumption_column] = df_normalized[consumption_column].abs()
            detection['recommendation'] += " → Применен модуль ко всем значениям"
            return df_normalized, detection
        else:
            # Не удалось определить - берем модуль
            df_normalized[consumption_column] = df_normalized[consumption_column].abs()
            detection['recommendation'] = "Конвенция неясна → Применен модуль"
            return df_normalized, detection

    elif convention == 'NEGATIVE':
        # Принудительная инверсия
        df_normalized[consumption_column] = df_normalized[consumption_column].abs()
        detection = {'convention': 'NEGATIVE', 'recommendation': 'Принудительная инверсия (abs)', 'confidence': 100.0}
        return df_normalized, detection

    elif convention == 'POSITIVE':
        # Уже положительные, но на всякий случай применим abs к отрицательным
        df_normalized[consumption_column] = df_normalized[consumption_column].abs()
        detection = {'convention': 'POSITIVE', 'recommendation': 'Применен abs для безопасности', 'confidence': 100.0}
        return df_normalized, detection

    elif convention == 'ABS':
        # Просто модуль
        df_normalized[consumption_column] = df_normalized[consumption_column].abs()
        detection = {'convention': 'ABS', 'recommendation': 'Применен модуль ко всем значениям', 'confidence': 100.0}
        return df_normalized, detection

    else:
        raise ValueError(f"Неизвестная конвенция: {convention}")


def validate_balance(df, date_column, material_column, branch_column,
                     start_column, end_column, arrival_column, consumption_column):
    """
    Проверяет баланс: начало + приход - списание = конец
    Возвращает отчет о проблемах
    """

    df_check = df.copy()
    df_check[date_column] = pd.to_datetime(df_check[date_column])

    # Расчет ожидаемого конца
    df_check['calculated_end'] = (df_check[start_column] +
                                   df_check[arrival_column] -
                                   df_check[consumption_column])

    # Разница
    df_check['balance_diff'] = df_check['calculated_end'] - df_check[end_column]

    # Проблемные строки (разница > 0.01)
    problems = df_check[np.abs(df_check['balance_diff']) > 0.01].copy()

    report = {
        'total_rows': len(df_check),
        'problems_count': len(problems),
        'problems_percentage': len(problems) / len(df_check) * 100 if len(df_check) > 0 else 0,
        'max_difference': df_check['balance_diff'].abs().max(),
        'avg_difference': df_check['balance_diff'].abs().mean(),
        'problems': problems[[date_column, material_column, branch_column,
                             start_column, arrival_column, consumption_column,
                             end_column, 'calculated_end', 'balance_diff']] if len(problems) > 0 else pd.DataFrame()
    }

    return report


def print_consumption_analysis(df, consumption_column, start_column, end_column, arrival_column=None):
    """
    Печатает анализ колонки списания
    """
    detection = detect_consumption_convention(df, consumption_column, start_column, end_column, arrival_column)

    print("=" * 80)
    print("АНАЛИЗ КОЛОНКИ СПИСАНИЯ")
    print("=" * 80)

    print(f"\n📊 Статистика значений:")
    print(f"  Положительных: {detection['positive_count']} ({detection['positive_count']/len(df)*100:.1f}%)")
    print(f"  Отрицательных: {detection['negative_count']} ({detection['negative_count']/len(df)*100:.1f}%)")
    print(f"  Нулевых: {detection['zero_count']} ({detection['zero_count']/len(df)*100:.1f}%)")

    if arrival_column:
        print(f"\n⚖️  Проверка баланса:")
        print(f"  С положительным списанием: {detection['balance_check_positive']} строк сходится")
        print(f"  С отрицательным списанием: {detection['balance_check_negative']} строк сходится")

    print(f"\n🔍 Определенная конвенция: {detection['convention']}")
    print(f"   Уверенность: {detection['confidence']:.1f}%")
    print(f"   Рекомендация: {detection['recommendation']}")

    return detection