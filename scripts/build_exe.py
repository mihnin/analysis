"""
Скрипт для сборки EXE файла приложения "Анализ и прогнозирование запасов"

Использует PyInstaller для создания standalone исполняемого файла для Windows.
"""
# -*- coding: utf-8 -*-
import sys
import io

# Исправление кодировки для Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import subprocess

# Конфигурация сборки
APP_NAME = "Nornickel_Inventory_Analysis"
MAIN_SCRIPT = os.path.join("src", "desktop", "desktop_app.py")
ICON_FILE = "icon.ico"  # Если есть иконка


# Модули, которые нужно включить
HIDDEN_IMPORTS = [
    'pandas',
    'numpy',
    'PyQt6',
    'xlsxwriter',
    'openpyxl',
    'statsmodels',
    'scipy',
    'src.analysis.historical_analysis',
    'src.analysis.forecast_analysis',
    'src.analysis.forecasting_models',
    'src.utils.data_validation',
    'src.utils.utils',
    'src.utils.visualization',
    'src.desktop.file_validation',
    'src.desktop.desktop_ui_styles',
    'src.desktop.desktop_ui_components',
    'src.desktop.excel_export_desktop',
]


# Данные для включения
DATAS = []


def build_exe():
    """Собрать EXE файл"""

    print("=" * 60)
    print("СБОРКА EXE ФАЙЛА")
    print("=" * 60)
    print()

    # Проверка наличия главного скрипта
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ ОШИБКА: Файл {MAIN_SCRIPT} не найден!")
        return False

    # Формирование команды PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',  # Запуск через python -m
        '--name', APP_NAME,
        '--onefile',  # Один исполняемый файл
        '--windowed',  # Без консоли (GUI приложение)
        '--clean',  # Очистить временные файлы
        '--paths', '.',  # Добавить текущую директорию в путь поиска модулей
    ]

    # Добавить иконку, если есть
    if os.path.exists(ICON_FILE):
        cmd.extend(['--icon', ICON_FILE])
        print(f"✓ Иконка: {ICON_FILE}")
    else:
        print(f"⚠ Иконка не найдена: {ICON_FILE}")

    # Добавить скрытые импорты
    for module in HIDDEN_IMPORTS:
        cmd.extend(['--hidden-import', module])
    print(f"✓ Скрытых импортов: {len(HIDDEN_IMPORTS)}")

    # Добавить данные
    for data in DATAS:
        cmd.extend(['--add-data', data])
    if DATAS:
        print(f"✓ Файлов данных: {len(DATAS)}")

    # Главный скрипт
    cmd.append(MAIN_SCRIPT)

    print()
    print("Команда сборки:")
    print(' '.join(cmd))
    print()

    # Запуск PyInstaller
    print("Начало сборки...")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)

        print("-" * 60)
        print()
        print("=" * 60)
        print("✅ СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        print()
        print(f"EXE файл находится в: dist\\{APP_NAME}.exe")
        print()

        # Размер файла
        exe_path = os.path.join('dist', f'{APP_NAME}.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"Размер файла: {size_mb:.2f} MB")
        print()

        return True

    except subprocess.CalledProcessError as e:
        print("-" * 60)
        print()
        print("=" * 60)
        print("❌ ОШИБКА ПРИ СБОРКЕ!")
        print("=" * 60)
        print()
        print(f"Код ошибки: {e.returncode}")
        print()
        return False


def main():
    """Главная функция"""
    print()
    print("СБОРКА DESKTOP ПРИЛОЖЕНИЯ")
    print("Норникель Спутник - Анализ и прогнозирование запасов")
    print()

    # Проверка установки PyInstaller
    try:
        import PyInstaller
        print(f"✓ PyInstaller установлен (версия {PyInstaller.__version__})")
    except ImportError:
        print("❌ PyInstaller не установлен!")
        print()
        print("Установите его командой:")
        print("  pip install pyinstaller")
        print()
        return

    # Сборка
    success = build_exe()

    if success:
        print("СЛЕДУЮЩИЕ ШАГИ:")
        print("-" * 60)
        print("1. Протестируйте приложение: dist\\Nornickel_Inventory_Analysis.exe")
        print("2. Подготовьте тестовые Excel файлы")
        print("3. Проверьте все функции приложения")
        print("4. Распространите EXE файл пользователям")
        print()
    else:
        print("РЕКОМЕНДАЦИИ ПРИ ОШИБКЕ:")
        print("-" * 60)
        print("1. Убедитесь, что все зависимости установлены:")
        print("   pip install -r requirements_desktop.txt")
        print("2. Проверьте, что все модули находятся в той же папке")
        print("3. Запустите скрипт из папки проекта")
        print()


if __name__ == "__main__":
    main()
