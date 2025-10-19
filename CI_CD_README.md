# CI/CD Configuration and Testing

## Overview

Проект настроен с GitHub Actions для автоматического тестирования при каждом push или pull request.

## Test Strategy

### Core Tests (Required ✅)
Эти тесты **обязательны** и должны проходить в CI:

1. **Core analysis modules** - historical_analysis, forecast_analysis, forecasting_models
2. **Utils modules** - data_validation, utils, visualization
3. **Web modules** - logging_config (для Streamlit)
4. **Key functions** - analyze_historical_data, forecast_start_balance и др.
5. **Data validation functions** - normalize_consumption, detect_consumption_convention

### Optional Tests (Can Skip ⏭️)
Эти тесты опциональны для CI (требуют дополнительных зависимостей):

1. **Desktop modules** - требуют PyQt6 (не устанавливается в CI для веб-версии)

## Test Scripts

### 1. Simple Import Test (Primary)

**File:** `scripts/test_imports_simple.py`

**Usage:**
```bash
python scripts/test_imports_simple.py
```

**Output (with PyQt6):**
```
[TEST 1/6] Importing core analysis modules... [OK] PASSED
[TEST 2/6] Importing utils modules... [OK] PASSED
[TEST 3/6] Importing desktop modules... [OK] PASSED
[TEST 4/6] Importing web modules... [OK] PASSED
[TEST 5/6] Checking key functions availability... [OK] PASSED
[TEST 6/6] Checking data validation functions... [OK] PASSED

[SUCCESS] ALL CRITICAL TESTS PASSED
```

**Output (without PyQt6 - in CI):**
```
[TEST 1/6] Importing core analysis modules... [OK] PASSED
[TEST 2/6] Importing utils modules... [OK] PASSED
[TEST 3/6] Importing desktop modules... [SKIP] SKIPPED (PyQt6 not installed - OK for CI)
[TEST 4/6] Importing web modules... [OK] PASSED
[TEST 5/6] Checking key functions availability... [OK] PASSED
[TEST 6/6] Checking data validation functions... [OK] PASSED

[SUCCESS] ALL CRITICAL TESTS PASSED
Note: 1 optional test(s) skipped
```

**Exit codes:**
- `0` - Success (all critical tests passed, optional tests may be skipped)
- `1` - Failure (one or more critical tests failed)

### 2. Pytest Tests (Secondary)

**File:** `tests/functional/test_imports.py`

**Usage:**
```bash
pytest tests/functional/test_imports.py -v -s --tb=short
```

**Note:** Может иметь проблемы с I/O в некоторых средах, поэтому в CI используется с `continue-on-error: true`

## GitHub Actions Workflow

**File:** `.github/workflows/ci.yml`

### Jobs

#### 1. test (Matrix: Python 3.10, 3.11, 3.12)
- Unit tests (historical_analysis, forecast_analysis, forecasting_models)
- Integration tests (consumption_conventions, new_features)
- Coverage report

#### 2. lint
- flake8 syntax check
- black formatting check
- pylint code quality
- isort import sorting

#### 3. functional-test
- **Primary:** Simple import test (always runs)
- **Secondary:** pytest import tests (continue-on-error)
- Template tests (continue-on-error)

### Workflow Configuration

```yaml
functional-test:
  name: Functional Tests
  runs-on: ubuntu-latest

  steps:
  - name: Checkout code
    uses: actions/checkout@v4

  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: '3.12'

  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install -r requirements.txt    # PyQt6 НЕ устанавливается
      pip install pytest

  # ✅ Основная проверка - обязательно должна пройти
  - name: Verify core modules load (simple check)
    run: |
      python scripts/test_imports_simple.py

  # ⏭️ Дополнительные проверки - могут упасть, не блокируют workflow
  - name: Run import tests with pytest
    run: |
      pytest tests/functional/test_imports.py -v -s --tb=short
    continue-on-error: true

  - name: Test template files
    run: |
      pytest tests/integration/test_both_templates.py -v -s --tb=short
    continue-on-error: true
```

## Dependencies

