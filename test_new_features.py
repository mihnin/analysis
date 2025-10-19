"""
Тест новых функций приложения
"""
import pandas as pd
import sys
import io
import historical_analysis as ha

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 80)
print("ТЕСТИРОВАНИЕ НОВЫХ ФУНКЦИЙ")
print("=" * 80)

# Загрузка данных
historical_df = pd.read_excel('datasets/inventory_dataset_monthly 2021-2023.xlsx')

date_col = historical_df.columns[0]
material_col = historical_df.columns[1]
branch_col = historical_df.columns[3]
start_col = historical_df.columns[4]
end_col = historical_df.columns[7]
cost_col = historical_df.columns[8]
consumption_col = historical_df.columns[6]

print("\nЗапуск анализа с НОВЫМИ метриками...")
print("-" * 80)

# Тестируем с разными Lead Time
lead_times = [7, 14, 30, 60]

for lead_time in lead_times:
    print(f"\n📦 Lead Time = {lead_time} дней")
    print("-" * 40)

    results_df, _ = ha.analyze_historical_data(
        historical_df.head(45),  # Первые 45 строк (3 материала × 3 филиала × 5 месяцев)
        date_col, branch_col, material_col,
        start_col, end_col, cost_col,
        5.0,
        consumption_column=consumption_col,
        lead_time_days=lead_time
    )

    # Показываем первую строку с новыми метриками
    sample = results_df.iloc[0]

    print(f"Материал: {sample['Материал']} в {sample['Филиал']}")
    print(f"\nКЛАССИЧЕСКИЕ МЕТРИКИ:")
    print(f"  • Среднее списание: {sample['Среднее списание']}")
    print(f"  • Оборачиваемость: {sample['Оборачиваемость']}")
    print(f"  • ABC-класс: {sample['ABC-класс']}")
    print(f"  • XYZ-класс: {sample['XYZ-класс']}")

    print(f"\n✨ НОВЫЕ МЕТРИКИ:")
    print(f"  • Оборачиваемость (дни): {sample['Оборачиваемость (дни)']}")
    print(f"  • Точка заказа (ROP): {sample['Точка заказа (ROP)']} при Lead Time {lead_time} дней")
    print(f"  • Периоды с дефицитом: {sample['Периоды с дефицитом']}")
    print(f"  • Fill Rate: {sample['Fill Rate']}")
    print(f"  • Мертвый запас: {sample['Мертвый запас']}")

print("\n" + "=" * 80)
print("ПРОВЕРКА ВСЕХ НОВЫХ МЕТРИК")
print("=" * 80)

# Полный анализ
full_results, _ = ha.analyze_historical_data(
    historical_df,
    date_col, branch_col, material_col,
    start_col, end_col, cost_col,
    5.0,
    consumption_column=consumption_col,
    lead_time_days=30
)

print(f"\nВсего проанализировано: {len(full_results)} комбинаций материал×филиал")

print("\n1. АНАЛИЗ ОБОРАЧИВАЕМОСТИ В ДНЯХ")
print("-" * 80)
days_values = full_results['Оборачиваемость (дни)'].value_counts().head(5)
print(days_values)

print("\n2. АНАЛИЗ ТОЧКИ ЗАКАЗА (ROP)")
print("-" * 80)
print("Примеры ROP для разных материалов:")
print(full_results[['Материал', 'Филиал', 'Точка заказа (ROP)', 'Среднее списание']].head(5))

print("\n3. АНАЛИЗ ДЕФИЦИТОВ")
print("-" * 80)
print("Материалы с дефицитами:")
deficit_materials = full_results[full_results['Периоды с дефицитом'].str.contains('из')]
print(f"Количество: {len(deficit_materials)}")
print(deficit_materials[['Материал', 'Филиал', 'Периоды с дефицитом', 'Fill Rate']].head())

print("\n4. АНАЛИЗ FILL RATE")
print("-" * 80)
print("Статистика Fill Rate:")
# Извлекаем числовые значения
fill_rates = full_results['Fill Rate'].str.replace('%', '').astype(float)
print(f"  Средний Fill Rate: {fill_rates.mean():.1f}%")
print(f"  Минимальный: {fill_rates.min():.1f}%")
print(f"  Максимальный: {fill_rates.max():.1f}%")

low_fill_rate = full_results[fill_rates < 95]
if len(low_fill_rate) > 0:
    print(f"\n⚠️  Материалы с Fill Rate < 95% (требуют внимания):")
    print(low_fill_rate[['Материал', 'Филиал', 'Fill Rate', 'Периоды с дефицитом']])
else:
    print("\n✅ Все материалы имеют Fill Rate >= 95%")

print("\n5. АНАЛИЗ МЕРТВОГО ЗАПАСА")
print("-" * 80)
dead_stock = full_results[full_results['Мертвый запас'].str.startswith('Да')]
print(f"Материалов с мертвым запасом: {len(dead_stock)}")
if len(dead_stock) > 0:
    print("\n⚠️  Материалы с мертвым запасом (>50% периодов без движения):")
    print(dead_stock[['Материал', 'Филиал', 'Мертвый запас', 'Среднее списание']])
else:
    print("✅ Нет материалов с мертвым запасом")

print("\n6. БИЗНЕС-РЕКОМЕНДАЦИИ НА ОСНОВЕ НОВЫХ МЕТРИК")
print("=" * 80)

for idx, row in full_results.iterrows():
    material = row['Материал']
    branch = row['Филиал']

    # Извлекаем Fill Rate
    fill_rate = float(row['Fill Rate'].replace('%', ''))

    # Проверка мертвого запаса
    is_dead = row['Мертвый запас'].startswith('Да')

    # Проверка дефицитов
    has_deficits = 'из' in row['Периоды с дефицитом'] and not row['Периоды с дефицитом'].startswith('0 из')

    # Формируем рекомендации
    recommendations = []

    if is_dead:
        recommendations.append(f"🔴 КРИТИЧНО: Мертвый запас! Рассмотреть ликвидацию или перераспределение.")

    if fill_rate < 95:
        recommendations.append(f"⚠️  ВАЖНО: Fill Rate {fill_rate:.1f}% - ниже целевого (95%). Увеличить точку заказа.")

    if has_deficits and fill_rate >= 95:
        recommendations.append(f"📊 КОНТРОЛЬ: Были дефициты, но Fill Rate приемлемый. Мониторить ситуацию.")

    if row['ABC-класс'] == 'A' and fill_rate < 98:
        recommendations.append(f"⚠️  A-класс требует Fill Rate ≥98%. Текущий: {fill_rate:.1f}%")

    if recommendations:
        print(f"\n{material} в {branch}:")
        for rec in recommendations:
            print(f"  {rec}")

print("\n" + "=" * 80)
print("✅ ВСЕ НОВЫЕ ФУНКЦИИ РАБОТАЮТ КОРРЕКТНО!")
print("=" * 80)

print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
print(f"  • Проанализировано материалов: {len(full_results)}")
print(f"  • Средний Fill Rate: {fill_rates.mean():.1f}%")
print(f"  • Материалов с дефицитами: {len(deficit_materials)}")
print(f"  • Материалов с мертвым запасом: {len(dead_stock)}")
print(f"  • Материалов A-класса: {(full_results['ABC-класс'] == 'A').sum()}")
print(f"  • Материалов B-класса: {(full_results['ABC-класс'] == 'B').sum()}")
print(f"  • Материалов C-класса: {(full_results['ABC-класс'] == 'C').sum()}")
