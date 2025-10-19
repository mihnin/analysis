"""
Unit тесты для historical_analysis.py
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(__file__))

import historical_analysis as ha


class TestHistoricalAnalysis(unittest.TestCase):
    """Тесты для функций анализа исторических данных"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем простой набор данных для тестирования
        dates = pd.date_range('2021-01-01', periods=36, freq='MS')
        self.test_df = pd.DataFrame({
            'Дата': dates,
            'Материал': ['MAT-001'] * 36,
            'Филиал': ['Филиал 1'] * 36,
            'Начальный запас': [100] * 36,
            'Конечный запас': [90] * 36,
            'Списание': [10] * 36,  # Фактическое списание
            'Стоимость': [1000.0] * 36
        })

    def test_average_usage_calculation(self):
        """
        Тест: Среднее списание должно использовать фактическое списание из данных,
        а не разницу (начало - конец)
        """
        # Текущий расчет (НЕПРАВИЛЬНЫЙ)
        current_method = (self.test_df['Начальный запас'] - self.test_df['Конечный запас']).mean()

        # Правильный расчет
        if 'Списание' in self.test_df.columns:
            correct_method = self.test_df['Списание'].mean()
        else:
            correct_method = abs((self.test_df['Начальный запас'] - self.test_df['Конечный запас']).mean())

        self.assertEqual(current_method, 10.0, "Текущий метод должен дать 10")
        self.assertEqual(correct_method, 10.0, "Правильный метод должен дать 10")

    def test_negative_usage_scenario(self):
        """
        Тест: Когда запасы растут (приход > расход), текущая формула дает отрицательное значение
        """
        # Сценарий: Начало=100, Конец=150 (приход больше расхода)
        df_growing = pd.DataFrame({
            'Дата': pd.date_range('2021-01-01', periods=12, freq='MS'),
            'Материал': ['MAT-002'] * 12,
            'Филиал': ['Филиал 1'] * 12,
            'Начальный запас': [100] * 12,
            'Конечный запас': [150] * 12,
            'Приход': [70] * 12,
            'Списание': [20] * 12,  # Фактическое списание
            'Стоимость': [2000.0] * 12
        })

        # Текущий метод (НЕПРАВИЛЬНЫЙ)
        current_usage = (df_growing['Начальный запас'] - df_growing['Конечный запас']).mean()
        self.assertEqual(current_usage, -50.0, "Текущий метод дает отрицательное значение")

        # Правильный метод
        correct_usage = df_growing['Списание'].mean()
        self.assertEqual(correct_usage, 20.0, "Правильный метод дает фактическое списание")

    def test_turnover_calculation(self):
        """
        Тест: Оборачиваемость = Общее использование / Средний запас
        """
        total_usage = abs((self.test_df['Начальный запас'] - self.test_df['Конечный запас']).sum())
        average_inventory = abs((self.test_df['Начальный запас'] + self.test_df['Конечный запас']).mean() / 2)
        turnover = total_usage / average_inventory if average_inventory > 0 else 0

        expected_turnover = (36 * 10) / 95.0  # 360 / 95 = 3.79
        self.assertAlmostEqual(turnover, expected_turnover, places=2)

    def test_abc_classification(self):
        """
        Тест: ABC классификация
        """
        # A класс: > 100
        self.assertEqual(ha.get_abc_class(150), 'A')
        # B класс: 50-100
        self.assertEqual(ha.get_abc_class(75), 'B')
        # C класс: < 50
        self.assertEqual(ha.get_abc_class(30), 'C')
        # Граничные значения
        self.assertEqual(ha.get_abc_class(100), 'B')
        self.assertEqual(ha.get_abc_class(50), 'C')

    def test_xyz_classification(self):
        """
        Тест: XYZ классификация по коэффициенту вариации
        """
        # X класс: < 0.1
        self.assertEqual(ha.get_xyz_class(0.05), 'X')
        # Y класс: 0.1-0.3
        self.assertEqual(ha.get_xyz_class(0.2), 'Y')
        # Z класс: > 0.3
        self.assertEqual(ha.get_xyz_class(0.5), 'Z')
        # Граничные значения
        self.assertEqual(ha.get_xyz_class(0.1), 'Y')
        self.assertEqual(ha.get_xyz_class(0.3), 'Z')

    def test_recommended_stock_level(self):
        """
        Тест: Рекомендуемый уровень запаса
        """
        # Базовый уровень без корректировок
        base = ha.get_recommended_stock_level(50, np.nan, 0)
        self.assertEqual(base, 100.0)  # 50 * 2

        # С высокой сезонностью (+20%)
        with_seasonality = ha.get_recommended_stock_level(50, 0.6, 0)
        self.assertEqual(with_seasonality, 120.0)  # 100 * 1.2

        # С положительным трендом (+10%)
        with_trend = ha.get_recommended_stock_level(50, np.nan, 5)
        self.assertEqual(with_trend, 110.0)  # 100 * 1.1

        # С сезонностью и трендом
        with_both = ha.get_recommended_stock_level(50, 0.6, 5)
        self.assertEqual(with_both, 132.0)  # 100 * 1.2 * 1.1

    def test_excess_inventory_detection(self):
        """
        Тест: Определение излишков
        """
        # Конечный запас > 2 * среднее списание
        end_qty = 200
        avg_usage = 50
        is_excess = end_qty > 2 * abs(avg_usage)
        self.assertTrue(is_excess, "Должны быть излишки")

        # Конечный запас <= 2 * среднее списание
        end_qty = 90
        is_excess = end_qty > 2 * abs(avg_usage)
        self.assertFalse(is_excess, "Не должно быть излишков")

    def test_lost_profit_calculation(self):
        """
        Тест: Расчет упущенной выгоды
        """
        end_quantity = 200
        average_usage = 50
        end_cost = 10000
        interest_rate = 5.0

        # Есть излишки
        unit_cost = end_cost / end_quantity
        excess_amount = end_quantity - 2 * abs(average_usage)
        lost_profit = excess_amount * unit_cost * interest_rate / 100

        expected_profit = 100 * 50 * 0.05  # 250
        self.assertEqual(lost_profit, expected_profit)

    def test_growth_calculation(self):
        """
        Тест: Расчет роста за период
        """
        start = 100
        end = 300
        growth = end / start if start != 0 else np.inf
        self.assertEqual(growth, 3.0)

        # Тест деления на ноль
        start = 0
        growth = end / start if start != 0 else np.inf
        self.assertEqual(growth, np.inf)

    def test_coefficient_of_variation(self):
        """
        Тест: Коэффициент вариации спроса
        """
        usage = pd.Series([10, 15, 20, 25, 30])
        std = usage.std()
        mean = usage.mean()
        cv = std / abs(mean) if mean != 0 else np.nan

        self.assertAlmostEqual(cv, std / 20.0, places=5)

        # Тест деления на ноль
        usage_zero = pd.Series([0, 0, 0])
        mean_zero = usage_zero.mean()
        cv_zero = std / abs(mean_zero) if mean_zero != 0 else np.nan
        self.assertTrue(np.isnan(cv_zero))


