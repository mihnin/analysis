# Nornickel Inventory Analysis - Структура проекта

[![CI Tests](https://github.com/username/analysis/workflows/CI%20-%20Tests%20and%20Linting/badge.svg)](https://github.com/username/analysis/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Профессиональное приложение для анализа складских запасов и прогнозирования потребностей.

## 📁 Структура проекта

```
analysis/
├── src/                          # Исходный код
│   ├── analysis/                 # Модули анализа данных
│   │   ├── historical_analysis.py
│   │   ├── forecast_analysis.py
│   │   └── forecasting_models.py
│   ├── desktop/                  # Desktop приложение (PyQt6)
│   │   ├── desktop_app.py
│   │   ├── desktop_ui_components.py
│   │   ├── desktop_ui_styles.py
│   │   ├── file_validation.py
│   │   └── excel_export_desktop.py
│   ├── web/                      # Web приложение (Streamlit)
│   │   ├── app.py
│   │   └── logging_config.py
│   └── utils/                    # Утилиты
│       ├── data_validation.py
│       ├── utils.py
│       ├── visualization.py
│       └── ui_elements.py
├── tests/                        # Тесты
│   ├── unit/                     # Модульные тесты (12 tests)
│   ├── integration/              # Интеграционные тесты
│   └── functional/               # Функциональные тесты
├── docs/                         # Документация
│   ├── guides/                   # Руководства пользователя
│   │   ├── CONSUMPTION_CONVENTION_GUIDE.md
│   │   ├── FORECASTING_MODELS_GUIDE.md
│   │   ├── DESKTOP_APP_README.md
│   │   └── ...
│   └── reports/                  # Технические отчеты
│       ├── ERRORS_FOUND.md
│       ├── FIXES_SUMMARY.md
│       ├── FINAL_REPORT.md
│       └── ...
├── scripts/                      # Служебные скрипты
│   ├── build_exe.py
│   ├── create_templates.py
│   ├── update_imports.py
│   └── test_imports_simple.py
├── datasets/                     # Шаблоны данных
│   ├── historical_data_template.xlsx
│   ├── historical_data_correct_template.xlsx
│   └── forecast_data_template.xlsx
├── archive/                      # Устаревшие файлы
├── .github/workflows/            # CI/CD
│   └── ci.yml
├── requirements.txt
├── requirements_desktop.txt
├── pytest.ini
├── .gitignore
└── CLAUDE.md
```

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/username/analysis.git
cd analysis

# Установка зависимостей
pip install -r requirements.txt

# Для desktop приложения
pip install -r requirements_desktop.txt
```

### Запуск приложений

```bash
# Web приложение (Streamlit)
streamlit run src/web/app.py

# Desktop приложение
python src/desktop/desktop_app.py

# Сборка EXE
python scripts/build_exe.py
```

### Запуск тестов

```bash
# Все тесты
pytest tests/

# Только юнит-тесты
pytest tests/unit/ -v

# С покрытием кода
pytest tests/ --cov=src --cov-report=html

# Простая проверка импортов
python scripts/test_imports_simple.py
```

## 📚 Документация

### Основные документы

| Документ | Описание |
|----------|----------|
| **QUICK_START.md** | Быстрый старт после рефакторинга |
| **MIGRATION_GUIDE.md** | Руководство по переходу на новую структуру |
| **REFACTORING_SUMMARY.md** | Полная сводка рефакторинга |
| **GITHUB_ACTIONS_FIX.md** | Решение проблем с GitHub Actions |
| **CLAUDE.md** | Инструкции для Claude Code |

### Руководства пользователя (docs/guides/)

- **CONSUMPTION_CONVENTION_GUIDE.md** - Работа с разными форматами данных списания
- **FORECASTING_MODELS_GUIDE.md** - Полное руководство по моделям прогнозирования
- **DESKTOP_APP_README.md** - Использование desktop приложения
- **КАК_СОБРАТЬ_EXE.md** - Сборка исполняемого файла

### Технические отчеты (docs/reports/)

- **ERRORS_FOUND.md** - Найденные и исправленные ошибки
- **FIXES_SUMMARY.md** - Сводка исправлений
- **FINAL_REPORT.md** - Итоговая оценка качества
- **FORECASTING_INTEGRATION_REPORT.md** - Отчет по интеграции прогнозирования

## 🔧 Возможности

### Анализ исторических данных

- ✅ Расчет оборачиваемости запасов
- ✅ ABC-XYZ классификация
- ✅ Анализ сезонности и трендов
- ✅ Расчет точки заказа (ROP)
- ✅ Определение мертвых запасов
- ✅ Fill Rate и дефицитные периоды
- ✅ Расчет упущенной выгоды

### Прогнозирование

- ✅ 5 профессиональных моделей временных рядов
  - Naive
  - Moving Average
  - Exponential Smoothing
  - Holt-Winters
  - SARIMA
- ✅ Автоматический выбор лучшей модели (AUTO)
- ✅ Прогноз спроса на основе истории потребления
- ✅ Расчет рекомендаций по закупкам
- ✅ Метрики точности (MAPE, MAE, RMSE)

### Валидация данных

- ✅ Автоматическое определение формата списания
- ✅ Нормализация положительных/отрицательных значений
- ✅ Валидация балансового уравнения
- ✅ Проверка корректности структуры данных

## 🧪 Тестирование

### Статистика тестов

- **Юнит-тесты:** 12 тестов (test_historical_analysis, test_forecast_analysis, test_forecasting_models)
- **Интеграционные тесты:** 3 теста (test_new_features, test_both_templates, test_consumption_conventions)
- **Функциональные тесты:** test_imports

### CI/CD

GitHub Actions автоматически запускает при каждом push:
- ✅ Тесты на Python 3.10, 3.11, 3.12
- ✅ Проверка синтаксиса (flake8)
- ✅ Проверка форматирования (black)
- ✅ Линтинг (pylint, mypy, isort)
- ✅ Генерация отчетов покрытия

## 🛠 Разработка

### Структура кода

- **src/analysis/** - Основная бизнес-логика анализа
- **src/desktop/** - Desktop UI (PyQt6)
- **src/web/** - Web UI (Streamlit)
- **src/utils/** - Общие утилиты

### Добавление нового функционала

1. Создай модуль в соответствующей папке src/
2. Добавь тесты в tests/
3. Обнови документацию в docs/
4. Запусти тесты: `pytest tests/`
5. Проверь линтинг: `flake8 src/`

### Стиль кода

```bash
# Форматирование
black src/ tests/

# Проверка
flake8 src/ tests/

# Сортировка импортов
isort src/ tests/
```

## 📦 Зависимости

### Основные (requirements.txt)

- pandas >= 1.5.3
- numpy >= 1.26.4
- streamlit >= 1.38.0
- plotly >= 5.14.1
- statsmodels >= 0.13.5
- scipy >= 1.13.1
- openpyxl >= 3.1.2
- xlsxwriter >= 3.1.2

### Desktop (requirements_desktop.txt)

- PyQt6 >= 6.6.0

## 🤝 Contributing

1. Fork проект
2. Создай feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Открой Pull Request

## 📝 Changelog

### 2025-10-19 - Мажорный рефакторинг

- ✅ Реорганизована файловая структура
- ✅ Обновлены все импорты
- ✅ Настроен GitHub Actions CI/CD
- ✅ Обновлен .gitignore
- ✅ Создана полная документация
- ✅ Исправлены ошибки в desktop_app.py
- ✅ Добавлены функциональные тесты

### Предыдущие версии

См. **docs/reports/FIXES_SUMMARY.md**

## 📞 Поддержка

- **Issues:** [GitHub Issues](https://github.com/username/analysis/issues)
- **Документация:** См. папку `docs/`
- **FAQ:** См. **MIGRATION_GUIDE.md**

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🙏 Благодарности

- Nornickel за брендбук и требования
- Команда разработки за тестирование
- Сообщество Python за отличные библиотеки

---

**Версия:** 1.0.0
**Дата:** 19 октября 2025
**Статус:** ✅ Production Ready