### requirements.txt (Core - для CI)
```
pandas>=1.5.3
numpy>=1.26.4
streamlit>=1.38.0
plotly>=5.14.1
statsmodels>=0.13.5
scipy>=1.13.1
openpyxl>=3.1.2
xlsxwriter>=3.1.2
```

### requirements_desktop.txt (Optional - НЕ для CI)
```
PyQt6>=6.6.0
```

**В CI устанавливается только `requirements.txt`**

## Local Testing

### Full test (with desktop)
```bash
# Установить все зависимости
pip install -r requirements.txt
pip install -r requirements_desktop.txt

# Запустить тесты
python scripts/test_imports_simple.py
# Output: All 6/6 tests passed
```

### CI simulation (without desktop)
```bash
# Установить только core зависимости
pip install -r requirements.txt

# Запустить тесты
python scripts/test_imports_simple.py
# Output: 5/6 tests passed, 1 skipped (desktop)
```

## Troubleshooting

### Test fails with "No module named 'PyQt6'"

**Причина:** PyQt6 не установлен

**Решение:**
- **Локально:** `pip install -r requirements_desktop.txt`
- **В CI:** Это нормально! Тест будет пропущен, CI пройдет успешно

### Test fails with "No module named 'src'"

**Причина:** Неправильная рабочая директория

**Решение:**
```bash
cd /path/to/analysis  # Корень проекта
python scripts/test_imports_simple.py
```

### pytest I/O error

**Причина:** Проблемы с захватом вывода pytest

**Решение:** Используй простой скрипт вместо pytest:
```bash
python scripts/test_imports_simple.py
```

## Best Practices

### 1. Pre-commit Testing

Перед коммитом запусти:
```bash
# Импорты
python scripts/test_imports_simple.py

# Юнит-тесты
pytest tests/unit/ -v

# Синтаксис
flake8 src/ tests/

# Форматирование
black --check src/ tests/
```

### 2. CI-friendly Code

- ✅ Core функциональность не должна зависеть от PyQt6
- ✅ Desktop модули - опциональные
- ✅ Web приложение - основной продукт
- ✅ Тесты должны работать в Linux/macOS (GitHub Actions)

### 3. Dependency Management

```python
# ✅ Good - optional import
try:
    from PyQt6.QtWidgets import QApplication
    HAS_PYQT6 = True
except ImportError:
    HAS_PYQT6 = False

# ❌ Bad - required import
from PyQt6.QtWidgets import QApplication  # Fails in CI
```

## CI Status

После push на GitHub, проверь статус в:
- **GitHub → Actions tab**
- **README badge** (если добавлен)

### Success Criteria

✅ CI проходит успешно если:
- Все core тесты прошли (5/6 minimum)
- Desktop тест может быть пропущен
- Синтаксис и форматирование корректны

❌ CI падает если:
- Любой core тест упал
- Синтаксические ошибки
- Импорт core модулей не работает

## Monitoring

### View Logs

```bash
# GitHub Actions
https://github.com/your-username/analysis/actions

# Local
pytest tests/ -v --tb=short
```

### Coverage Reports

```bash
# Generate locally
pytest tests/unit/ --cov=src --cov-report=html

# View
open htmlcov/index.html
```

## FAQs

### Q: Почему desktop тесты опциональны?

**A:** Desktop приложение требует PyQt6, который не нужен для основного веб-приложения. Устанавливать PyQt6 в CI для каждого билда неэффективно.

### Q: Как тестировать desktop локально?

**A:**
```bash
pip install -r requirements_desktop.txt
python scripts/test_imports_simple.py
# Все 6/6 тестов должны пройти
```

### Q: CI упал из-за desktop теста?

**A:** Проверь скрипт - desktop тест должен иметь `[SKIP]` статус, а не `[FAIL]`. Если `[FAIL]` - проблема в скрипте, не в зависимостях.

### Q: Нужен ли отдельный CI job для desktop?

**A:** Не обязательно. Desktop приложение тестируется локально перед релизом. Для автоматического тестирования desktop можно создать отдельный workflow, который запускается реже (например, только на release branches).

---

**Дата:** 19 октября 2025
**Статус:** ✅ Настроено и работает
