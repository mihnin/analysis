"""
Модуль моделей прогнозирования для управления запасами
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# МЕТРИКИ КАЧЕСТВА ПРОГНОЗА
# ============================================================================

def calculate_metrics(actual, predicted):
    """
    Рассчитывает метрики качества прогноза

    Returns:
    --------
    dict: MAPE, MAE, RMSE, Bias
    """
    actual = np.array(actual)
    predicted = np.array(predicted)

    # Удаляем нулевые значения для MAPE (деление на ноль)
    mask = actual != 0

    # MAPE (Mean Absolute Percentage Error) - средняя абсолютная процентная ошибка
    mape = np.mean(np.abs((actual[mask] - predicted[mask]) / actual[mask])) * 100 if mask.sum() > 0 else np.nan

    # MAE (Mean Absolute Error) - средняя абсолютная ошибка
    mae = np.mean(np.abs(actual - predicted))

    # RMSE (Root Mean Square Error) - корень из средней квадратичной ошибки
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    # Bias - систематическое смещение (положительное = перепрогноз, отрицательное = недопрогноз)
    bias = np.mean(predicted - actual)

    return {
        'MAPE': mape,
        'MAE': mae,
        'RMSE': rmse,
        'Bias': bias
    }


# ============================================================================
# МОДЕЛЬ 1: NAIVE FORECAST (Наивный прогноз)
# ============================================================================

def naive_forecast(series, horizon=1):
    """
    Наивный прогноз: прогноз = последнее наблюдение

    Parameters:
    -----------
    series : array-like
        Временной ряд
    horizon : int
        Горизонт прогнозирования (количество периодов вперед)

    Returns:
    --------
    array: Прогноз
    """
    last_value = series.iloc[-1] if isinstance(series, pd.Series) else series[-1]
    forecast = np.full(horizon, last_value)

    return forecast


# ============================================================================
# МОДЕЛЬ 2: MOVING AVERAGE (Скользящее среднее)
# ============================================================================

def moving_average_forecast(series, window=3, horizon=1):
    """
    Прогноз на основе скользящего среднего

    Parameters:
    -----------
    series : array-like
        Временной ряд
    window : int
        Размер окна для скользящего среднего
    horizon : int
        Горизонт прогнозирования

    Returns:
    --------
    array: Прогноз
    """
    if len(series) < window:
        window = len(series)

    # Берем среднее за последние window периодов
    ma_value = series.iloc[-window:].mean() if isinstance(series, pd.Series) else np.mean(series[-window:])
    forecast = np.full(horizon, ma_value)

    return forecast


# ============================================================================
# МОДЕЛЬ 3: EXPONENTIAL SMOOTHING (Экспоненциальное сглаживание)
# ============================================================================

def exponential_smoothing_forecast(series, alpha=0.3, horizon=1):
    """
    Simple Exponential Smoothing

    Parameters:
    -----------
    series : array-like
        Временной ряд
    alpha : float
        Параметр сглаживания (0 < alpha < 1)
        Чем выше alpha, тем больше вес у свежих наблюдений
    horizon : int
        Горизонт прогнозирования

    Returns:
    --------
    array: Прогноз
    """
    try:
        model = ExponentialSmoothing(series, trend=None, seasonal=None)
        fitted_model = model.fit(smoothing_level=alpha, optimized=False)
        forecast = fitted_model.forecast(steps=horizon)
        return forecast.values if isinstance(forecast, pd.Series) else forecast
    except:
        # Fallback на moving average если не получилось
        return moving_average_forecast(series, window=3, horizon=horizon)


# ============================================================================
# МОДЕЛЬ 4: HOLT-WINTERS (Тройное экспоненциальное сглаживание)
# ============================================================================

def holt_winters_forecast(series, horizon=1, seasonal_periods=12, trend='add', seasonal='add'):
    """
    Holt-Winters Triple Exponential Smoothing
    Учитывает тренд и сезонность

    Parameters:
    -----------
    series : array-like
        Временной ряд
    horizon : int
        Горизонт прогнозирования
    seasonal_periods : int
        Длина сезонного цикла (12 для месячных данных)
    trend : str
        'add' (аддитивный) или 'mul' (мультипликативный) или None
    seasonal : str
        'add' (аддитивный) или 'mul' (мультипликативный) или None

    Returns:
    --------
    array: Прогноз
    """
    try:
        # Проверяем что данных достаточно
        if len(series) < 2 * seasonal_periods:
            # Недостаточно данных для сезонности, используем только тренд
            seasonal = None

        # Проверяем наличие отрицательных значений для мультипликативной модели
        if (series <= 0).any():
            if seasonal == 'mul':
                seasonal = 'add'
            if trend == 'mul':
                trend = 'add'

        model = ExponentialSmoothing(
            series,
            trend=trend,
            seasonal=seasonal,
            seasonal_periods=seasonal_periods if seasonal else None
        )

        fitted_model = model.fit()
        forecast = fitted_model.forecast(steps=horizon)

        return forecast.values if isinstance(forecast, pd.Series) else forecast

    except Exception as e:
        # Fallback: пробуем без сезонности
        try:
            model = ExponentialSmoothing(series, trend='add', seasonal=None)
            fitted_model = model.fit()
            forecast = fitted_model.forecast(steps=horizon)
            return forecast.values if isinstance(forecast, pd.Series) else forecast
        except:
            # Fallback на moving average
            return moving_average_forecast(series, window=3, horizon=horizon)


# ============================================================================
# МОДЕЛЬ 5: SARIMA (Seasonal ARIMA)
# ============================================================================

def sarima_forecast(series, horizon=1, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
    """
    SARIMA (Seasonal AutoRegressive Integrated Moving Average)
    Самая продвинутая модель

    Parameters:
    -----------
    series : array-like
        Временной ряд
    horizon : int
        Горизонт прогнозирования
    order : tuple
        (p, d, q) параметры ARIMA
    seasonal_order : tuple
        (P, D, Q, s) сезонные параметры

    Returns:
    --------
    array: Прогноз
    """
    try:
        # Проверяем что данных достаточно
        min_obs = max(order[0] + order[2] + seasonal_order[0] + seasonal_order[2] + seasonal_order[3], 20)
        if len(series) < min_obs:
            # Слишком мало данных для SARIMA
            return holt_winters_forecast(series, horizon)

        model = SARIMAX(
            series,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        fitted_model = model.fit(disp=False, maxiter=50)
        forecast = fitted_model.forecast(steps=horizon)

        return forecast.values if isinstance(forecast, pd.Series) else forecast

    except:
        # Fallback на Holt-Winters
        return holt_winters_forecast(series, horizon)


# ============================================================================
# АВТОМАТИЧЕСКИЙ ВЫБОР ЛУЧШЕЙ МОДЕЛИ
# ============================================================================

def auto_select_best_model(series, test_size=3, seasonal_periods=12):
    """
    Автоматически выбирает лучшую модель на основе кросс-валидации

    Parameters:
    -----------
    series : array-like
        Временной ряд
    test_size : int
        Количество последних наблюдений для тестирования
    seasonal_periods : int
        Длина сезонного цикла

    Returns:
    --------
    tuple: (best_model_name, metrics_dict)
    """
    if len(series) < test_size + 5:
        # Слишком мало данных для валидации
        return 'moving_average', {}

    # Разделяем на train/test
    train = series.iloc[:-test_size] if isinstance(series, pd.Series) else series[:-test_size]
    test = series.iloc[-test_size:] if isinstance(series, pd.Series) else series[-test_size:]

    models = {}

    # Тестируем модели
    try:
        # Naive
        pred = naive_forecast(train, horizon=test_size)
        models['naive'] = calculate_metrics(test, pred)
    except:
        pass

    try:
        # Moving Average
        pred = moving_average_forecast(train, window=3, horizon=test_size)
        models['moving_average'] = calculate_metrics(test, pred)
    except:
        pass

    try:
        # Exponential Smoothing
        pred = exponential_smoothing_forecast(train, alpha=0.3, horizon=test_size)
        models['exponential_smoothing'] = calculate_metrics(test, pred)
    except:
        pass

    try:
        # Holt-Winters
        pred = holt_winters_forecast(train, horizon=test_size, seasonal_periods=seasonal_periods)
        models['holt_winters'] = calculate_metrics(test, pred)
    except:
        pass

    # Выбираем модель с наименьшим MAPE
    if models:
        best_model = min(models.items(), key=lambda x: x[1]['MAPE'] if not np.isnan(x[1]['MAPE']) else float('inf'))
        return best_model[0], models
    else:
        return 'moving_average', {}


# ============================================================================
# ЕДИНАЯ ФУНКЦИЯ ПРОГНОЗИРОВАНИЯ
# ============================================================================

def forecast_demand(series, horizon=1, model='auto', seasonal_periods=12, **kwargs):
    """
    Универсальная функция прогнозирования спроса

    Parameters:
    -----------
    series : array-like or pd.Series
        Исторический временной ряд
    horizon : int
        Горизонт прогнозирования (сколько периодов вперед)
    model : str
        Модель: 'auto', 'naive', 'moving_average', 'exponential_smoothing',
                'holt_winters', 'sarima'
    seasonal_periods : int
        Длина сезонного цикла (12 для месячных данных)
    **kwargs : dict
        Дополнительные параметры для моделей

    Returns:
    --------
    dict: {
        'forecast': array,
        'model_used': str,
        'metrics': dict (если model='auto')
    }
    """
    if not isinstance(series, pd.Series):
        series = pd.Series(series)

    result = {
        'forecast': None,
        'model_used': model,
        'metrics': {}
    }

    if model == 'auto':
        # Автоматический выбор лучшей модели
        best_model, metrics = auto_select_best_model(series, seasonal_periods=seasonal_periods)
        result['model_used'] = best_model
        result['metrics'] = metrics
        model = best_model

    # Применяем выбранную модель
    if model == 'naive':
        result['forecast'] = naive_forecast(series, horizon)

    elif model == 'moving_average':
        window = kwargs.get('window', 3)
        result['forecast'] = moving_average_forecast(series, window, horizon)

    elif model == 'exponential_smoothing':
        alpha = kwargs.get('alpha', 0.3)
        result['forecast'] = exponential_smoothing_forecast(series, alpha, horizon)

    elif model == 'holt_winters':
        trend = kwargs.get('trend', 'add')
        seasonal = kwargs.get('seasonal', 'add')
        result['forecast'] = holt_winters_forecast(
            series, horizon, seasonal_periods, trend, seasonal
        )

    elif model == 'sarima':
        order = kwargs.get('order', (1, 1, 1))
        seasonal_order = kwargs.get('seasonal_order', (1, 1, 1, seasonal_periods))
        result['forecast'] = sarima_forecast(series, horizon, order, seasonal_order)

    else:
        # Неизвестная модель - используем moving average
        result['forecast'] = moving_average_forecast(series, window=3, horizon=horizon)
        result['model_used'] = 'moving_average'

    return result


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def get_model_description(model_name):
    """Возвращает описание модели"""
    descriptions = {
        'naive': 'Наивный прогноз: последнее значение',
        'moving_average': 'Скользящее среднее за 3 периода',
        'exponential_smoothing': 'Экспоненциальное сглаживание',
        'holt_winters': 'Holt-Winters (тренд + сезонность)',
        'sarima': 'SARIMA (авторегрессионная модель)',
        'auto': 'Автоматический выбор лучшей модели'
    }
    return descriptions.get(model_name, 'Неизвестная модель')


def format_metrics(metrics):
    """Форматирует метрики для вывода"""
    if not metrics:
        return "Метрики недоступны"

    lines = []
    for model_name, model_metrics in metrics.items():
        lines.append(f"\n{model_name.upper()}:")
        lines.append(f"  MAPE: {model_metrics['MAPE']:.2f}%")
        lines.append(f"  MAE:  {model_metrics['MAE']:.2f}")
        lines.append(f"  RMSE: {model_metrics['RMSE']:.2f}")
        lines.append(f"  Bias: {model_metrics['Bias']:.2f}")

    return '\n'.join(lines)
