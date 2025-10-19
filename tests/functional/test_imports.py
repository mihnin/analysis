"""
Тесты импорта модулей после реорганизации структуры проекта
"""
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

import pytest


def test_core_analysis_imports():
    """Проверка импорта основных модулей анализа"""
    try:
        from src.analysis import historical_analysis
        from src.analysis import forecast_analysis
        from src.analysis import forecasting_models
        assert historical_analysis is not None
        assert forecast_analysis is not None
        assert forecasting_models is not None
    except ImportError as e:
        pytest.fail(f"Failed to import analysis modules: {e}")


def test_utils_imports():
    """Проверка импорта утилит"""
    try:
        from src.utils import data_validation
        from src.utils import utils
        from src.utils import visualization
        assert data_validation is not None
        assert utils is not None
        assert visualization is not None
    except ImportError as e:
        pytest.fail(f"Failed to import utils modules: {e}")


def test_desktop_imports():
    """Проверка импорта desktop модулей"""
    try:
        from src.desktop import desktop_ui_styles
        from src.desktop import desktop_ui_components
        from src.desktop import file_validation
        assert desktop_ui_styles is not None
        assert desktop_ui_components is not None
        assert file_validation is not None
    except ImportError as e:
        pytest.fail(f"Failed to import desktop modules: {e}")


def test_web_imports():
    """Проверка импорта web модулей"""
    try:
        from src.web import logging_config
        assert logging_config is not None
    except ImportError as e:
        pytest.fail(f"Failed to import web modules: {e}")


def test_key_functions_available():
    """Проверка доступности ключевых функций"""
    from src.analysis.historical_analysis import analyze_historical_data
    from src.analysis.forecast_analysis import (
        analyze_forecast_data,
        forecast_start_balance,
        calculate_purchase_recommendations
    )
    from src.analysis.forecasting_models import forecast_demand

    assert callable(analyze_historical_data)
    assert callable(analyze_forecast_data)
    assert callable(forecast_start_balance)
    assert callable(calculate_purchase_recommendations)
    assert callable(forecast_demand)


def test_data_validation_functions():
    """Проверка функций валидации данных"""
    from src.utils.data_validation import (
        normalize_consumption,
        detect_consumption_convention
    )

    assert callable(normalize_consumption)
    assert callable(detect_consumption_convention)


if __name__ == '__main__':
    # Запуск тестов напрямую
    pytest.main([__file__, '-v'])
