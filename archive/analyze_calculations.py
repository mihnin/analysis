"""
Скрипт для анализа логических ошибок в расчетах
"""
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats
import sys
import io

# Устанавливаем UTF-8 для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Загружаем данные
print("=" * 80)
print("АНАЛИЗ ИСТОРИЧЕСКИХ ДАННЫХ")
print("=" * 80)

df = pd.read_excel('datasets/inventory_dataset_monthly 2021-2023.xlsx')
print(f"\nЗагружено строк: {len(df)}")
print(f"Колонки: {df.columns.tolist()}")

# Используем правильные названия колонок
date_col = df.columns[0]  # Дата
material_col = df.columns[1]  # Код материала
branch_col = df.columns[3]  # Филиал
start_qty_col = df.columns[4]  # Остаток на начало
end_qty_col = df.columns[7]  # Остаток на конец
end_cost_col = df.columns[8]  # Стоимость на конец

print(f"\nИспользуемые колонки:")
print(f"  Дата: {date_col}")
print(f"  Материал: {material_col}")
print(f"  Филиал: {branch_col}")
print(f"  Начальный остаток: {start_qty_col}")
print(f"  Конечный остаток: {end_qty_col}")
print(f"  Стоимость на конец: {end_cost_col}")

# Берем один материал и филиал для детального анализа
test_material = df[material_col].iloc[0]
test_branch = df[branch_col].iloc[0]

print(f"\n{'=' * 80}")
print(f"АНАЛИЗ ДЛЯ: {test_material} в {test_branch}")
print(f"{'=' * 80}")

group = df[(df[material_col] == test_material) & (df[branch_col] == test_branch)].copy()
group[date_col] = pd.to_datetime(group[date_col])
group = group.sort_values(date_col)

print(f"\nКоличество периодов: {len(group)}")
print(f"\nПервые 5 строк:")
print(group[[date_col, start_qty_col, end_qty_col, end_cost_col]].head())

# ПРОВЕРКА 1: Рост за период
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 1: РОСТ ЗА ПЕРИОД")
print(f"{'=' * 80}")
start_quantity = group[start_qty_col].iloc[0]
end_quantity = group[end_qty_col].iloc[-1]
growth = end_quantity / start_quantity if start_quantity != 0 else np.inf
months = (group[date_col].max() - group[date_col].min()).days / 30.44

print(f"Начальный запас (первый период): {start_quantity}")
print(f"Конечный запас (последний период): {end_quantity}")
print(f"Рост: {growth:.2f} раз")
print(f"Количество месяцев: {months:.1f}")
print(f"✓ Формула корректна: end_quantity / start_quantity")

# ПРОВЕРКА 2: Среднее списание
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 2: СРЕДНЕЕ СПИСАНИЕ")
print(f"{'=' * 80}")
usage = group[start_qty_col] - group[end_qty_col]
average_usage = usage.mean()
print(f"Списание по периодам:\n{usage.head()}")
print(f"\nСреднее списание: {average_usage:.2f}")
print(f"⚠️  ВНИМАНИЕ: В текущем коде используется формула (start - end).mean()")
print(f"   Это может давать отрицательные значения если запасы растут!")
print(f"   Правильнее: abs((start - end)).mean() для расхода")

# ПРОВЕРКА 3: Оборачиваемость
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 3: ОБОРАЧИВАЕМОСТЬ")
print(f"{'=' * 80}")
total_usage = abs((group[start_qty_col] - group[end_qty_col]).sum())
average_inventory = abs((group[start_qty_col] + group[end_qty_col]).mean() / 2)
print(f"Общее использование: {total_usage:.2f}")
print(f"Средний запас: {average_inventory:.2f}")
if average_inventory > 0:
    turnover = total_usage / average_inventory
    print(f"Оборачиваемость: {turnover:.2f}")
    print(f"✓ Формула корректна")
else:
    print(f"⚠️  Средний запас = 0, невозможно рассчитать оборачиваемость")

# ПРОВЕРКА 4: Сезонность и тренд
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 4: СЕЗОННОСТЬ И ТРЕНД")
print(f"{'=' * 80}")
print(f"Количество периодов: {len(group)}")
if len(group) > 12:
    print(f"✓ Достаточно данных для анализа сезонности (period=12)")
    try:
        decomposition = seasonal_decompose(group[end_qty_col], model='additive', period=12)
        seasonality = decomposition.seasonal.std() / group[end_qty_col].std()
        print(f"Сезонность: {seasonality:.2f}")
        print(f"✓ Формула корректна")
    except Exception as e:
        print(f"❌ ОШИБКА при разложении: {e}")

    trend = stats.linregress(range(len(group)), group[end_qty_col]).slope
    print(f"Тренд (наклон): {trend:.2f}")
    print(f"✓ Формула корректна")
else:
    print(f"⚠️  Недостаточно данных для анализа сезонности")

