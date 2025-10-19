"""
Скрипт для автоматического обновления импортов после реорганизации файловой структуры
"""
import re
from pathlib import Path

# Словарь замен для импортов
IMPORT_REPLACEMENTS = {
    # Модули анализа
    r'from src.analysis import historical_analysis': 'from src.analysis import historical_analysis',
    r'from src.analysis import forecast_analysis': 'from src.analysis import forecast_analysis',
    r'from src.analysis import forecasting_models': 'from src.analysis import forecasting_models',
    r'from src.analysis.historical_analysis import': 'from src.analysis.historical_analysis import',
    r'from src.analysis.forecast_analysis import': 'from src.analysis.forecast_analysis import',
    r'from src.analysis.forecasting_models import': 'from src.analysis.forecasting_models import',

    # Утилиты
    r'from src.utils import data_validation': 'from src.utils import data_validation',
    r'from src.utils import data_processing': 'from src.utils import data_processing',
    r'from src.utils import utils\b': 'from src.utils import utils',
    r'from src.utils import visualization': 'from src.utils import visualization',
    r'from src.utils import ui_elements': 'from src.utils import ui_elements',
    r'from src.utils.data_validation import': 'from src.utils.data_validation import',
    r'from src.utils.utils import': 'from src.utils.utils import',
    r'from src.utils.visualization import': 'from src.utils.visualization import',

    # Desktop
    r'from src.desktop import desktop_ui_components': 'from src.desktop import desktop_ui_components',
    r'from src.desktop import desktop_ui_styles': 'from src.desktop import desktop_ui_styles',
    r'from src.desktop import file_validation': 'from src.desktop import file_validation',
    r'from src.desktop import excel_export_desktop': 'from src.desktop import excel_export_desktop',
    r'from src.desktop.desktop_ui_components import': 'from src.desktop.desktop_ui_components import',
    r'from src.desktop.desktop_ui_styles import': 'from src.desktop.desktop_ui_styles import',
    r'from src.desktop.file_validation import': 'from src.desktop.file_validation import',
    r'from src.desktop.excel_export_desktop import': 'from src.desktop.excel_export_desktop import',

    # Web
    r'from src.web import logging_config': 'from src.web import logging_config',
    r'from src.web.logging_config import': 'from src.web.logging_config import',
}

def add_sys_path_setup(content, file_path):
    """Добавляет setup для sys.path если нужно"""
    # Определяем уровень вложенности
    parts = Path(file_path).parts
    if 'src' in parts:
        level = len(parts) - parts.index('src')
    elif 'tests' in parts:
        level = len(parts) - parts.index('tests') + 1
    else:
        level = 1

    parent_str = '.parent' * level

    setup_code = f"""import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__){parent_str}
sys.path.insert(0, str(root_dir))

"""

    # Проверяем, есть ли уже setup
    if 'sys.path.insert' in content or 'PYTHONPATH' in content:
        return content

    # Вставляем после последнего import из стандартной библиотеки
    lines = content.split('\n')
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            # Проверяем, это стандартная библиотека или нет
            if not any(x in line for x in ['src.', 'historical_', 'forecast_', 'data_validation', 'utils', 'desktop_', 'logging_config']):
                insert_pos = i + 1
        elif line.strip() and not line.strip().startswith('#'):
            break

    lines.insert(insert_pos, '\n' + setup_code.rstrip())
    return '\n'.join(lines)

def update_imports_in_file(file_path):
    """Обновляет импорты в одном файле"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Применяем замены
        for pattern, replacement in IMPORT_REPLACEMENTS.items():
            content = re.sub(pattern, replacement, content)

        # Добавляем setup для sys.path
        if 'from src.' in content:
            content = add_sys_path_setup(content, file_path)

        # Сохраняем если были изменения
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Updated: {file_path}")
            return True
        else:
            print(f"[-] No changes: {file_path}")
            return False
    except Exception as e:
        print(f"[ERROR] Error in {file_path}: {e}")
        return False

def main():
    """Обновляет импорты во всех файлах проекта"""
    root = Path(__file__).parent.parent

    # Файлы для обработки
    patterns = [
        'src/**/*.py',
        'tests/**/*.py',
        'scripts/**/*.py',
    ]

    updated = 0
    for pattern in patterns:
        for file_path in root.glob(pattern):
            if '__init__.py' not in file_path.name and '__pycache__' not in str(file_path):
                if update_imports_in_file(file_path):
                    updated += 1

    print(f"\n[DONE] Updated {updated} files")

if __name__ == '__main__':
    main()
