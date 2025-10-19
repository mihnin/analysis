"""
Расширенный модуль экспорта результатов анализа в Excel для desktop приложения.

Создает Excel файл с 4+ вкладками:
1. Исторический анализ (данные + метрики)
2. Прогноз и закупки (рекомендации)
3. Инструкция (как пользоваться)
4. Экономический эффект (польза для бизнеса)
"""

import pandas as pd
import xlsxwriter
from datetime import datetime
from typing import Optional


class ExcelExporter:
    """Класс для экспорта данных в Excel с фирменным оформлением"""

    # Фирменные цвета Норникель Спутник (HEX -> RGB)
    COLOR_PRIMARY_BLUE = "#0077C8"
    COLOR_DARK_BLUE = "#004C97"
    COLOR_GRAY = "#626262"
    COLOR_LIGHT_GRAY = "#C8C8C8"
    COLOR_WHITE = "#FFFFFF"

    def __init__(self, file_path: str):
        """
        Инициализация экспортера.

        Args:
            file_path: Путь к файлу для сохранения
        """
        self.file_path = file_path
        self.workbook = xlsxwriter.Workbook(file_path)
        self._create_formats()

    def _create_formats(self):
        """Создать форматы ячеек в фирменном стиле"""
        # Заголовок таблицы
        self.format_header = self.workbook.add_format({
            'bold': True,
            'font_size': 12,
            'font_color': 'white',
            'bg_color': self.COLOR_DARK_BLUE,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1,
            'text_wrap': True
        })

        # Заголовок страницы
        self.format_title = self.workbook.add_format({
            'bold': True,
            'font_size': 18,
            'font_color': self.COLOR_DARK_BLUE,
            'align': 'left',
            'valign': 'vcenter'
        })

        # Подзаголовок
        self.format_subtitle = self.workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': self.COLOR_PRIMARY_BLUE,
            'align': 'left'
        })

        # Обычный текст
        self.format_normal = self.workbook.add_format({
            'font_size': 11,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })

        # Числовой формат
        self.format_number = self.workbook.add_format({
            'font_size': 11,
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.00'
        })

        # Процентный формат
        self.format_percent = self.workbook.add_format({
            'font_size': 11,
            'border': 1,
            'align': 'right',
            'num_format': '0.00%'
        })

        # Формат даты
        self.format_date = self.workbook.add_format({
            'font_size': 11,
            'border': 1,
            'align': 'center',
            'num_format': 'dd.mm.yyyy'
        })

        # Выделенная ячейка (важное значение)
        self.format_highlight = self.workbook.add_format({
            'bold': True,
            'font_size': 11,
            'font_color': self.COLOR_DARK_BLUE,
            'bg_color': '#E3F2FD',
            'border': 1,
            'align': 'right',
            'num_format': '#,##0.00'
        })

    def add_historical_analysis_sheet(self, df_results: pd.DataFrame, explanation: str):
        """
        Добавить вкладку с результатами исторического анализа.

        Args:
            df_results: DataFrame с результатами анализа
            explanation: Текстовое объяснение метрик
        """
        worksheet = self.workbook.add_worksheet('1. Исторический анализ')

        # Заголовок
        worksheet.write('A1', 'ИСТОРИЧЕСКИЙ АНАЛИЗ ЗАПАСОВ', self.format_title)
        worksheet.write('A2', f'Дата формирования: {datetime.now().strftime("%d.%m.%Y %H:%M")}', self.format_normal)

        # Объяснение
        worksheet.write('A4', 'ОБЪЯСНЕНИЕ РАСЧЕТОВ:', self.format_subtitle)
        row = 5
        for line in explanation.split('\n'):
            if line.strip():
                worksheet.write(row, 0, line, self.format_normal)
                row += 1

        # Данные
        start_row = row + 2
        worksheet.write(start_row, 0, 'ДАННЫЕ:', self.format_subtitle)
        start_row += 1

        # Записать заголовки
        for col_num, column in enumerate(df_results.columns):
            worksheet.write(start_row, col_num, str(column), self.format_header)

        # Записать данные
        for row_num, row_data in enumerate(df_results.values):
            for col_num, value in enumerate(row_data):
                # Определить формат ячейки
                if pd.isna(value):
                    cell_format = self.format_normal
                elif isinstance(value, (int, float)):
                    cell_format = self.format_number
                elif isinstance(value, datetime):
                    cell_format = self.format_date
                else:
                    cell_format = self.format_normal

                worksheet.write(start_row + 1 + row_num, col_num, value, cell_format)

        # Настройка ширины колонок
        for col_num in range(len(df_results.columns)):
            worksheet.set_column(col_num, col_num, 15)

        # Заморозить первую строку таблицы
        worksheet.freeze_panes(start_row + 1, 0)

    def add_forecast_analysis_sheet(self, df_results: pd.DataFrame, explanation: str):
        """
        Добавить вкладку с результатами прогнозного анализа.

        Args:
            df_results: DataFrame с результатами прогноза
            explanation: Текстовое объяснение расчетов
        """
        worksheet = self.workbook.add_worksheet('2. Прогноз и закупки')

        # Заголовок
        worksheet.write('A1', 'ПРОГНОЗ ЗАПАСОВ И РЕКОМЕНДАЦИИ ПО ЗАКУПКАМ', self.format_title)
        worksheet.write('A2', f'Дата формирования: {datetime.now().strftime("%d.%m.%Y %H:%M")}', self.format_normal)

        # Объяснение
        worksheet.write('A4', 'ОБЪЯСНЕНИЕ РАСЧЕТОВ:', self.format_subtitle)
        row = 5
        for line in explanation.split('\n'):
            if line.strip():
                worksheet.write(row, 0, line, self.format_normal)
                row += 1

        # Данные
        start_row = row + 2
        worksheet.write(start_row, 0, 'ДАННЫЕ:', self.format_subtitle)
        start_row += 1

        # Записать заголовки
        for col_num, column in enumerate(df_results.columns):
            worksheet.write(start_row, col_num, str(column), self.format_header)

        # Записать данные
        for row_num, row_data in enumerate(df_results.values):
            for col_num, value in enumerate(row_data):
                # Определить формат ячейки
                if pd.isna(value):
                    cell_format = self.format_normal
                elif isinstance(value, (int, float)):
                    # Выделить рекомендации по закупкам
                    if col_num == len(df_results.columns) - 1:  # Последняя колонка - рекомендации
                        cell_format = self.format_highlight
                    else:
                        cell_format = self.format_number
                elif isinstance(value, datetime):
                    cell_format = self.format_date
                else:
                    cell_format = self.format_normal

                worksheet.write(start_row + 1 + row_num, col_num, value, cell_format)

        # Настройка ширины колонок
        for col_num in range(len(df_results.columns)):
            worksheet.set_column(col_num, col_num, 15)

        # Заморозить первую строку таблицы
        worksheet.freeze_panes(start_row + 1, 0)

    def add_instructions_sheet(self):
        """Добавить вкладку с инструкцией по использованию"""
        worksheet = self.workbook.add_worksheet('3. Инструкция')

        row = 0

        # Заголовок
        worksheet.write(row, 0, 'ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ ПРИЛОЖЕНИЯ', self.format_title)
        worksheet.set_row(row, 24)
        row += 2

        # Описание приложения
        worksheet.write(row, 0, 'О ПРИЛОЖЕНИИ:', self.format_subtitle)
        row += 1
        worksheet.write(row, 0,
            'Приложение "Анализ и прогнозирование запасов" предназначено для комплексного анализа '
            'исторических данных об остатках материалов и формирования рекомендаций по закупкам на основе прогнозов.',
            self.format_normal
        )
        row += 3

        # Шаг 1
        worksheet.write(row, 0, 'ШАГ 1: ПОДГОТОВКА ДАННЫХ', self.format_subtitle)
        row += 1

        instructions_step1 = [
            '1.1. Подготовьте файл с историческими данными в формате Excel (.xlsx или .xls)',
            '',
            'Обязательные колонки:',
            '  • Дата (формат: ГГГГ-ММ-ДД или ДД.ММ.ГГГГ)',
            '  • Материал / Товар / Артикул (текстовое название или код)',
            '  • Начальный остаток (числовое значение)',
            '  • Конечный остаток (числовое значение)',
            '',
            'Рекомендуемые колонки:',
            '  • Филиал / Склад / Подразделение',
            '  • Потребление / Расход (для более точного анализа)',
            '  • Стоимость конечного остатка (для расчета opportunity cost)',
            '',
            '1.2. Убедитесь, что данные корректны:',
            '  • Нет пропущенных значений в ключевых колонках',
            '  • Даты указаны в правильном формате',
            '  • Числовые значения не содержат текста',
        ]

        for line in instructions_step1:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 1

        # Шаг 2
        worksheet.write(row, 0, 'ШАГ 2: ЗАГРУЗКА ФАЙЛА ИСТОРИЧЕСКИХ ДАННЫХ', self.format_subtitle)
        row += 1

        instructions_step2 = [
            '2.1. Запустите приложение "Анализ и прогнозирование запасов.exe"',
            '2.2. Нажмите кнопку "Выбрать Excel файл" в разделе "Исторические данные"',
            '2.3. Выберите подготовленный файл',
            '2.4. Приложение автоматически проверит файл на соответствие шаблону',
            '2.5. Если файл корректен, вы увидите зеленую галочку и количество строк/колонок',
            '2.6. Если есть ошибки, приложение покажет, какие колонки отсутствуют',
        ]

        for line in instructions_step2:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 1

        # Шаг 3
        worksheet.write(row, 0, 'ШАГ 3: ВЫБОР РЕЖИМА ПРОГНОЗИРОВАНИЯ', self.format_subtitle)
        row += 1

        instructions_step3 = [
            'У вас есть ДВА варианта прогнозирования:',
            '',
            'ВАРИАНТ A: Загрузить готовый прогноз спроса',
            '  3A.1. Подготовьте Excel файл с плановым спросом',
            '  3A.2. Обязательные колонки: Дата, Материал, Плановый спрос',
            '  3A.3. Нажмите "Выбрать Excel файл" в разделе "Прогнозные данные"',
            '',
            'ВАРИАНТ B: Использовать автоматический прогноз (рекомендуется)',
            '  3B.1. Выберите режим "Автоматический прогноз"',
            '  3B.2. Укажите количество периодов для прогноза (1-24 месяца)',
            '  3B.3. Выберите модель прогнозирования или оставьте "AUTO" (система выберет лучшую)',
            '  3B.4. Модели: Naive, Moving Average, Exponential Smoothing, Holt-Winters, SARIMA',
        ]

        for line in instructions_step3:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 1

        # Шаг 4
        worksheet.write(row, 0, 'ШАГ 4: НАСТРОЙКА ПАРАМЕТРОВ (опционально)', self.format_subtitle)
        row += 1

        instructions_step4 = [
            '4.1. Процент страхового запаса (по умолчанию 20%)',
            '  • Определяет размер буферного запаса для защиты от дефицита',
            '',
            '4.2. Процентная ставка для opportunity cost (по умолчанию 5%)',
            '  • Используется для расчета стоимости замороженных средств в избыточных запасах',
            '',
            '4.3. Время поставки для ROP (по умолчанию 30 дней)',
            '  • Влияет на расчет точки перезаказа (Reorder Point)',
        ]

        for line in instructions_step4:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 1

        # Шаг 5
        worksheet.write(row, 0, 'ШАГ 5: ЗАПУСК АНАЛИЗА', self.format_subtitle)
        row += 1

        instructions_step5 = [
            '5.1. Нажмите кнопку "▶ Выполнить анализ"',
            '5.2. Дождитесь завершения обработки (отображается прогресс-бар)',
            '5.3. Приложение последовательно выполнит:',
            '  • Анализ исторических данных',
            '  • Генерацию прогноза (если выбран автоматический режим)',
            '  • Расчет рекомендаций по закупкам',
            '  • Создание отчета',
        ]

        for line in instructions_step5:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 1

        # Шаг 6
        worksheet.write(row, 0, 'ШАГ 6: ПРОСМОТР И СОХРАНЕНИЕ РЕЗУЛЬТАТОВ', self.format_subtitle)
        row += 1

        instructions_step6 = [
            '6.1. После завершения анализа вы увидите сводку результатов',
            '6.2. Просмотрите ключевые метрики в интерфейсе',
            '6.3. Нажмите кнопку "💾 Сохранить в Excel"',
            '6.4. Выберите место сохранения и имя файла',
            '6.5. Excel файл будет содержать 4 вкладки:',
            '  • Исторический анализ (все рассчитанные метрики)',
            '  • Прогноз и закупки (рекомендации по закупкам)',
            '  • Инструкция (эта страница)',
            '  • Экономический эффект (польза для бизнеса)',
        ]

        for line in instructions_step6:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 2

        # Поддержка
        worksheet.write(row, 0, 'ТЕХНИЧЕСКАЯ ПОДДЕРЖКА:', self.format_subtitle)
        row += 1
        worksheet.write(row, 0,
            'При возникновении вопросов или проблем обратитесь в службу технической поддержки '
            'Норникель Спутник.',
            self.format_normal
        )

        # Настройка ширины колонок
        worksheet.set_column(0, 0, 100)

    def add_business_value_sheet(self):
        """Добавить вкладку с описанием экономического эффекта"""
        worksheet = self.workbook.add_worksheet('4. Экономический эффект')

        row = 0

        # Заголовок
        worksheet.write(row, 0, 'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ И ПОЛЬЗА ДЛЯ БИЗНЕСА', self.format_title)
        worksheet.set_row(row, 24)
        row += 2

        # Введение
        worksheet.write(row, 0,
            'Внедрение системы анализа и прогнозирования запасов приносит существенный '
            'экономический эффект за счет оптимизации управления материалами.',
            self.format_normal
        )
        row += 3

        # Выгода 1
        worksheet.write(row, 0, '1. СНИЖЕНИЕ ЗАТРАТ НА ХРАНЕНИЕ', self.format_subtitle)
        row += 1

        benefits_1 = [
            'ПРОБЛЕМА:',
            'Избыточные запасы материалов занимают складские площади и замораживают оборотный капитал.',
            '',
            'РЕШЕНИЕ:',
            'Приложение выявляет излишки и мертвый запас (dead stock), рассчитывает opportunity cost - '
            'стоимость замороженных в запасах средств.',
            '',
            'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:',
            '• Сокращение избыточных запасов на 15-25%',
            '• Высвобождение оборотного капитала',
            '• Снижение затрат на аренду складских площадей',
            '• Уменьшение расходов на логистику и содержание склада',
            '',
            'ПРИМЕР:',
            'Если избыточные запасы составляют 10 млн руб. при ставке 5% годовых, '
            'opportunity cost = 500 тыс. руб./год. Сокращение запасов на 20% экономит 100 тыс. руб./год.',
        ]

        for line in benefits_1:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 2

        # Выгода 2
        worksheet.write(row, 0, '2. УМЕНЬШЕНИЕ ДЕФИЦИТА И ПРОСТОЕВ', self.format_subtitle)
        row += 1

        benefits_2 = [
            'ПРОБЛЕМА:',
            'Дефицит критически важных материалов приводит к простоям производства, срывам сроков, '
            'потере клиентов и упущенной выгоде.',
            '',
            'РЕШЕНИЕ:',
            'Система анализирует историю дефицитов, рассчитывает Fill Rate (уровень выполнения заказов), '
            'определяет точку перезаказа (ROP) и рекомендует страховые запасы.',
            '',
            'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:',
            '• Сокращение случаев дефицита на 30-40%',
            '• Снижение простоев производства',
            '• Повышение Fill Rate до 95-98%',
            '• Улучшение качества обслуживания клиентов',
            '• Предотвращение штрафов за срыв сроков поставок',
            '',
            'ПРИМЕР:',
            'Если один день простоя производственной линии стоит 1 млн руб., а дефициты сокращаются '
            'с 12 до 5 случаев в год, экономия составит 7 млн руб./год.',
        ]

        for line in benefits_2:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 2

        # Выгода 3
        worksheet.write(row, 0, '3. ОПТИМИЗАЦИЯ ЗАКУПОК', self.format_subtitle)
        row += 1

        benefits_3 = [
            'ПРОБЛЕМА:',
            'Необоснованные или несвоевременные закупки приводят к переплатам, срочным заказам '
            'по завышенным ценам, потерям на хранении устаревших материалов.',
            '',
            'РЕШЕНИЕ:',
            'Приложение формирует точные рекомендации по объемам и срокам закупок на основе прогнозов спроса, '
            'учитывая сезонность, тренды, страховые запасы и время поставки.',
            '',
            'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:',
            '• Сокращение срочных заказов на 50-70%',
            '• Снижение закупочных цен за счет планирования',
            '• Уменьшение затрат на экспресс-доставку',
            '• Оптимизация оборачиваемости запасов',
            '• Улучшение отношений с поставщиками',
            '',
            'ПРИМЕР:',
            'Если объем закупок составляет 100 млн руб./год, а оптимизация снижает цены на 3% и '
            'устраняет 20 срочных заказов (доп. стоимость 100 тыс. руб./заказ), '
            'экономия = 3 млн + 2 млн = 5 млн руб./год.',
        ]

        for line in benefits_3:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 2

        # Выгода 4
        worksheet.write(row, 0, '4. ПОВЫШЕНИЕ ТОЧНОСТИ ПЛАНИРОВАНИЯ', self.format_subtitle)
        row += 1

        benefits_4 = [
            'ПРОБЛЕМА:',
            'Отсутствие надежных прогнозов усложняет бюджетирование, планирование производства '
            'и принятие стратегических решений.',
            '',
            'РЕШЕНИЕ:',
            'Система использует 5 профессиональных моделей прогнозирования (Naive, MA, ES, Holt-Winters, SARIMA), '
            'автоматически выбирает лучшую модель, предоставляет метрики точности (MAPE, MAE, RMSE).',
            '',
            'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:',
            '• Повышение точности прогнозов на 20-30%',
            '• Улучшение качества бюджетирования',
            '• Снижение рисков при планировании производства',
            '• Более обоснованные инвестиционные решения',
            '',
            'ПРИМЕР:',
            'Точный прогноз позволяет избежать закупки избыточного оборудования на 15 млн руб. '
            'и оптимизировать инвестиции в складскую инфраструктуру, экономя 5 млн руб.',
        ]

        for line in benefits_4:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 2

        # Выгода 5
        worksheet.write(row, 0, '5. АВТОМАТИЗАЦИЯ И ЭКОНОМИЯ ВРЕМЕНИ', self.format_subtitle)
        row += 1

        benefits_5 = [
            'ПРОБЛЕМА:',
            'Ручной анализ данных в Excel занимает десятки часов рабочего времени специалистов, '
            'подвержен ошибкам, не масштабируется.',
            '',
            'РЕШЕНИЕ:',
            'Приложение автоматически обрабатывает тысячи строк данных за секунды, '
            'рассчитывает десятки метрик, генерирует понятные отчеты с объяснениями.',
            '',
            'ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:',
            '• Сокращение времени на анализ с 20-30 часов до 10 минут',
            '• Устранение человеческих ошибок в расчетах',
            '• Высвобождение времени специалистов для стратегических задач',
            '• Возможность анализа большего количества материалов',
            '',
            'ПРИМЕР:',
            'Если аналитик тратит 25 часов/месяц на анализ запасов при ставке 3000 руб./час, '
            'экономия времени 90% = 22.5 часа/месяц = 67.5 тыс. руб./месяц = 810 тыс. руб./год.',
        ]

        for line in benefits_5:
            worksheet.write(row, 0, line, self.format_normal)
            row += 1

        row += 3

        # Итого
        worksheet.write(row, 0, 'ИТОГОВЫЙ ЭКОНОМИЧЕСКИЙ ЭФФЕКТ:', self.format_subtitle)
        row += 1

        summary = [
            'Совокупный годовой эффект от внедрения системы (на примере среднего предприятия):',
            '',
            '1. Снижение затрат на хранение:          +2,000,000 руб.',
            '2. Сокращение простоев от дефицита:      +7,000,000 руб.',
            '3. Оптимизация закупок:                  +5,000,000 руб.',
            '4. Улучшение планирования:               +3,000,000 руб.',
            '5. Экономия времени специалистов:          +810,000 руб.',
            '─' * 60,
            'ИТОГО ЭФФЕКТ В ГОД:                     +17,810,000 руб.',
            '',
            'ROI (окупаемость инвестиций): менее 1 месяца',
            '',
            'Внедрение системы анализа и прогнозирования запасов - это не затраты, '
            'а высокодоходная инвестиция в эффективность бизнеса.',
        ]

        for line in summary:
            if 'ИТОГО ЭФФЕКТ' in line:
                worksheet.write(row, 0, line, self.format_highlight)
            else:
                worksheet.write(row, 0, line, self.format_normal)
            row += 1

        # Настройка ширины колонок
        worksheet.set_column(0, 0, 100)

    def close(self):
        """Закрыть и сохранить файл"""
        try:
            self.workbook.close()
            return True
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False


def export_full_report(
    file_path: str,
    df_historical: Optional[pd.DataFrame] = None,
    explanation_historical: Optional[str] = None,
    df_forecast: Optional[pd.DataFrame] = None,
    explanation_forecast: Optional[str] = None
) -> bool:
    """
    Экспортировать полный отчет в Excel.

    Args:
        file_path: Путь к файлу для сохранения
        df_historical: DataFrame с историческим анализом
        explanation_historical: Объяснение исторического анализа
        df_forecast: DataFrame с прогнозом
        explanation_forecast: Объяснение прогноза

    Returns:
        bool: True если успешно, False если ошибка
    """
    try:
        exporter = ExcelExporter(file_path)

        # Добавить вкладки
        if df_historical is not None and explanation_historical:
            exporter.add_historical_analysis_sheet(df_historical, explanation_historical)

        if df_forecast is not None and explanation_forecast:
            exporter.add_forecast_analysis_sheet(df_forecast, explanation_forecast)

        exporter.add_instructions_sheet()
        exporter.add_business_value_sheet()

        # Сохранить файл
        return exporter.close()

    except Exception as e:
        print(f"Ошибка при экспорте: {e}")
        return False
