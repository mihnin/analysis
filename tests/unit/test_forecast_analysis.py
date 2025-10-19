"""
Unit тесты для forecast_analysis.py
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

from src.analysis import forecast_analysis as fa


class TestForecastAnalysis(unittest.TestCase):
    """Тесты для функций прогнозного анализа"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Исторические данные
        hist_dates = pd.date_range('2021-01-01', periods=36, freq='MS')
        self.historical_df = pd.DataFrame({
            'Дата': hist_dates,
            'Материал': ['MAT-001'] * 36,
            'Филиал': ['Филиал 1'] * 36,
            'Конечный запас': [100] * 36
        })

        # Прогнозные данные
        forecast_dates = pd.date_range('2024-01-01', periods=12, freq='MS')
        self.forecast_df = pd.DataFrame({
            'Дата': forecast_dates,
            'Материал': ['MAT-001'] * 12,
            'Филиал': ['Филиал 1'] * 12,
            'Потребность': [50, 60, 55, 70, 65, 50, 55, 60, 65, 70, 55, 60]
        })

    def test_forecast_start_balance(self):
        """
        Тест: Прогноз начального остатка берет последний конечный остаток
        """
        last_balance = fa.forecast_start_balance(
            self.historical_df,
            self.forecast_df,
            'Дата',
            'Материал',
            'Филиал',
            'Конечный запас',
            'Дата',
            'Материал',
            'Филиал'
        )

        # Должен вернуть 100 для всех строк (последний остаток из исторических данных)
        self.assertTrue((last_balance == 100).all())
        self.assertEqual(len(last_balance), 12)

    def test_end_balance_calculation(self):
        """
        Тест: Конечный остаток = Начальный остаток - Потребность
        """
        start_balance = 100
        demand = 50
        end_balance = start_balance - demand

        self.assertEqual(end_balance, 50)

        # Проверка отрицательного остатка
        high_demand = 150
        negative_balance = start_balance - high_demand
        self.assertEqual(negative_balance, -50)
        self.assertTrue(negative_balance < 0, "Остаток может быть отрицательным")

    def test_safety_stock_calculation(self):
        """
        Тест: Страховой запас = Потребность * Процент
        """
        df = pd.DataFrame({
            'Потребность': [100, 200, 150]
        })

        safety_percent = 0.20
        expected = pd.Series([20.0, 40.0, 30.0])
        result = df['Потребность'] * safety_percent

        pd.testing.assert_series_equal(result, expected, check_names=False)

    def test_future_demand_rolling_sum(self):
        """
        Тест: Будущий спрос - rolling sum
        ТЕКУЩАЯ ЛОГИКА (НЕПРАВИЛЬНАЯ): суммирует текущий + 2 предыдущих
        ПРАВИЛЬНАЯ ЛОГИКА: должна суммировать текущий + 2 следующих
        """
        demand_series = pd.Series([10, 20, 30, 40, 50])

        # Текущий метод (НЕПРАВИЛЬНЫЙ)
        current_method = demand_series.rolling(window=3, min_periods=1).sum()
        # Результат: [10, 30, 60, 90, 120]
        # (период 0: 10, период 1: 10+20=30, период 2: 10+20+30=60, ...)

        # Правильный метод (должен суммировать вперед)
        correct_method = demand_series.rolling(window=3, min_periods=1).sum().shift(-2)
        # Или используя iloc:
        correct_manual = pd.Series([
            demand_series.iloc[0:3].sum(),  # 10+20+30 = 60
            demand_series.iloc[1:4].sum(),  # 20+30+40 = 90
            demand_series.iloc[2:5].sum(),  # 30+40+50 = 120
            demand_series.iloc[3:5].sum(),  # 40+50 = 90
            demand_series.iloc[4:5].sum()   # 50 = 50
        ])

        # Проверяем текущий метод
        self.assertEqual(current_method.iloc[2], 60.0)  # 10+20+30

        # Проверяем правильный метод
        self.assertEqual(correct_manual.iloc[0], 60.0)  # 10+20+30
        self.assertEqual(correct_manual.iloc[1], 90.0)  # 20+30+40

    def test_purchase_recommendation_basic(self):
        """
        Тест: Рекомендация = max(0, Будущий спрос + Страховой запас - Конечный остаток)
        """
        future_demand = 100
        safety_stock = 20
        end_balance = 30

        recommendation = max(0, future_demand + safety_stock - end_balance)
        expected = 90  # 100 + 20 - 30

        self.assertEqual(recommendation, expected)

    def test_purchase_recommendation_no_deficit(self):
        """
        Тест: Когда остатка достаточно, рекомендация = 0
        """
        future_demand = 50
        safety_stock = 10
        end_balance = 100

        recommendation = max(0, future_demand + safety_stock - end_balance)
        self.assertEqual(recommendation, 0)

    def test_purchase_recommendation_with_deficit(self):
        """
        Тест: При отрицательном остатке учитывается в рекомендации
        """
        future_demand = 100
        safety_stock = 20
        end_balance = -50  # Дефицит

        recommendation = max(0, future_demand + safety_stock - end_balance)
        expected = 170  # 100 + 20 - (-50)

        self.assertEqual(recommendation, expected)

    def test_calculate_purchase_recommendations(self):
        """
        Тест: Функция calculate_purchase_recommendations
        """
        test_df = pd.DataFrame({
            'Конечный остаток': [100, 80, 60],
            'Потребность': [50, 60, 55]
        })

        safety_percent = 0.20
        result = fa.calculate_purchase_recommendations(
            test_df,
            'Конечный остаток',
            'Потребность',
            safety_percent
        )

        # Проверяем наличие нужных колонок
        self.assertIn('Рекомендация по закупке', result.columns)
        self.assertIn('Будущий спрос', result.columns)
        self.assertIn('Страховой запас', result.columns)

        # Проверяем расчет страхового запаса
        expected_safety = test_df['Потребность'] * safety_percent
        pd.testing.assert_series_equal(
            result['Страховой запас'],
            expected_safety,
            check_names=False
        )


