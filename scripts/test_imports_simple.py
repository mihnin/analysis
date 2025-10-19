#!/usr/bin/env python
"""
Простая проверка импортов без pytest
Используется для CI/CD когда pytest может иметь проблемы
"""
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_imports():
    """Проверка всех ключевых импортов"""
    tests_passed = 0
    tests_failed = 0

    # Test 1: Core analysis modules
    print("[TEST 1/6] Importing core analysis modules...", end=" ")
    try:
        from src.analysis import historical_analysis
        from src.analysis import forecast_analysis
        from src.analysis import forecasting_models
        assert historical_analysis is not None
        assert forecast_analysis is not None
        assert forecasting_models is not None
        print("[OK] PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Test 2: Utils modules
    print("[TEST 2/6] Importing utils modules...", end=" ")
    try:
        from src.utils import data_validation
        from src.utils import utils as utils_module
        from src.utils import visualization
        assert data_validation is not None
        assert utils_module is not None
        assert visualization is not None
        print("[OK] PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Test 3: Desktop modules (optional - requires PyQt6)
    print("[TEST 3/6] Importing desktop modules...", end=" ")
    try:
        from src.desktop import desktop_ui_styles
        from src.desktop import desktop_ui_components
        from src.desktop import file_validation
        assert desktop_ui_styles is not None
        assert desktop_ui_components is not None
        assert file_validation is not None
        print("[OK] PASSED")
        tests_passed += 1
    except ImportError as e:
        if "PyQt6" in str(e):
            print("[SKIP] SKIPPED (PyQt6 not installed - OK for CI)")
            # Don't count as failed, just skip
        else:
            print(f"[FAIL] FAILED: {e}")
            tests_failed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Test 4: Web modules
    print("[TEST 4/6] Importing web modules...", end=" ")
    try:
        from src.web import logging_config
        assert logging_config is not None
        print("[OK] PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Test 5: Key functions
    print("[TEST 5/6] Checking key functions availability...", end=" ")
    try:
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
        print("[OK] PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Test 6: Data validation functions
    print("[TEST 6/6] Checking data validation functions...", end=" ")
    try:
        from src.utils.data_validation import (
            normalize_consumption,
            detect_consumption_convention
        )
        assert callable(normalize_consumption)
        assert callable(detect_consumption_convention)
        print("[OK] PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] FAILED: {e}")
        tests_failed += 1

    # Summary
    total_tests = 6
    tests_skipped = total_tests - tests_passed - tests_failed

    print("\n" + "="*50)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Tests failed: {tests_failed}/{total_tests}")
    if tests_skipped > 0:
        print(f"Tests skipped: {tests_skipped}/{total_tests}")
    print("="*50)

    if tests_failed > 0:
        print("\n[ERROR] SOME TESTS FAILED")
        sys.exit(1)
    else:
        # Success even if some tests were skipped (e.g., desktop modules without PyQt6)
        print("\n[SUCCESS] ALL CRITICAL TESTS PASSED")
        if tests_skipped > 0:
            print(f"Note: {tests_skipped} optional test(s) skipped")
        sys.exit(0)

if __name__ == '__main__':
    test_imports()