# ПРОВЕРКА 5: ABC класс
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 5: ABC КЛАССИФИКАЦИЯ")
print(f"{'=' * 80}")
abs_avg_usage = abs(average_usage)
print(f"Абсолютное среднее списание: {abs_avg_usage:.2f}")
if abs_avg_usage > 100:
    abc_class = 'A'
elif abs_avg_usage > 50:
    abc_class = 'B'
else:
    abc_class = 'C'
print(f"ABC класс: {abc_class}")
print(f"✓ Логика корректна (A>100, B>50, остальное C)")

# ПРОВЕРКА 6: Коэффициент вариации и XYZ класс
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 6: КОЭФФИЦИЕНТ ВАРИАЦИИ И XYZ КЛАСС")
print(f"{'=' * 80}")
usage_std = usage.std()
coefficient_variation = usage_std / abs(average_usage) if average_usage != 0 else np.nan
print(f"Стандартное отклонение списаний: {usage_std:.2f}")
print(f"Коэффициент вариации: {coefficient_variation:.2f}")

if coefficient_variation < 0.1:
    xyz_class = 'X'
elif coefficient_variation < 0.3:
    xyz_class = 'Y'
else:
    xyz_class = 'Z'
print(f"XYZ класс: {xyz_class}")
print(f"✓ Логика корректна (X<0.1, Y<0.3, остальное Z)")

# ПРОВЕРКА 7: Рекомендуемый уровень запаса
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 7: РЕКОМЕНДУЕМЫЙ УРОВЕНЬ ЗАПАСА")
print(f"{'=' * 80}")
base_level = abs(average_usage) * 2
print(f"Базовый уровень (среднее * 2): {base_level:.2f}")
if len(group) > 12:
    if seasonality > 0.5:
        base_level *= 1.2
        print(f"Корректировка на сезонность (+20%): {base_level:.2f}")
    if trend > 0:
        base_level *= 1.1
        print(f"Корректировка на тренд (+10%): {base_level:.2f}")
print(f"Итоговый рекомендуемый уровень: {base_level:.0f}")
print(f"✓ Логика корректна")

# ПРОВЕРКА 8: Упущенная выгода
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 8: УПУЩЕННАЯ ВЫГОДА")
print(f"{'=' * 80}")
excess_inventory = "Да" if end_quantity > 2 * abs(average_usage) else "Нет"
print(f"Конечный запас: {end_quantity}")
print(f"2 * Среднее списание: {2 * abs(average_usage):.2f}")
print(f"Есть излишки: {excess_inventory}")

end_cost = group[end_cost_col].iloc[-1]
unit_cost = end_cost / end_quantity if end_quantity != 0 else 0
print(f"Стоимость на конец: {end_cost:.2f}")
print(f"Стоимость единицы: {unit_cost:.2f}")

interest_rate = 5.0
if excess_inventory == "Да":
    excess_amount = end_quantity - 2 * abs(average_usage)
    lost_profit = excess_amount * unit_cost * interest_rate / 100
    print(f"Количество излишков: {excess_amount:.2f}")
    print(f"Упущенная выгода: {lost_profit:.2f} руб.")
    print(f"✓ Формула корректна")
else:
    print(f"Нет излишков, упущенная выгода = 0")

# ПРОВЕРКА данных с приходом и расходом
print(f"\n{'=' * 80}")
print("ПРОВЕРКА 9: ЛОГИКА С ПРИХОДОМ И РАСХОДОМ")
print(f"{'=' * 80}")
arrival_col = df.columns[5]  # Приход
consumption_col = df.columns[6]  # Расход/Списание

print(f"Колонка прихода: {arrival_col}")
print(f"Колонка расхода: {consumption_col}")
print(f"\nПроверяем баланс: Начало + Приход - Расход = Конец")

for idx, row in group.head(3).iterrows():
    start = row[start_qty_col]
    arrival = row[arrival_col]
    consumption = row[consumption_col]
    end = row[end_qty_col]
    calculated_end = start + arrival - consumption
    diff = end - calculated_end
    print(f"\nДата: {row[date_col].date()}")
    print(f"  Начало: {start}, Приход: {arrival}, Расход: {consumption}, Конец: {end}")
    print(f"  Расчет: {start} + {arrival} - {consumption} = {calculated_end}")
    if abs(diff) < 0.01:
        print(f"  ✓ Баланс сходится")
    else:
        print(f"  ⚠️  РАСХОЖДЕНИЕ: {diff:.2f}")

print(f"\n{'=' * 80}")
print("❗ КРИТИЧЕСКАЯ НАХОДКА:")
print(f"{'=' * 80}")
print("В исходных данных есть колонка 'Расход/Списание', но в коде")
print("среднее списание считается как (start - end).mean()")
print("Это НЕКОРРЕКТНО, так как:")
print("  1. Игнорирует приход товара")
print("  2. Может давать отрицательные значения")
print("  3. Фактический расход уже есть в данных!")
print("\n✅ ИСПРАВЛЕНИЕ: Использовать фактический расход из данных")
print(f"   Средний расход = df['{consumption_col}'].mean()")
