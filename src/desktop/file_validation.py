"""
Модуль валидации входных файлов для desktop приложения.

Проверяет корректность структуры Excel файлов и выявляет
отсутствующие колонки или некорректные данные.
"""

import pandas as pd
from typing import Tuple, Dict, List


class ValidationResult:
    """Результат валидации файла"""

    def __init__(self, is_valid: bool, message: str, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.message = message
        self.errors = errors or []
        self.warnings = warnings or []

    def get_full_message(self) -> str:
        """Получить полное сообщение с ошибками и предупреждениями"""
        parts = [self.message]

        if self.errors:
            parts.append("\n\nОШИБКИ:")
            for i, error in enumerate(self.errors, 1):
                parts.append(f"{i}. {error}")

        if self.warnings:
            parts.append("\n\nПРЕДУПРЕЖДЕНИЯ:")
            for i, warning in enumerate(self.warnings, 1):
                parts.append(f"{i}. {warning}")

        return "\n".join(parts)


def validate_excel_file(file_path: str) -> ValidationResult:
    """
    Базовая валидация Excel файла.

    Args:
        file_path: Путь к файлу

    Returns:
        ValidationResult: Результат валидации
    """
    errors = []
    warnings = []

    try:
        # Попытка прочитать файл
        df = pd.read_excel(file_path)

        # Проверка на пустоту
        if df.empty:
            errors.append("Файл пустой или не содержит данных")
            return ValidationResult(False, "❌ Файл пустой", errors)

        # Проверка минимального количества строк
        if len(df) < 2:
            warnings.append(f"Файл содержит слишком мало данных ({len(df)} строк). Рекомендуется минимум 10 строк для корректного анализа.")

        # Проверка на наличие колонок
        if len(df.columns) == 0:
            errors.append("Файл не содержит колонок")
            return ValidationResult(False, "❌ Нет колонок в файле", errors)

        return ValidationResult(
            True,
            f"✅ Файл загружен успешно ({len(df)} строк, {len(df.columns)} колонок)",
            warnings=warnings
        )

    except FileNotFoundError:
        errors.append(f"Файл не найден: {file_path}")
        return ValidationResult(False, "❌ Файл не найден", errors)

    except pd.errors.EmptyDataError:
        errors.append("Файл пустой")
        return ValidationResult(False, "❌ Файл пустой", errors)

    except Exception as e:
        errors.append(f"Ошибка чтения файла: {str(e)}")
        return ValidationResult(False, "❌ Ошибка чтения файла", errors)


def validate_historical_data(file_path: str) -> ValidationResult:
    """
    Валидация файла исторических данных.

    Проверяет наличие необходимых типов колонок для анализа.

    Args:
        file_path: Путь к файлу

    Returns:
        ValidationResult: Результат валидации
    """
    # Базовая валидация
    base_result = validate_excel_file(file_path)
    if not base_result.is_valid:
        return base_result

    errors = []
    warnings = []

    try:
        df = pd.read_excel(file_path)
        columns = [str(col).strip().lower() for col in df.columns]

        # Ожидаемые типы колонок
        expected_types = {
            "дата": ["дата", "date", "период", "period", "месяц", "month"],
            "филиал": ["филиал", "branch", "подразделение", "division", "склад", "warehouse"],
            "материал": ["материал", "material", "товар", "product", "артикул", "sku", "item"],
            "начальный остаток": ["начальный", "начало", "start", "opening", "остаток на начало"],
            "конечный остаток": ["конечный", "конец", "end", "closing", "остаток на конец"],
        }

        # Опциональные колонки
        optional_types = {
            "потребление": ["потребление", "расход", "consumption", "usage", "использование"],
            "стоимость": ["стоимость", "цена", "cost", "price", "сумма"],
        }

        # Проверка наличия ключевых типов колонок
        found_types = {}
        for col_type, patterns in expected_types.items():
            found = False
            for col in columns:
                if any(pattern in col for pattern in patterns):
                    found = True
                    found_types[col_type] = True
                    break

            if not found:
                if col_type == "дата":
                    errors.append(
                        f"❌ Не найдена колонка с датой. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type == "филиал":
                    warnings.append(
                        f"⚠️ Не найдена колонка с филиалом/складом. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type == "материал":
                    errors.append(
                        f"❌ Не найдена колонка с материалом/товаром. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type in ["начальный остаток", "конечный остаток"]:
                    errors.append(
                        f"❌ Не найдена колонка '{col_type}'. Ожидаются названия: {', '.join(patterns)}"
                    )

        # Проверка опциональных колонок
        for col_type, patterns in optional_types.items():
            found = False
            for col in columns:
                if any(pattern in col for pattern in patterns):
                    found = True
                    break
            if not found:
                if col_type == "потребление":
                    warnings.append(
                        f"⚠️ Не найдена колонка с потреблением. Рекомендуется для точного анализа. "
                        f"Ожидаются названия: {', '.join(patterns)}"
                    )

        # Если есть критические ошибки
        if errors:
            return ValidationResult(
                False,
                "❌ Файл не соответствует шаблону исторических данных",
                errors,
                warnings
            )

        # Успешная валидация
        success_msg = f"✅ Файл исторических данных корректен\n"
        success_msg += f"Найдено {len(df)} строк, {len(df.columns)} колонок"

        return ValidationResult(True, success_msg, warnings=warnings)

    except Exception as e:
        errors.append(f"Ошибка валидации: {str(e)}")
        return ValidationResult(False, "❌ Ошибка валидации", errors)


def validate_forecast_data(file_path: str) -> ValidationResult:
    """
    Валидация файла прогнозных данных.

    Проверяет наличие необходимых типов колонок для прогнозирования.

    Args:
        file_path: Путь к файлу

    Returns:
        ValidationResult: Результат валидации
    """
    # Базовая валидация
    base_result = validate_excel_file(file_path)
    if not base_result.is_valid:
        return base_result

    errors = []
    warnings = []

    try:
        df = pd.read_excel(file_path)
        columns = [str(col).strip().lower() for col in df.columns]

        # Ожидаемые типы колонок
        expected_types = {
            "дата": ["дата", "date", "период", "period", "месяц", "month"],
            "филиал": ["филиал", "branch", "подразделение", "division", "склад", "warehouse"],
            "материал": ["материал", "material", "товар", "product", "артикул", "sku", "item"],
            "плановый спрос": ["плановый", "спрос", "demand", "forecast", "прогноз", "план"],
        }

        # Проверка наличия ключевых типов колонок
        found_types = {}
        for col_type, patterns in expected_types.items():
            found = False
            for col in columns:
                if any(pattern in col for pattern in patterns):
                    found = True
                    found_types[col_type] = True
                    break

            if not found:
                if col_type == "дата":
                    errors.append(
                        f"❌ Не найдена колонка с датой. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type == "филиал":
                    warnings.append(
                        f"⚠️ Не найдена колонка с филиалом/складом. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type == "материал":
                    errors.append(
                        f"❌ Не найдена колонка с материалом/товаром. Ожидаются названия: {', '.join(patterns)}"
                    )
                elif col_type == "плановый спрос":
                    errors.append(
                        f"❌ Не найдена колонка с плановым спросом. Ожидаются названия: {', '.join(patterns)}"
                    )

        # Если есть критические ошибки
        if errors:
            return ValidationResult(
                False,
                "❌ Файл не соответствует шаблону прогнозных данных",
                errors,
                warnings
            )

        # Успешная валидация
        success_msg = f"✅ Файл прогнозных данных корректен\n"
        success_msg += f"Найдено {len(df)} строк, {len(df.columns)} колонок"

        return ValidationResult(True, success_msg, warnings=warnings)

    except Exception as e:
        errors.append(f"Ошибка валидации: {str(e)}")
        return ValidationResult(False, "❌ Ошибка валидации", errors)


def get_column_suggestions(df: pd.DataFrame, column_type: str) -> List[str]:
    """
    Получить предложения колонок для определенного типа.

    Args:
        df: DataFrame
        column_type: Тип колонки ("date", "material", "branch", "quantity", etc.)

    Returns:
        List[str]: Список подходящих колонок
    """
    columns = [str(col) for col in df.columns]

    patterns = {
        "date": ["дата", "date", "период", "period", "месяц", "month"],
        "branch": ["филиал", "branch", "подразделение", "division", "склад", "warehouse"],
        "material": ["материал", "material", "товар", "product", "артикул", "sku", "item"],
        "start_qty": ["начальный", "начало", "start", "opening"],
        "end_qty": ["конечный", "конец", "end", "closing"],
        "consumption": ["потребление", "расход", "consumption", "usage"],
        "cost": ["стоимость", "цена", "cost", "price", "сумма"],
        "demand": ["плановый", "спрос", "demand", "forecast", "прогноз", "план"],
    }

    if column_type not in patterns:
        return []

    suggestions = []
    for col in columns:
        col_lower = col.strip().lower()
        if any(pattern in col_lower for pattern in patterns[column_type]):
            suggestions.append(col)

    return suggestions


def get_template_description(file_type: str) -> Dict[str, any]:
    """
    Получить описание шаблона файла.

    Args:
        file_type: Тип файла ("historical" или "forecast")

    Returns:
        Dict: Описание шаблона с примерами колонок
    """
    if file_type == "historical":
        return {
            "название": "Шаблон исторических данных",
            "описание": "Файл с историческими данными об остатках и потреблении материалов",
            "обязательные_колонки": [
                {"название": "Дата", "примеры": "Дата, Date, Период, Месяц", "тип": "Дата (формат ГГГГ-ММ-ДД)"},
                {"название": "Материал", "примеры": "Материал, Material, Товар, Артикул", "тип": "Текст"},
                {"название": "Начальный остаток", "примеры": "Начальный остаток, Start Balance, Остаток на начало", "тип": "Число"},
                {"название": "Конечный остаток", "примеры": "Конечный остаток, End Balance, Остаток на конец", "тип": "Число"},
            ],
            "рекомендуемые_колонки": [
                {"название": "Филиал", "примеры": "Филиал, Branch, Склад, Подразделение", "тип": "Текст"},
                {"название": "Потребление", "примеры": "Потребление, Consumption, Расход, Usage", "тип": "Число"},
                {"название": "Стоимость", "примеры": "Стоимость конечная, End Cost, Цена", "тип": "Число"},
            ]
        }
    elif file_type == "forecast":
        return {
            "название": "Шаблон прогнозных данных",
            "описание": "Файл с плановым спросом на материалы (или можно использовать автоматический прогноз)",
            "обязательные_колонки": [
                {"название": "Дата", "примеры": "Дата, Date, Период, Месяц", "тип": "Дата (формат ГГГГ-ММ-ДД)"},
                {"название": "Материал", "примеры": "Материал, Material, Товар, Артикул", "тип": "Текст"},
                {"название": "Плановый спрос", "примеры": "Плановый спрос, Demand, Forecast, Прогноз", "тип": "Число"},
            ],
            "рекомендуемые_колонки": [
                {"название": "Филиал", "примеры": "Филиал, Branch, Склад, Подразделение", "тип": "Текст"},
            ],
            "примечание": "Вместо загрузки файла можно использовать АВТОМАТИЧЕСКИЙ ПРОГНОЗ на основе исторических данных"
        }
    else:
        return {}