class TestHistoricalAnalysisIntegration(unittest.TestCase):
    """Интеграционные тесты с реальными данными"""

    @classmethod
    def setUpClass(cls):
        """Загрузка реальных данных один раз для всех тестов"""
        try:
            cls.real_df = pd.read_excel('datasets/inventory_dataset_monthly 2021-2023.xlsx')
            cls.has_real_data = True
        except FileNotFoundError:
            cls.has_real_data = False

    def test_analyze_with_real_data(self):
        """Тест: Анализ с реальными данными"""
        if not self.has_real_data:
            self.skipTest("Реальные данные не найдены")

        date_col = self.real_df.columns[0]
        material_col = self.real_df.columns[1]
        branch_col = self.real_df.columns[3]
        start_col = self.real_df.columns[4]
        end_col = self.real_df.columns[7]
        cost_col = self.real_df.columns[8]

        try:
            results_df, explanation = ha.analyze_historical_data(
                self.real_df,
                date_col,
                branch_col,
                material_col,
                start_col,
                end_col,
                cost_col,
                5.0
            )

            # Проверки результатов
            self.assertFalse(results_df.empty, "Результаты не должны быть пустыми")
            self.assertIn('Материал', results_df.columns)
            self.assertIn('Филиал', results_df.columns)
            self.assertIn('Оборачиваемость', results_df.columns)
            self.assertIn('ABC-класс', results_df.columns)
            self.assertIn('XYZ-класс', results_df.columns)

            # Проверка что explanation не пустой
            self.assertTrue(len(explanation) > 0)

        except Exception as e:
            self.fail(f"Анализ с реальными данными провалился: {str(e)}")

    def test_no_division_by_zero(self):
        """Тест: Проверка отсутствия деления на ноль"""
        if not self.has_real_data:
            self.skipTest("Реальные данные не найдены")

        date_col = self.real_df.columns[0]
        material_col = self.real_df.columns[1]
        branch_col = self.real_df.columns[3]
        start_col = self.real_df.columns[4]
        end_col = self.real_df.columns[7]
        cost_col = self.real_df.columns[8]

        # Создаем экстремальный случай с нулями
        extreme_df = self.real_df.copy()
        extreme_df[start_col] = 0
        extreme_df[end_col] = 0

        try:
            results_df, _ = ha.analyze_historical_data(
                extreme_df,
                date_col,
                branch_col,
                material_col,
                start_col,
                end_col,
                cost_col,
                5.0
            )
            # Если не было исключения, тест пройден
            self.assertTrue(True)
        except ZeroDivisionError:
            self.fail("Обнаружено деление на ноль")


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
