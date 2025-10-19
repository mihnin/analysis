# Руководство по миграции - Новая структура проекта

## Что изменилось

Проект был полностью реорганизован для улучшения поддерживаемости, тестируемости и CI/CD интеграции.

## Новая структура проекта

```
analysis/
├── src/                          # Весь исходный код
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
│   └── utils/                    # Общие утилиты
│       ├── data_validation.py
│       ├── utils.py
│       ├── visualization.py
│       └── ui_elements.py
├── tests/                        # Все тесты
│   ├── unit/                     # Модульные тесты
│   ├── integration/              # Интеграционные тесты
│   └── functional/               # Функциональные тесты
├── docs/                         # Документация
│   ├── guides/                   # Руководства
│   └── reports/                  # Технические отчеты
├── scripts/                      # Служебные скрипты
├── archive/                      # Устаревшие файлы
├── datasets/                     # Шаблоны данных
└── .github/workflows/            # CI/CD (GitHub Actions)
```

## Как запустить приложения

### Web приложение (Streamlit)

```bash
# Из корня проекта
python -m streamlit run src/web/app.py
```

### Desktop приложение

```bash
# Из корня проекта
python src/desktop/desktop_app.py
```

### Сборка EXE

```bash
# Из корня проекта
python scripts/build_exe.py
```

## Как запустить тесты

```bash
# Все тесты
pytest tests/

# Только юнит-тесты
pytest tests/unit/

# Только интеграционные тесты
pytest tests/integration/

# С покрытием кода
pytest tests/ --cov=src --cov-report=html
```

## Изменения в импортах

### Было:
```python
import historical_analysis
import forecast_analysis
import data_validation
```

### Стало:
```python
from src.analysis import historical_analysis
from src.analysis import forecast_analysis
from src.utils import data_validation
```

## CI/CD

Настроен GitHub Actions workflow (`.github/workflows/ci.yml`):

- ✅ Проверка синтаксиса (flake8)
- ✅ Форматирование кода (black)
- ✅ Запуск тестов на Python 3.10, 3.11, 3.12
- ✅ Генерация отчетов о покрытии кода
- ✅ Линтинг (pylint, mypy, isort)

Тесты автоматически запускаются при каждом push или pull request.

## .gitignore обновлен

Теперь игнорируются:
- ✅ Исполняемые файлы (*.exe, *.app, *.dmg)
- ✅ Установочные файлы (*.msi, *.deb, *.rpm)
- ✅ Сборочные директории (build/, dist/)
- ✅ Логи приложения
- ✅ Временные файлы
- ✅ Скриншоты (кроме docs/ и images/)
- ✅ CSV/Excel файлы (кроме шаблонов)

## Дополнительные файлы

- `pytest.ini` - конфигурация pytest
- `scripts/update_imports.py` - скрипт для обновления импортов
- `PROJECT_STRUCTURE_PLAN.txt` - детальный план структуры

## Часто задаваемые вопросы

### Сломались старые скрипты?

Да, если они импортировали модули напрямую. Обновите импорты:
```bash
python scripts/update_imports.py
```

### Где находятся старые анализы и отчеты?

- Руководства: `docs/guides/`
- Технические отчеты: `docs/reports/`
- Устаревшие скрипты: `archive/`

### Как добавить новый тест?

1. Создайте файл `test_*.py` в соответствующей папке tests/
2. Импортируйте модули из `src.*`
3. Запустите `pytest tests/`

### Нужно ли обновлять CLAUDE.md?

Нет, файл `CLAUDE.md` уже обновлен и содержит актуальную информацию о новой структуре.

## Проблемы и решения

### ImportError: No module named 'src'

**Решение:** Запускайте скрипты из корневой директории проекта:
```bash
cd /path/to/analysis
python src/web/app.py  # ❌ Неправильно
python -m streamlit run src/web/app.py  # ✅ Правильно
```

### Тесты не находят модули

**Решение:** Убедитесь что pytest запускается из корня:
```bash
cd /path/to/analysis
pytest tests/  # ✅ Правильно
```

## Контрибьюторам

При добавлении нового кода:

1. Следуйте структуре `src/`
2. Добавьте тесты в `tests/`
3. Обновите документацию в `docs/`
4. Запустите тесты перед коммитом:
   ```bash
   pytest tests/
   flake8 src/
   black --check src/
   ```

## Changelog

**2025-10-19:**
- ✅ Реорганизована файловая структура
- ✅ Обновлены все импорты
- ✅ Настроен GitHub Actions CI/CD
- ✅ Обновлен .gitignore
- ✅ Создана документация по миграции