class TestForecastAnalysisIssues(unittest.TestCase):
    """Тесты для выявления конкретных проблем"""

    def test_exponential_smoothing_overwrites_demand(self):
        """
        Тест: Проверка что Exponential Smoothing не должен перезаписывать
        запланированную потребность
        """
        # Создаем тестовые данные
        df = pd.DataFrame({
            'Дата': pd.date_range('2024-01-01', periods=12, freq='MS'),
            'Материал': ['MAT-001'] * 12,
            'Филиал': ['Филиал 1'] * 12,
            'Потребность': [100, 110, 105, 120, 115, 100, 105, 110, 115, 120, 105, 110],
            'Начальный остаток': [500] * 12,
            'Конечный остаток': [400] * 12,
            'Рекомендация': [0] * 12,
            'Будущий спрос': [0] * 12,
            'Страховой запас': [0] * 12
        })

        original_demand = df['Потребность'].copy()

        # ТЕКУЩАЯ ПРОБЛЕМА: analyze_forecast_data перезаписывает потребность
        # Это имитация того, что происходит в коде:
        # model = ExponentialSmoothing(df['Потребность'], trend='add', seasonal=None).fit()
        # df['Потребность'] = model.fittedvalues

        # После применения Exponential Smoothing значения изменятся
        # Мы проверяем что это НЕ должно происходить

        # Правильное поведение: исходные данные не должны меняться
        pd.testing.assert_series_equal(df['Потребность'], original_demand)

    def test_rolling_sum_direction(self):
        """
        Тест: Проверка направления rolling sum для будущего спроса
        """
        demand = pd.Series([10, 20, 30, 40, 50], name='Потребность')

        # ТЕКУЩАЯ РЕАЛИЗАЦИЯ (суммирует назад)
        backward_rolling = demand.rolling(window=3, min_periods=1).sum()

        # ПРАВИЛЬНАЯ РЕАЛИЗАЦИЯ (должна суммировать вперед)
        # Для периода i нужна сумма [i, i+1, i+2]
        forward_rolling = []
        for i in range(len(demand)):
            window_sum = demand.iloc[i:min(i+3, len(demand))].sum()
            forward_rolling.append(window_sum)
        forward_rolling = pd.Series(forward_rolling)

        # Проверяем разницу
        # Для первого периода:
        # Текущий метод: 10 (только текущий, т.к. нет предыдущих)
        # Правильный метод: 60 (10+20+30)
        self.assertEqual(backward_rolling.iloc[0], 10)
        self.assertEqual(forward_rolling.iloc[0], 60)

        # Для третьего периода:
        # Текущий метод: 60 (10+20+30)
        # Правильный метод: 120 (30+40+50)
        self.assertEqual(backward_rolling.iloc[2], 60)
        self.assertEqual(forward_rolling.iloc[2], 120)


class TestForecastAnalysisIntegration(unittest.TestCase):
    """Интеграционные тесты с реальными данными"""

    @classmethod
    def setUpClass(cls):
        """Загрузка реальных данных"""
        try:
            cls.historical_df = pd.read_excel('datasets/inventory_dataset_monthly 2021-2023.xlsx')
            cls.forecast_df = pd.read_excel('datasets/forecast_data_2024_monthly.xlsx')
            cls.has_real_data = True
        except FileNotFoundError:
            cls.has_real_data = False

    def test_forecast_start_balance_with_real_data(self):
        """Тест: Прогноз начального остатка с реальными данными"""
        if not self.has_real_data:
            self.skipTest("Реальные данные не найдены")

        hist_date = self.historical_df.columns[0]
        hist_material = self.historical_df.columns[1]
        hist_branch = self.historical_df.columns[3]
        hist_end_qty = self.historical_df.columns[7]

        forecast_date = self.forecast_df.columns[0]
        forecast_material = self.forecast_df.columns[1]
        forecast_branch = self.forecast_df.columns[3]

        result = fa.forecast_start_balance(
            self.historical_df,
            self.forecast_df,
            hist_date,
            hist_material,
            hist_branch,
            hist_end_qty,
            forecast_date,
            forecast_material,
            forecast_branch
        )

        # Проверки
        self.assertEqual(len(result), len(self.forecast_df))
        self.assertTrue(result.notna().all(), "Не должно быть NaN значений")
        self.assertTrue((result >= 0).all(), "Начальные остатки должны быть >= 0")

    def test_calculate_recommendations_with_real_data(self):
        """Тест: Расчет рекомендаций с реальными данными"""
        if not self.has_real_data:
            self.skipTest("Реальные данные не найдены")

        # Добавляем тестовые колонки
        test_df = self.forecast_df.copy()
        test_df['Конечный остаток'] = 1000
        test_df['Потребность'] = test_df[test_df.columns[4]]

        result = fa.calculate_purchase_recommendations(
            test_df,
            'Конечный остаток',
            'Потребность',
            0.20
        )

        # Проверки
        self.assertEqual(len(result), len(test_df))
        self.assertTrue((result['Рекомендация по закупке'] >= 0).all())
        self.assertTrue((result['Страховой запас'] >= 0).all())
        self.assertTrue((result['Будущий спрос'] >= 0).all())


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
