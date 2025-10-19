
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))
"""
Тестовый скрипт для проверки импортов и базовой функциональности
"""
# -*- coding: utf-8 -*-
import sys
import io

# Исправление кодировки для Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("ТЕСТИРОВАНИЕ DESKTOP ПРИЛОЖЕНИЯ")
print("=" * 60)
print()

# Тест 1: Импорт UI модулей
print("1. Тестирование импорта UI модулей...")
try:
    from src.desktop.desktop_ui_styles import NornikColors, NornikFonts, NornikMetrics
    print("   ✓ desktop_ui_styles импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта desktop_ui_styles: {e}")
    exit(1)

try:
    from src.desktop.desktop_ui_components import (
        NornikPrimaryButton, NornikSecondaryButton,
        FileUploadCard, NornikProgressBar
    )
    print("   ✓ desktop_ui_components импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта desktop_ui_components: {e}")
    exit(1)

# Тест 2: Импорт валидации
print("\n2. Тестирование модуля валидации...")
try:
    from src.desktop.file_validation import (
        validate_excel_file,
        validate_historical_data,
        validate_forecast_data,
        ValidationResult
    )
    print("   ✓ file_validation импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта file_validation: {e}")
    exit(1)

# Тест 3: Импорт экспорта
print("\n3. Тестирование модуля экспорта...")
try:
    from src.desktop.excel_export_desktop import ExcelExporter, export_full_report
    print("   ✓ excel_export_desktop импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта excel_export_desktop: {e}")
    exit(1)

# Тест 4: Импорт логики анализа
print("\n4. Тестирование модулей анализа...")
try:
    from src.analysis.historical_analysis import analyze_historical_data
    print("   ✓ historical_analysis импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта historical_analysis: {e}")
    exit(1)

try:
    from src.analysis.forecast_analysis import analyze_forecast_data, auto_forecast_demand
    print("   ✓ forecast_analysis импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта forecast_analysis: {e}")
    exit(1)

try:
    from src.analysis.forecasting_models import (
        naive_forecast,
        moving_average_forecast,
        exponential_smoothing_forecast,
        holt_winters_forecast,
        sarima_forecast
    )
    print("   ✓ forecasting_models импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта forecasting_models: {e}")
    exit(1)

# Тест 5: Проверка PyQt6
print("\n5. Тестирование PyQt6...")
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    print("   ✓ PyQt6 импортирован")
except Exception as e:
    print(f"   ✗ Ошибка импорта PyQt6: {e}")
    exit(1)

# Тест 6: Проверка цветов из брендбука
print("\n6. Проверка брендбука...")
print(f"   - Основной синий: {NornikColors.PRIMARY_BLUE}")
print(f"   - Темно-синий: {NornikColors.DARK_BLUE}")
print(f"   - Серый: {NornikColors.GRAY}")
print("   ✓ Цвета брендбука загружены")

# Тест 7: Проверка ValidationResult
print("\n7. Проверка ValidationResult...")
result = ValidationResult(True, "Тест успешен", [], ["Тестовое предупреждение"])
print(f"   - is_valid: {result.is_valid}")
print(f"   - message: {result.message}")
print("   ✓ ValidationResult работает")

print()
print("=" * 60)
print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
print("=" * 60)
print()
print("Приложение готово к сборке EXE!")
print()
