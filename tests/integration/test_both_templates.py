
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))
# -*- coding: utf-8 -*-
"""
Тест совместимости обоих шаблонов с приложением
"""
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
from src.desktop.file_validation import validate_historical_data

print("="*80)
print("ТЕСТ СОВМЕСТИМОСТИ ШАБЛОНОВ С ПРИЛОЖЕНИЕМ")
print("="*80)
print()

# Тест 1: Упрощенный шаблон
print("1. Тест упрощенного шаблона (7 колонок)")
print("-"*80)
file1 = 'c:/dev/analysis/datasets/historical_data_template.xlsx'
result1 = validate_historical_data(file1)
print(f"   Файл: historical_data_template.xlsx")
print(f"   Валиден: {result1.is_valid}")
print(f"   Сообщение: {result1.message}")

if result1.warnings:
    print(f"   Предупреждения: {len(result1.warnings)}")
    for w in result1.warnings:
        print(f"     - {w}")

df1 = pd.read_excel(file1)
print(f"   Колонок: {len(df1.columns)}")
print(f"   Список: {list(df1.columns)}")
print()

# Тест 2: Полный шаблон
print("2. Тест полного шаблона (9 колонок)")
print("-"*80)
file2 = 'c:/dev/analysis/datasets/historical_data_correct_template.xlsx'
result2 = validate_historical_data(file2)
print(f"   Файл: historical_data_correct_template.xlsx")
print(f"   Валиден: {result2.is_valid}")
print(f"   Сообщение: {result2.message}")

if result2.warnings:
    print(f"   Предупреждения: {len(result2.warnings)}")
    for w in result2.warnings:
        print(f"     - {w}")

df2 = pd.read_excel(file2)
print(f"   Колонок: {len(df2.columns)}")
print(f"   Список: {list(df2.columns)}")
print()

# Сравнение
print("="*80)
print("ИТОГИ ТЕСТИРОВАНИЯ")
print("="*80)
print()
print(f"Упрощенный шаблон (7 колонок): {'OK' if result1.is_valid else 'ОШИБКА'}")
print(f"Полный шаблон (9 колонок):     {'OK' if result2.is_valid else 'ОШИБКА'}")
print()

if result1.is_valid and result2.is_valid:
    print("ВЫВОД: Оба шаблона корректно валидируются!")
    print()
    print("Приложение работает с ОБОИМИ шаблонами:")
    print("  - historical_data_template.xlsx (упрощенный)")
    print("  - historical_data_correct_template.xlsx (полный)")
    print()
    print("Дополнительные колонки в полном шаблоне (Поступление, Цена)")
    print("не мешают работе приложения - они просто игнорируются.")
    print()
    print("Используйте любой шаблон по вашему усмотрению!")
else:
    print("ПРОБЛЕМА: Один из шаблонов не прошел валидацию")

print()
print("="*80)
