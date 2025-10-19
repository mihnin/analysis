# -*- coding: utf-8 -*-
"""
Создание ПРАВИЛЬНОГО шаблона данных с логичной структурой

Начальный остаток + Поступление - Потребление = Конечный остаток
Конечный остаток × Цена за единицу = Конечная стоимость
"""
import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 80)
print("СОЗДАНИЕ ПРАВИЛЬНОГО ШАБЛОНА ДАННЫХ")
print("=" * 80)
print()

# Генерация данных за 2021-2023 (36 месяцев)
dates = pd.date_range('2021-01-01', '2023-12-31', freq='MS')
materials = ['Материал A', 'Материал B', 'Материал C', 'Материал D', 'Материал E']
branches = ['Москва', 'Санкт-Петербург', 'Новосибирск']

historical_data = []

for material in materials:
    for branch in branches:
        # Базовые параметры для материала
        base_consumption = np.random.randint(80, 150)
        base_delivery_freq = 0.6  # Вероятность поставки в месяц
        unit_price = np.random.uniform(40, 70)  # Цена за единицу

        # Начальный остаток в первом периоде
        prev_end_balance = np.random.randint(300, 500)

        for i, date in enumerate(dates):
            # === 1. Начальный остаток ===
            start_balance = prev_end_balance

            # === 2. Потребление (с сезонностью и трендом) ===
            # Сезонность (синусоида с периодом 12 месяцев)
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * i / 12)
            # Тренд роста
            trend_factor = 1 + (i * 0.01)
            # Случайный шум
            noise = np.random.uniform(0.8, 1.2)

            consumption = base_consumption * seasonal_factor * trend_factor * noise
            consumption = round(max(0, consumption), 2)

            # === 3. Поступление (доставки материалов) ===
            # Поставки происходят не каждый месяц
            if np.random.random() < base_delivery_freq:
                # Поставка примерно равна 1.5-2 месяцам потребления
                delivery = consumption * np.random.uniform(1.5, 2.5)
                delivery = round(delivery, 2)
            else:
                delivery = 0

            # === 4. Конечный остаток (БАЛАНСОВОЕ УРАВНЕНИЕ) ===
            end_balance = start_balance + delivery - consumption
            end_balance = round(max(0, end_balance), 2)

            # === 5. Цена за единицу (с небольшой инфляцией) ===
            # Инфляция 0.3% в месяц
            inflation_factor = 1 + (i * 0.003)
            current_unit_price = unit_price * inflation_factor
            current_unit_price = round(current_unit_price, 2)

            # === 6. Конечная стоимость (РАСЧЕТ) ===
            end_cost = end_balance * current_unit_price
            end_cost = round(end_cost, 2)

            historical_data.append({
                'Дата': date,
                'Филиал': branch,
                'Материал': material,
                'Начальный остаток': start_balance,
                'Поступление': delivery,
                'Потребление': consumption,
                'Конечный остаток': end_balance,
                'Цена за единицу': current_unit_price,
                'Конечная стоимость': end_cost
            })

            # Запомним конечный остаток для следующего периода
            prev_end_balance = end_balance

df_historical = pd.DataFrame(historical_data)

# Сохранение
output_file = 'c:/dev/analysis/datasets/historical_data_correct_template.xlsx'
df_historical.to_excel(output_file, index=False)

print(f"OK - Файл создан: {output_file}")
print(f"  Строк: {len(df_historical)}")
print(f"  Колонок: {len(df_historical.columns)}")
print(f"  Период: {df_historical['Дата'].min().date()} - {df_historical['Дата'].max().date()}")
print()
print("СТРУКТУРА (логичная и полная):")
print("=" * 80)
for i, col in enumerate(df_historical.columns, 1):
    print(f"  {i}. {col}")
print()
print("БАЛАНСОВОЕ УРАВНЕНИЕ:")
print("  Конечный остаток = Начальный остаток + Поступление - Потребление")
print()
print("РАСЧЕТ СТОИМОСТИ:")
print("  Конечная стоимость = Конечный остаток * Цена за единицу")
print()
print()

# Показать первые строки
print("Первые 5 строк:")
print("=" * 80)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df_historical.head().to_string())
print()
print()

# Проверка балансового уравнения
print("Проверка балансового уравнения (первые 3 строки):")
print("=" * 80)
for idx in range(min(3, len(df_historical))):
    row = df_historical.iloc[idx]
    calculated = row['Начальный остаток'] + row['Поступление'] - row['Потребление']
    actual = row['Конечный остаток']
    status = "OK" if abs(calculated - actual) < 0.01 else "ERR"
    print(f"{status} Строка {idx+1}: {row['Начальный остаток']:.2f} + {row['Поступление']:.2f} - {row['Потребление']:.2f} = {actual:.2f} (расчет: {calculated:.2f})")

print()
print("=" * 80)
print("ГОТОВО! Шаблон с правильной структурой создан!")
print("=" * 80)
