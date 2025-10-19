"""
Скрипт для анализа логики прогнозирования
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import sys
import io

# Устанавливаем UTF-8 для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 80)
print("АНАЛИЗ ПРОГНОЗНЫХ РАСЧЕТОВ")
print("=" * 80)

# Загружаем исторические данные
historical_df = pd.read_excel('datasets/inventory_dataset_monthly 2021-2023.xlsx')
forecast_df = pd.read_excel('datasets/forecast_data_2024_monthly.xlsx')

print(f"\nИсторические данные: {len(historical_df)} строк")
print(f"Прогнозные данные: {len(forecast_df)} строк")

# Получаем названия колонок
hist_date_col = historical_df.columns[0]
hist_material_col = historical_df.columns[1]
hist_branch_col = historical_df.columns[3]
hist_end_qty_col = historical_df.columns[7]

forecast_date_col = forecast_df.columns[0]
forecast_material_col = forecast_df.columns[1]
forecast_branch_col = forecast_df.columns[3]
forecast_demand_col = forecast_df.columns[4]

print(f"\nКолонки исторических данных:")
print(f"  Дата: {hist_date_col}")
print(f"  Материал: {hist_material_col}")
print(f"  Филиал: {hist_branch_col}")
print(f"  Конечный остаток: {hist_end_qty_col}")

print(f"\nКолонки прогнозных данных:")
print(f"  Дата: {forecast_date_col}")
print(f"  Материал: {forecast_material_col}")
print(f"  Филиал: {forecast_branch_col}")
print(f"  Запланированная потребность: {forecast_demand_col}")

# ПРОВЕРКА 1: Прогноз начального остатка
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 1: ПРОГНОЗ НАЧАЛЬНОГО ОСТАТКА")
print(f"{'=' * 80}")

# Берем последние остатки из исторических данных
historical_df[hist_date_col] = pd.to_datetime(historical_df[hist_date_col])
last_date = historical_df[hist_date_col].max()
print(f"Последняя дата в исторических данных: {last_date.date()}")

last_balances = historical_df[historical_df[hist_date_col] == last_date][[hist_branch_col, hist_material_col, hist_end_qty_col]]
print(f"\nПоследние остатки (первые 5):")
print(last_balances.head())

# Проверяем соединение с прогнозом
test_material = forecast_df[forecast_material_col].iloc[0]
test_branch = forecast_df[forecast_branch_col].iloc[0]
print(f"\nТестовый материал: {test_material}, Филиал: {test_branch}")

matching_balance = last_balances[
    (last_balances[hist_material_col] == test_material) &
    (last_balances[hist_branch_col] == test_branch)
]

if len(matching_balance) > 0:
    start_balance = matching_balance[hist_end_qty_col].iloc[0]
    print(f"✓ Найден последний остаток: {start_balance}")
else:
    print(f"⚠️  ОШИБКА: Не найден последний остаток для {test_material} в {test_branch}")

# Проверяем логику функции forecast_start_balance
print(f"\n{'=' * 80}")
print("ПРОВЕРКА ФУНКЦИИ forecast_start_balance()")
print(f"{'=' * 80}")

merged = forecast_df.merge(
    last_balances,
    left_on=[forecast_branch_col, forecast_material_col],
    right_on=[hist_branch_col, hist_material_col],
    how='left'
)

print(f"После merge: {len(merged)} строк")
print(f"Количество NaN в остатках: {merged[hist_end_qty_col].isna().sum()}")

if merged[hist_end_qty_col].isna().sum() > 0:
    print(f"⚠️  ПРОБЛЕМА: Есть материалы без начального остатка!")
    print(merged[merged[hist_end_qty_col].isna()][[forecast_material_col, forecast_branch_col]].head())

# ПРОВЕРКА 2: Расчет конечного остатка
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 2: РАСЧЕТ КОНЕЧНОГО ОСТАТКА")
print(f"{'=' * 80}")

# Берем тестовую строку
test_row = forecast_df.iloc[0]
test_demand = test_row[forecast_demand_col]
assumed_start_balance = start_balance if len(matching_balance) > 0 else 0

print(f"Начальный остаток: {assumed_start_balance}")
print(f"Запланированная потребность: {test_demand}")
end_balance = assumed_start_balance - test_demand
print(f"Конечный остаток = {assumed_start_balance} - {test_demand} = {end_balance}")

if end_balance < 0:
    print(f"⚠️  ВНИМАНИЕ: Отрицательный остаток! Не хватает товара.")
else:
    print(f"✓ Остаток положительный")

# ПРОВЕРКА 3: Расчет будущего спроса
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 3: РАСЧЕТ БУДУЩЕГО СПРОСА")
print(f"{'=' * 80}")

# Сортируем по материалу, филиалу и дате
forecast_test = forecast_df[
    (forecast_df[forecast_material_col] == test_material) &
    (forecast_df[forecast_branch_col] == test_branch)
].copy()
forecast_test[forecast_date_col] = pd.to_datetime(forecast_test[forecast_date_col])
forecast_test = forecast_test.sort_values(forecast_date_col)

print(f"Данные для {test_material} в {test_branch}:")
print(forecast_test[[forecast_date_col, forecast_demand_col]].head())

# Рассчитываем rolling sum (окно 3)
forecast_test['future_demand'] = forecast_test[forecast_demand_col].rolling(window=3, min_periods=1).sum()
print(f"\nБудущий спрос (rolling sum, window=3):")
print(forecast_test[[forecast_date_col, forecast_demand_col, 'future_demand']].head())

print(f"\n⚠️  ВНИМАНИЕ: rolling(window=3) суммирует ТЕКУЩИЙ и 2 ПРЕДЫДУЩИХ периода!")
print(f"Это может быть некорректно. Возможно, нужно суммировать ТЕКУЩИЙ и 2 СЛЕДУЮЩИХ?")
print(f"\nПример:")
print(f"  Текущая логика: periods[i-2, i-1, i]")
print(f"  Возможно правильнее: periods[i, i+1, i+2]")

# ПРОВЕРКА 4: Расчет страхового запаса
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 4: РАСЧЕТ СТРАХОВОГО ЗАПАСА")
print(f"{'=' * 80}")

safety_stock_percent = 0.20  # 20%
test_demand_val = forecast_test[forecast_demand_col].iloc[0]
safety_stock = test_demand_val * safety_stock_percent

print(f"Запланированная потребность: {test_demand_val}")
print(f"Процент страхового запаса: {safety_stock_percent * 100}%")
print(f"Страховой запас: {safety_stock:.2f}")
print(f"✓ Формула корректна: demand * percentage")

# ПРОВЕРКА 5: Рекомендация по закупке
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 5: РЕКОМЕНДАЦИЯ ПО ЗАКУПКЕ")
print(f"{'=' * 80}")

future_demand_val = forecast_test['future_demand'].iloc[0]
recommendation = max(0, future_demand_val + safety_stock - end_balance)

print(f"Будущий спрос: {future_demand_val:.2f}")
print(f"Страховой запас: {safety_stock:.2f}")
print(f"Конечный остаток: {end_balance:.2f}")
print(f"Рекомендация = max(0, {future_demand_val:.2f} + {safety_stock:.2f} - {end_balance:.2f})")
print(f"Рекомендация = {recommendation:.2f}")
print(f"✓ Формула корректна")

# ПРОВЕРКА 6: Использование Exponential Smoothing в analyze_forecast_data
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 6: EXPONENTIAL SMOOTHING В analyze_forecast_data()")
print(f"{'=' * 80}")

print(f"⚠️  КРИТИЧЕСКАЯ НАХОДКА:")
print(f"В функции analyze_forecast_data() есть цикл, который применяет")
print(f"ExponentialSmoothing к ЗАПЛАНИРОВАННОЙ ПОТРЕБНОСТИ.")
print(f"\nКод:")
print(f"  model = ExponentialSmoothing(material_branch_data[demand_column], trend='add', seasonal=None).fit()")
print(f"  analysis_df.loc[..., demand_column] = model.fittedvalues")
print(f"\n❌ ОШИБКА: Это ПЕРЕЗАПИСЫВАЕТ запланированную потребность!")
print(f"   Исходные данные теряются, заменяясь fitted values.")
print(f"\nПример последствий:")
orig_demand = forecast_test[forecast_demand_col].iloc[0]
print(f"  Исходная потребность: {orig_demand}")
print(f"  После Exponential Smoothing: будет другое значение")
print(f"\n✅ ИСПРАВЛЕНИЕ: Убрать эту перезапись или применять модель")
print(f"   только для прогноза ОСТАТКОВ, а не потребности.")

# ПРОВЕРКА 7: Порядок операций
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 7: ПОРЯДОК ОПЕРАЦИЙ В ПРИЛОЖЕНИИ")
print(f"{'=' * 80}")

print(f"В app.py порядок такой:")
print(f"1. Загружаются прогнозные данные")
print(f"2. forecast_start_balance() - прогноз начального остатка")
print(f"3. Расчет конечного остатка = начало - потребность")
print(f"4. calculate_purchase_recommendations() - рекомендации")
print(f"5. analyze_forecast_data() - применяет Exponential Smoothing")
print(f"\n⚠️  ПРОБЛЕМА: Шаг 5 перезаписывает потребность ПОСЛЕ")
print(f"   всех расчетов в шагах 3-4, что делает предыдущие расчеты некорректными!")
print(f"\n✅ ИСПРАВЛЕНИЕ: Убрать перезапись потребности в analyze_forecast_data()")

print(f"\n{'=' * 80}")
print("ИТОГИ АНАЛИЗА ПРОГНОЗОВ")
print(f"{'=' * 80}")
print(f"\n✓ Корректные элементы:")
print(f"  - Логика получения последних остатков")
print(f"  - Расчет конечного остатка (начало - потребность)")
print(f"  - Расчет страхового запаса")
print(f"  - Формула рекомендации по закупке")
print(f"\n❌ Найденные ошибки:")
print(f"  1. Rolling sum суммирует прошлые периоды вместо будущих")
print(f"  2. Exponential Smoothing перезаписывает запланированную потребность")
print(f"  3. Перезапись происходит ПОСЛЕ расчетов, что нелогично")
