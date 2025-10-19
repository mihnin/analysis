# -*- coding: utf-8 -*-
"""
Скрипт для создания правильных шаблонов данных для приложения
"""
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("СОЗДАНИЕ ШАБЛОНОВ ДАННЫХ ДЛЯ ПРИЛОЖЕНИЯ")
print("=" * 80)
print()

# ============================================================================
# 1. ИСТОРИЧЕСКИЕ ДАННЫЕ
# ============================================================================
print("1. Создание файла исторических данных...")

# Генерация данных за 2021-2023 (36 месяцев)
dates = pd.date_range('2021-01-01', '2023-12-31', freq='MS')
materials = ['Материал A', 'Материал B', 'Материал C', 'Материал D', 'Материал E']
branches = ['Москва', 'Санкт-Петербург', 'Новосибирск']

historical_data = []

for material in materials:
    for branch in branches:
        # Базовое потребление для каждого материала
        base_consumption = np.random.randint(80, 150)

        # Начальный остаток
        prev_end_balance = np.random.randint(300, 500)

        for i, date in enumerate(dates):
            # Сезонность (синусоида с периодом 12 месяцев)
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * i / 12)

            # Тренд роста
            trend_factor = 1 + (i * 0.01)

            # Случайный шум
            noise = np.random.uniform(0.8, 1.2)

            # Рассчитываем потребление
            consumption = base_consumption * seasonal_factor * trend_factor * noise
            consumption = round(max(0, consumption), 2)

            # Начальный остаток = конечный остаток предыдущего периода
            start_balance = prev_end_balance

            # Конечный остаток = начальный - потребление + поставка (случайная)
            delivery = np.random.randint(0, 200) if np.random.random() > 0.5 else 0
            end_balance = start_balance - consumption + delivery
            end_balance = round(max(0, end_balance), 2)

            # Стоимость (цена за единицу * остаток)
            unit_price = np.random.uniform(40, 70)
            end_cost = round(end_balance * unit_price, 2)

            historical_data.append({
                'Дата': date,
                'Филиал': branch,
                'Материал': material,
                'Начальный остаток': start_balance,
                'Конечный остаток': end_balance,
                'Потребление': consumption,
                'Стоимость конечная': end_cost
            })

            # Запомним конечный остаток для следующего периода
            prev_end_balance = end_balance

df_historical = pd.DataFrame(historical_data)

# Сохранение
output_file = 'c:/dev/analysis/datasets/historical_data_template.xlsx'
df_historical.to_excel(output_file, index=False)

print(f"   Файл создан: {output_file}")
print(f"   Строк: {len(df_historical)}")
print(f"   Колонок: {len(df_historical.columns)}")
print(f"   Период: {df_historical['Дата'].min().date()} - {df_historical['Дата'].max().date()}")
print()
print("   Обязательные колонки:")
print("   - Дата")
print("   - Материал")
print("   - Начальный остаток")
print("   - Конечный остаток")
print()
print("   Рекомендуемые колонки:")
print("   - Филиал")
print("   - Потребление")
print("   - Стоимость конечная")
print()

# Показать первые строки
print("   Первые 5 строк:")
print(df_historical.head().to_string())
print()
print()

# ============================================================================
# 2. ПРОГНОЗНЫЕ ДАННЫЕ
# ============================================================================
print("2. Создание файла прогнозных данных...")

# Генерация данных на 2024 год (12 месяцев)
forecast_dates = pd.date_range('2024-01-01', '2024-12-31', freq='MS')

forecast_data = []

for material in materials:
    for branch in branches:
        # Базовый плановый спрос (чуть выше среднего исторического)
        base_demand = np.random.randint(100, 180)

        for i, date in enumerate(forecast_dates):
            # Сезонность
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * i / 12)

            # Тренд
            trend_factor = 1.1  # Рост на 10% от базы

            # Плановый спрос
            planned_demand = base_demand * seasonal_factor * trend_factor
            planned_demand = round(max(0, planned_demand), 2)

            forecast_data.append({
                'Дата': date,
                'Филиал': branch,
                'Материал': material,
                'Плановый спрос': planned_demand
            })

df_forecast = pd.DataFrame(forecast_data)

# Сохранение
output_file_forecast = 'c:/dev/analysis/datasets/forecast_data_template.xlsx'
df_forecast.to_excel(output_file_forecast, index=False)

print(f"   Файл создан: {output_file_forecast}")
print(f"   Строк: {len(df_forecast)}")
print(f"   Колонок: {len(df_forecast.columns)}")
print(f"   Период: {df_forecast['Дата'].min().date()} - {df_forecast['Дата'].max().date()}")
print()
print("   Обязательные колонки:")
print("   - Дата")
print("   - Материал")
print("   - Плановый спрос")
print()
print("   Рекомендуемые колонки:")
print("   - Филиал")
print()

# Показать первые строки
print("   Первые 5 строк:")
print(df_forecast.head().to_string())
print()
print()

print("=" * 80)
print("ГОТОВО! Шаблоны созданы успешно")
print("=" * 80)
print()
print("ФАЙЛЫ:")
print(f"1. {output_file}")
print(f"2. {output_file_forecast}")
print()
print("Используйте эти файлы как шаблоны для ваших данных!")
