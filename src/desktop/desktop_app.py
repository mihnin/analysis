
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
"""
Главное desktop приложение для анализа и прогнозирования запасов.

Приложение в фирменном стиле Норникель Спутник для Windows.
"""

import sys
import os
import pandas as pd
import logging
import traceback
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QFileDialog, QMessageBox, QLabel, QSpinBox,
    QDoubleSpinBox, QComboBox, QRadioButton, QButtonGroup, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon

# Настройка логирования
log_file = Path.home() / 'Nornickel_Inventory_Analysis.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("="*80)
logger.info("ЗАПУСК ПРИЛОЖЕНИЯ")
logger.info(f"Файл логов: {log_file}")
logger.info(f"Python версия: {sys.version}")
logger.info(f"Рабочая директория: {os.getcwd()}")
logger.info(f"Root директория: {root_dir}")
logger.info("="*80)

# Импорт наших модулей
logger.info("Импорт модулей UI...")
from src.desktop.desktop_ui_styles import *
from src.desktop.desktop_ui_components import *
from src.desktop.file_validation import *
from src.desktop.excel_export_desktop import export_full_report
from src.utils.utils import auto_detect_columns
logger.info("✓ Модули UI импортированы")

# Импорт логики анализа из существующих модулей
logger.info("Импорт модулей анализа...")
try:
    from src.analysis.historical_analysis import analyze_historical_data, get_explanation as get_historical_explanation
    logger.info("✓ historical_analysis импортирован")
    logger.info(f"  - analyze_historical_data: {type(analyze_historical_data)}")
    logger.info(f"  - get_historical_explanation: {type(get_historical_explanation)}")
except Exception as e:
    logger.error(f"✗ Ошибка импорта historical_analysis: {e}")
    logger.error(traceback.format_exc())

try:
    from src.analysis.forecast_analysis import (
        analyze_forecast_data,
        auto_forecast_demand,
        forecast_start_balance,
        calculate_purchase_recommendations,
        get_explanation as get_forecast_explanation
    )
    logger.info("✓ forecast_analysis импортирован")
    logger.info(f"  - analyze_forecast_data: {type(analyze_forecast_data)}")
    logger.info(f"  - auto_forecast_demand: {type(auto_forecast_demand)}")
    logger.info(f"  - forecast_start_balance: {type(forecast_start_balance)}")
    logger.info(f"  - calculate_purchase_recommendations: {type(calculate_purchase_recommendations)}")
    logger.info(f"  - get_forecast_explanation: {type(get_forecast_explanation)}")
except Exception as e:
    logger.error(f"✗ Ошибка импорта forecast_analysis: {e}")
    logger.error(traceback.format_exc())

logger.info("Все модули импортированы успешно")


class AnalysisWorker(QThread):
    """Рабочий поток для выполнения анализа в фоне"""

    progress = pyqtSignal(int, str)  # (процент, сообщение)
    finished = pyqtSignal(bool, object)  # (успех, результат или ошибка)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        """Выполнить анализ"""
        logger.info("="*80)
        logger.info("НАЧАЛО АНАЛИЗА")
        logger.info(f"Конфигурация: {self.config}")
        logger.info("="*80)

        try:
            results = {}

            # Шаг 1: Исторический анализ
            logger.info("[ШАГ 1] Загрузка исторических данных...")
            self.progress.emit(10, "Загрузка исторических данных...")
            logger.info(f"Файл: {self.config['historical_file']}")
            df_hist = pd.read_excel(self.config['historical_file'])
            logger.info(f"✓ Данные загружены: {df_hist.shape[0]} строк, {df_hist.shape[1]} колонок")
            logger.info(f"Колонки: {list(df_hist.columns)}")

            logger.info("[ШАГ 2] Анализ исторических данных...")
            self.progress.emit(30, "Анализ исторических данных...")

            # Автоматическое определение колонок
            logger.info("Автоматическое определение колонок...")
            detected_cols = auto_detect_columns(df_hist)
            logger.info(f"Обнаружено колонок: {detected_cols}")

            # Получение колонок (либо из конфига, либо автоопределение, либо дефолт)
            date_col = self.config.get('date_col') or detected_cols.get('date') or df_hist.columns[0]
            branch_col = self.config.get('branch_col') or detected_cols.get('branch')
            material_col = self.config.get('material_col') or detected_cols.get('material') or df_hist.columns[1]
            start_qty_col = self.config.get('start_qty_col') or detected_cols.get('start_quantity') or df_hist.columns[3]
            end_qty_col = self.config.get('end_qty_col') or detected_cols.get('end_quantity') or df_hist.columns[6]
            end_cost_col = self.config.get('end_cost_col') or detected_cols.get('end_cost')
            consumption_col = self.config.get('consumption_col') or detected_cols.get('consumption')

            logger.info(f"Параметры анализа (после автоопределения):")
            logger.info(f"  - date_column: {date_col}")
            logger.info(f"  - branch_column: {branch_col}")
            logger.info(f"  - material_column: {material_col}")
            logger.info(f"  - start_quantity_column: {start_qty_col}")
            logger.info(f"  - end_quantity_column: {end_qty_col}")
            logger.info(f"  - end_cost_column: {end_cost_col}")
            logger.info(f"  - consumption_column: {consumption_col}")
            logger.info(f"  - interest_rate: {self.config.get('interest_rate', 0.05)}")
            logger.info(f"  - lead_time_days: {self.config.get('lead_time_days', 30)}")

            logger.info("Вызов analyze_historical_data()...")
            logger.info(f"Тип функции: {type(analyze_historical_data)}")

            hist_results, _ = analyze_historical_data(
                df=df_hist,
                date_column=date_col,
                branch_column=branch_col,
                material_column=material_col,
                start_quantity_column=start_qty_col,
                end_quantity_column=end_qty_col,
                end_cost_column=end_cost_col,
                interest_rate=self.config.get('interest_rate', 0.05),
                consumption_column=consumption_col,
                lead_time_days=self.config.get('lead_time_days', 30)
            )
            logger.info(f"✓ analyze_historical_data() выполнена успешно")
            logger.info(f"Результат: тип={type(hist_results)}, shape={hist_results.shape if hasattr(hist_results, 'shape') else 'N/A'}")

            results['historical'] = hist_results

            logger.info("Вызов get_historical_explanation()...")
            logger.info(f"Тип функции: {type(get_historical_explanation)}")
            logger.info(f"Первая строка hist_results: {hist_results.iloc[0].to_dict() if hasattr(hist_results, 'iloc') else 'N/A'}")

            results['historical_explanation'] = get_historical_explanation(hist_results.iloc[0])
            logger.info(f"✓ get_historical_explanation() выполнена успешно")

            # Шаг 2: Прогнозный анализ
            logger.info("[ШАГ 3] Прогнозный анализ...")
            forecast_mode = self.config.get('forecast_mode')
            logger.info(f"Режим прогноза: {forecast_mode}")

            if forecast_mode == 'auto':
                # Автоматический прогноз
                logger.info("[ШАГ 3.1] Генерация автоматического прогноза...")
                self.progress.emit(50, "Генерация автоматического прогноза...")

                logger.info("Вызов auto_forecast_demand()...")
                logger.info(f"Тип функции: {type(auto_forecast_demand)}")
                logger.info(f"Параметры:")
                logger.info(f"  - forecast_periods: {self.config.get('forecast_periods', 12)}")
                logger.info(f"  - date_column: {date_col}")
                logger.info(f"  - material_column: {material_col}")
                logger.info(f"  - branch_column: {branch_col}")
                logger.info(f"  - consumption_column: {consumption_col}")
                logger.info(f"  - forecast_model: {self.config.get('forecast_model', 'auto')}")

                forecast_df = auto_forecast_demand(
                    historical_df=df_hist,
                    forecast_periods=self.config.get('forecast_periods', 12),
                    date_column=date_col,
                    material_column=material_col,
                    branch_column=branch_col,
                    consumption_column=consumption_col,
                    forecast_model=self.config.get('forecast_model', 'auto')
                )
                logger.info(f"✓ auto_forecast_demand() выполнена успешно")
                logger.info(f"Результат: тип={type(forecast_df)}, shape={forecast_df.shape if hasattr(forecast_df, 'shape') else 'N/A'}")

                logger.info("[ШАГ 3.2] Прогноз начальных остатков...")
                self.progress.emit(70, "Прогноз начальных остатков...")
                logger.info("Вызов forecast_start_balance()...")
                logger.info(f"Тип функции: {type(forecast_start_balance)}")

                # Прогноз начальных остатков
                forecast_df['Прогноз остатка на начало'] = forecast_start_balance(
                    df_hist,
                    forecast_df,
                    date_col,
                    material_col,
                    branch_col,
                    end_qty_col,
                    date_col,  # forecast_date_column
                    material_col,  # forecast_material_column
                    branch_col,  # forecast_branch_column
                    forecast_model='naive',
                    seasonal_periods=12
                )
                logger.info(f"✓ forecast_start_balance() выполнена успешно")

                # Расчет конечных остатков
                logger.info("[ШАГ 3.3] Расчет конечных остатков...")
                forecast_df['Прогноз остатка на конец'] = forecast_df['Прогноз остатка на начало'] - forecast_df['Запланированная потребность']
                logger.info(f"✓ Конечные остатки рассчитаны")

                logger.info("[ШАГ 3.4] Расчет рекомендаций по закупкам...")
                self.progress.emit(85, "Расчет рекомендаций по закупкам...")
                logger.info("Вызов calculate_purchase_recommendations()...")
                logger.info(f"Тип функции: {type(calculate_purchase_recommendations)}")

                # Расчет рекомендаций
                recommendations_df = calculate_purchase_recommendations(
                    forecast_df,
                    'Прогноз остатка на конец',
                    'Запланированная потребность',
                    self.config.get('safety_stock_pct', 0.20)
                )
                logger.info(f"✓ calculate_purchase_recommendations() выполнена успешно")

                forecast_df = pd.concat([forecast_df, recommendations_df], axis=1)
                logger.info(f"✓ Рекомендации добавлены в DataFrame")

                # Анализ
                logger.info("[ШАГ 3.5] Финальный анализ прогноза...")
                logger.info("Вызов analyze_forecast_data()...")
                logger.info(f"Тип функции: {type(analyze_forecast_data)}")

                forecast_results, _ = analyze_forecast_data(
                    forecast_df,
                    date_col,
                    material_col,
                    branch_col,
                    'Запланированная потребность',
                    'Прогноз остатка на начало',
                    'Прогноз остатка на конец',
                    'Рекомендация по закупке',
                    'Будущий спрос',
                    'Страховой запас'
                )
                logger.info(f"✓ analyze_forecast_data() выполнена успешно")

            else:
                # Ручной прогноз из файла
                logger.info("[ШАГ 3.1] Загрузка прогнозных данных...")
                self.progress.emit(50, "Загрузка прогнозных данных...")
                df_forecast = pd.read_excel(self.config['forecast_file'])
                logger.info(f"✓ Прогнозные данные загружены: {df_forecast.shape[0]} строк, {df_forecast.shape[1]} колонок")

                # Автоматическое определение колонок в прогнозном файле
                logger.info("Автоматическое определение колонок прогноза...")
                forecast_detected_cols = auto_detect_columns(df_forecast)
                logger.info(f"Обнаружено колонок в прогнозе: {forecast_detected_cols}")

                # Получение колонки планового спроса
                planned_demand_col = self.config.get('planned_demand_col') or forecast_detected_cols.get('planned_demand') or df_forecast.columns[3]
                logger.info(f"Колонка планового спроса: {planned_demand_col}")

                logger.info("[ШАГ 3.2] Прогноз начальных остатков...")
                self.progress.emit(70, "Прогноз начальных остатков...")
                # Прогноз начальных остатков
                df_forecast['Прогноз остатка на начало'] = forecast_start_balance(
                    df_hist,
                    df_forecast,
                    date_col,
                    material_col,
                    branch_col,
                    end_qty_col,
                    date_col,  # forecast_date_column
                    material_col,  # forecast_material_column
                    branch_col,  # forecast_branch_column
                    forecast_model='naive',
                    seasonal_periods=12
                )
                logger.info(f"✓ forecast_start_balance() выполнена успешно")

                # Расчет конечных остатков
                logger.info("[ШАГ 3.3] Расчет конечных остатков...")
                df_forecast['Прогноз остатка на конец'] = df_forecast['Прогноз остатка на начало'] - df_forecast[planned_demand_col]
                logger.info(f"✓ Конечные остатки рассчитаны")

                logger.info("[ШАГ 3.4] Расчет рекомендаций по закупкам...")
                self.progress.emit(85, "Расчет рекомендаций по закупкам...")
                # Расчет рекомендаций
                recommendations_df = calculate_purchase_recommendations(
                    df_forecast,
                    'Прогноз остатка на конец',
                    planned_demand_col,
                    self.config.get('safety_stock_pct', 0.20)
                )
                logger.info(f"✓ calculate_purchase_recommendations() выполнена успешно")

                df_forecast = pd.concat([df_forecast, recommendations_df], axis=1)
                logger.info(f"✓ Рекомендации добавлены в DataFrame")

                # Анализ
                logger.info("[ШАГ 3.5] Финальный анализ прогноза...")
                forecast_results, _ = analyze_forecast_data(
                    df_forecast,
                    date_col,
                    material_col,
                    branch_col,
                    planned_demand_col,
                    'Прогноз остатка на начало',
                    'Прогноз остатка на конец',
                    'Рекомендация по закупке',
                    'Будущий спрос',
                    'Страховой запас'
                )
                logger.info(f"✓ analyze_forecast_data() выполнена успешно")

            logger.info("[ШАГ 4] Сохранение результатов прогноза...")
            results['forecast'] = forecast_results
            logger.info(f"✓ Результаты прогноза сохранены")

            logger.info("Вызов get_forecast_explanation()...")
            logger.info(f"Тип функции: {type(get_forecast_explanation)}")
            logger.info(f"Первая строка forecast_results: {forecast_results.iloc[0].to_dict() if hasattr(forecast_results, 'iloc') else 'N/A'}")

            # Определяем имена колонок для explanation
            if forecast_mode == 'auto':
                demand_col_name = 'Запланированная потребность'
            else:
                demand_col_name = planned_demand_col

            results['forecast_explanation'] = get_forecast_explanation(
                forecast_results.iloc[0],
                date_col,
                material_col,
                branch_col,
                demand_col_name,
                'Прогноз остатка на начало',
                'Прогноз остатка на конец',
                'Рекомендация по закупке',
                'Будущий спрос',
                'Страховой запас'
            )
            logger.info(f"✓ get_forecast_explanation() выполнена успешно")

            logger.info("="*80)
            logger.info("АНАЛИЗ ЗАВЕРШЕН УСПЕШНО!")
            logger.info("="*80)

            self.progress.emit(100, "Анализ завершен!")
            self.finished.emit(True, results)

        except Exception as e:
            logger.error("="*80)
            logger.error("ОШИБКА ПРИ ВЫПОЛНЕНИИ АНАЛИЗА!")
            logger.error(f"Тип ошибки: {type(e).__name__}")
            logger.error(f"Сообщение: {str(e)}")
            logger.error("="*80)
            logger.error("ПОЛНЫЙ TRACEBACK:")
            logger.error(traceback.format_exc())
            logger.error("="*80)

            error_message = f"{type(e).__name__}: {str(e)}\n\nПодробности в логе: {log_file}"
            self.finished.emit(False, error_message)


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        # Данные
        self.historical_file = None
        self.forecast_file = None
        self.analysis_results = None

        # UI
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle("Норникель Спутник - Анализ и прогнозирование запасов")
        self.setGeometry(100, 100, 1200, 800)

        # Применить стили
        self.setStyleSheet(get_main_window_style())

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Шапка
        header = NornikHeader()
        main_layout.addWidget(header)

        # Прокручиваемая область для контента
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {NornikColors.BACKGROUND};
            }}
        """)

        # Контейнер контента
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(
            NornikMetrics.PADDING_LARGE,
            NornikMetrics.PADDING_LARGE,
            NornikMetrics.PADDING_LARGE,
            NornikMetrics.PADDING_LARGE
        )
        content_layout.setSpacing(NornikMetrics.PADDING_LARGE)

        # Секция 1: Загрузка исторических данных
        hist_card = self.create_historical_section()
        content_layout.addWidget(hist_card)

        # Секция 2: Прогнозирование
        forecast_card = self.create_forecast_section()
        content_layout.addWidget(forecast_card)

        # Секция 3: Параметры
        params_card = self.create_parameters_section()
        content_layout.addWidget(params_card)

        # Секция 4: Управление
        control_card = self.create_control_section()
        content_layout.addWidget(control_card)

        # Секция 5: Результаты
        self.results_card = self.create_results_section()
        self.results_card.setVisible(False)
        content_layout.addWidget(self.results_card)

        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        main_layout.addWidget(scroll)

        central_widget.setLayout(main_layout)

    def create_historical_section(self):
        """Создать секцию загрузки исторических данных"""
        card = NornikCard()
        layout = QVBoxLayout()

        # Заголовок
        title = NornikHeadingLabel("1️⃣ Исторические данные")
        layout.addWidget(title)

        info = InfoCard(
            "Что нужно?",
            "Загрузите Excel файл с историческими данными об остатках материалов. "
            "Файл должен содержать колонки: Дата, Материал, Начальный остаток, Конечный остаток.",
            icon="📊",
            color=NornikColors.PRIMARY_BLUE
        )
        layout.addWidget(info)

        # Карточка загрузки
        self.historical_upload = FileUploadCard(
            "Исторические данные",
            "Выберите Excel файл с историей остатков и потребления материалов",
            file_type="исторические данные"
        )
        self.historical_upload.file_selected.connect(self.on_historical_file_selected)
        layout.addWidget(self.historical_upload)

        card.setLayout(layout)
        return card

    def create_forecast_section(self):
        """Создать секцию прогнозирования"""
        card = NornikCard()
        layout = QVBoxLayout()

        # Заголовок
        title = NornikHeadingLabel("2️⃣ Прогнозирование спроса")
        layout.addWidget(title)

        info = InfoCard(
            "Два режима работы:",
            "Вы можете загрузить готовый прогноз спроса ИЛИ использовать автоматическое прогнозирование на основе исторических данных.",
            icon="🔮",
            color=NornikColors.TURQUOISE
        )
        layout.addWidget(info)

        # Выбор режима
        mode_group = QGroupBox("Выберите режим прогнозирования")
        mode_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: {NornikFonts.SIZE_BODY}px;
                font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
                border: 2px solid {NornikColors.BORDER};
                border-radius: {NornikMetrics.BORDER_RADIUS_MEDIUM}px;
                margin-top: {NornikMetrics.PADDING_MEDIUM}px;
                padding-top: {NornikMetrics.PADDING_MEDIUM}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {NornikMetrics.PADDING_MEDIUM}px;
                padding: 0 {NornikMetrics.PADDING_SMALL}px;
            }}
        """)

        mode_layout = QVBoxLayout()

        self.radio_manual = QRadioButton("📁 Загрузить готовый прогноз из Excel файла")
        self.radio_auto = QRadioButton("🤖 Автоматический прогноз (рекомендуется)")
        self.radio_auto.setChecked(True)

        mode_layout.addWidget(self.radio_manual)
        mode_layout.addWidget(self.radio_auto)

        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)

        # Карточка загрузки (для ручного режима)
        self.forecast_upload = FileUploadCard(
            "Прогнозные данные (опционально)",
            "Выберите Excel файл с плановым спросом на материалы",
            file_type="прогнозные данные"
        )
        self.forecast_upload.file_selected.connect(self.on_forecast_file_selected)
        self.forecast_upload.setVisible(False)
        layout.addWidget(self.forecast_upload)

        # Настройки автопрогноза
        auto_settings = QWidget()
        auto_layout = QVBoxLayout()

        # Количество периодов
        periods_layout = QHBoxLayout()
        periods_layout.addWidget(QLabel("Количество периодов для прогноза:"))
        self.forecast_periods_spin = QSpinBox()
        self.forecast_periods_spin.setRange(1, 24)
        self.forecast_periods_spin.setValue(12)
        self.forecast_periods_spin.setSuffix(" мес.")
        self.forecast_periods_spin.setStyleSheet(get_input_style())
        periods_layout.addWidget(self.forecast_periods_spin)
        periods_layout.addStretch()
        auto_layout.addLayout(periods_layout)

        # Модель прогнозирования
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Модель прогнозирования:"))
        self.forecast_model_combo = QComboBox()
        self.forecast_model_combo.addItems([
            "AUTO (автовыбор лучшей модели)",
            "naive",
            "moving_average",
            "exponential_smoothing",
            "holt_winters",
            "sarima"
        ])
        self.forecast_model_combo.setStyleSheet(get_input_style())
        model_layout.addWidget(self.forecast_model_combo)
        model_layout.addStretch()
        auto_layout.addLayout(model_layout)

        auto_settings.setLayout(auto_layout)
        layout.addWidget(auto_settings)
        self.auto_forecast_settings = auto_settings

        # Переключение режимов
        self.radio_manual.toggled.connect(lambda checked: self.forecast_upload.setVisible(checked))
        self.radio_manual.toggled.connect(lambda checked: self.auto_forecast_settings.setVisible(not checked))

        card.setLayout(layout)
        return card

    def create_parameters_section(self):
        """Создать секцию параметров"""
        card = NornikCard()
        layout = QVBoxLayout()

        # Заголовок
        title = NornikHeadingLabel("3️⃣ Параметры анализа")
        layout.addWidget(title)

        # Параметры в две колонки
        params_layout = QHBoxLayout()

        # Колонка 1
        col1_layout = QVBoxLayout()

        # Процент страхового запаса
        safety_layout = QVBoxLayout()
        safety_layout.addWidget(QLabel("Процент страхового запаса:"))
        self.safety_stock_spin = QDoubleSpinBox()
        self.safety_stock_spin.setRange(0, 100)
        self.safety_stock_spin.setValue(20)
        self.safety_stock_spin.setSuffix(" %")
        self.safety_stock_spin.setSingleStep(5)
        self.safety_stock_spin.setStyleSheet(get_input_style())
        safety_layout.addWidget(self.safety_stock_spin)
        safety_caption = NornikCaptionLabel("Размер буферного запаса для защиты от дефицита")
        safety_layout.addWidget(safety_caption)
        col1_layout.addLayout(safety_layout)

        col1_layout.addSpacing(NornikMetrics.PADDING_MEDIUM)

        # Процентная ставка
        rate_layout = QVBoxLayout()
        rate_layout.addWidget(QLabel("Процентная ставка (opportunity cost):"))
        self.interest_rate_spin = QDoubleSpinBox()
        self.interest_rate_spin.setRange(0, 100)
        self.interest_rate_spin.setValue(5)
        self.interest_rate_spin.setSuffix(" %")
        self.interest_rate_spin.setSingleStep(0.5)
        self.interest_rate_spin.setStyleSheet(get_input_style())
        rate_layout.addWidget(self.interest_rate_spin)
        rate_caption = NornikCaptionLabel("Для расчета стоимости замороженных средств в запасах")
        rate_layout.addWidget(rate_caption)
        col1_layout.addLayout(rate_layout)

        params_layout.addLayout(col1_layout, 1)

        # Колонка 2
        col2_layout = QVBoxLayout()

        # Время поставки
        lead_time_layout = QVBoxLayout()
        lead_time_layout.addWidget(QLabel("Время поставки (lead time):"))
        self.lead_time_spin = QSpinBox()
        self.lead_time_spin.setRange(1, 365)
        self.lead_time_spin.setValue(30)
        self.lead_time_spin.setSuffix(" дней")
        self.lead_time_spin.setStyleSheet(get_input_style())
        lead_time_layout.addWidget(self.lead_time_spin)
        lead_time_caption = NornikCaptionLabel("Для расчета точки перезаказа (ROP)")
        lead_time_layout.addWidget(lead_time_caption)
        col2_layout.addLayout(lead_time_layout)

        params_layout.addLayout(col2_layout, 1)

        layout.addLayout(params_layout)

        card.setLayout(layout)
        return card

    def create_control_section(self):
        """Создать секцию управления"""
        card = NornikCard()
        layout = QVBoxLayout()

        # Заголовок
        title = NornikHeadingLabel("4️⃣ Управление")
        layout.addWidget(title)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.run_button = NornikPrimaryButton("▶ Выполнить анализ")
        self.run_button.clicked.connect(self.run_analysis)
        buttons_layout.addWidget(self.run_button)

        self.export_button = NornikSecondaryButton("💾 Сохранить в Excel")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        buttons_layout.addWidget(self.export_button)

        self.help_button = NornikSecondaryButton("❓ Справка")
        self.help_button.clicked.connect(self.show_help)
        buttons_layout.addWidget(self.help_button)

        layout.addLayout(buttons_layout)

        # Прогресс-бар
        self.progress_bar = NornikProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"""
            QLabel {{
                color: {NornikColors.TEXT_SECONDARY};
                font-size: {NornikFonts.SIZE_CAPTION}px;
            }}
        """)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        card.setLayout(layout)
        return card

    def create_results_section(self):
        """Создать секцию результатов"""
        card = NornikCard()
        layout = QVBoxLayout()

        # Заголовок
        title = NornikHeadingLabel("✅ Результаты анализа")
        layout.addWidget(title)

        self.results_label = QLabel("")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet(f"""
            QLabel {{
                font-size: {NornikFonts.SIZE_BODY}px;
                padding: {NornikMetrics.PADDING_MEDIUM}px;
                background-color: #E8F5E9;
                border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
            }}
        """)
        layout.addWidget(self.results_label)

        card.setLayout(layout)
        return card

    def on_historical_file_selected(self, file_path):
        """Обработчик выбора файла исторических данных"""
        # Валидация
        result = validate_historical_data(file_path)
        if result.is_valid:
            self.historical_file = file_path
            self.historical_upload.set_status(result.message, "success")
            if result.warnings:
                for warning in result.warnings:
                    self.historical_upload.set_status(warning, "warning")
        else:
            self.historical_upload.set_status(result.get_full_message(), "error")

    def on_forecast_file_selected(self, file_path):
        """Обработчик выбора файла прогнозных данных"""
        # Валидация
        result = validate_forecast_data(file_path)
        if result.is_valid:
            self.forecast_file = file_path
            self.forecast_upload.set_status(result.message, "success")
            if result.warnings:
                for warning in result.warnings:
                    self.forecast_upload.set_status(warning, "warning")
        else:
            self.forecast_upload.set_status(result.get_full_message(), "error")

    def run_analysis(self):
        """Запустить анализ"""
        logger.info("="*80)
        logger.info("НАЖАТА КНОПКА 'ВЫПОЛНИТЬ АНАЛИЗ'")
        logger.info("="*80)

        # Проверка наличия исторических данных
        logger.info("Проверка наличия исторических данных...")
        if not self.historical_file:
            logger.warning("Исторические данные не загружены")
            show_message_box(
                self,
                "Ошибка",
                "Пожалуйста, загрузите файл с историческими данными",
                "error"
            )
            return
        logger.info(f"✓ Исторические данные: {self.historical_file}")

        # Проверка прогноза в ручном режиме
        logger.info(f"Режим: {'Автоматический' if self.radio_auto.isChecked() else 'Ручной'}")
        if self.radio_manual.isChecked() and not self.forecast_file:
            logger.warning("Ручной режим выбран, но файл прогноза не загружен")
            show_message_box(
                self,
                "Ошибка",
                "Пожалуйста, загрузите файл с прогнозными данными или выберите автоматический режим",
                "error"
            )
            return

        # Подготовка конфигурации
        logger.info("Подготовка конфигурации...")
        config = {
            'historical_file': self.historical_file,
            'forecast_mode': 'auto' if self.radio_auto.isChecked() else 'manual',
            'safety_stock_pct': self.safety_stock_spin.value() / 100,
            'interest_rate': self.interest_rate_spin.value() / 100,
            'lead_time_days': self.lead_time_spin.value(),
        }

        if self.radio_auto.isChecked():
            config['forecast_periods'] = self.forecast_periods_spin.value()
            model_text = self.forecast_model_combo.currentText()
            config['forecast_model'] = model_text.split(' ')[0].lower()
        else:
            config['forecast_file'] = self.forecast_file

        logger.info(f"Конфигурация подготовлена:")
        for key, value in config.items():
            logger.info(f"  - {key}: {value}")

        # Запуск анализа в фоновом потоке
        logger.info("Запуск рабочего потока анализа...")
        self.run_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(0)

        self.worker = AnalysisWorker(config)
        self.worker.progress.connect(self.on_analysis_progress)
        self.worker.finished.connect(self.on_analysis_finished)
        self.worker.start()
        logger.info("✓ Рабочий поток запущен")

    def on_analysis_progress(self, percent, message):
        """Обработчик прогресса анализа"""
        self.progress_bar.setValue(percent)
        self.progress_label.setText(message)

    def on_analysis_finished(self, success, result):
        """Обработчик завершения анализа"""
        self.run_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)

        if success:
            logger.info("Анализ завершен успешно, отображение результатов...")
            self.analysis_results = result
            self.show_results(result)
            self.export_button.setEnabled(True)

            # Предложить автоматическое сохранение
            from PyQt6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self,
                "Анализ завершен успешно!",
                "Результаты готовы!\n\nХотите сохранить их в Excel прямо сейчас?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                logger.info("Пользователь выбрал автосохранение в Excel")
                self.export_results()
            else:
                logger.info("Пользователь отказался от автосохранения")
                show_message_box(
                    self,
                    "Готово",
                    "Результаты отображены ниже. Вы можете сохранить их позже кнопкой '💾 Сохранить в Excel'",
                    "info"
                )
        else:
            show_message_box(
                self,
                "Ошибка",
                f"Произошла ошибка при выполнении анализа:\n\n{result}",
                "error"
            )

    def show_results(self, results):
        """Показать результаты анализа"""
        logger.info("Отображение результатов пользователю...")

        try:
            self.results_card.setVisible(True)

            # Формирование сводки
            hist_df = results.get('historical')
            forecast_df = results.get('forecast')

            logger.info("Формирование краткой сводки...")
            summary = f"""
        <h2 style='color: {NornikColors.PRIMARY_BLUE}; border-bottom: 2px solid {NornikColors.PRIMARY_BLUE}; padding-bottom: 10px;'>
        📊 Результаты анализа запасов
        </h2>

        <div style='background-color: #f0f5ff; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: {NornikColors.PRIMARY_BLUE}; margin-top: 0;'>📈 Исторический анализ:</h3>
        <ul style='font-size: 14px; line-height: 1.8;'>
            <li><b>Материалов:</b> {hist_df['Материал'].nunique() if 'Материал' in hist_df.columns else len(hist_df)}</li>
            <li><b>Филиалов:</b> {hist_df['Филиал'].nunique() if 'Филиал' in hist_df.columns else 'N/A'}</li>
            <li><b>Всего записей:</b> {len(hist_df)}</li>
            <li><b>Рассчитано метрик:</b> {len(hist_df.columns)}</li>
        </ul>
        </div>

        <div style='background-color: #f0fff0; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h3 style='color: {NornikColors.SUCCESS}; margin-top: 0;'>📦 Прогноз и закупки:</h3>
        <ul style='font-size: 14px; line-height: 1.8;'>
            <li><b>Всего прогнозов:</b> {len(forecast_df)}</li>
            <li><b>Рекомендаций по закупкам:</b> {(forecast_df['Рекомендация по закупке'] > 0).sum() if 'Рекомендация по закупке' in forecast_df.columns else 0}</li>
            <li><b>Объем закупок:</b> {forecast_df['Рекомендация по закупке'].sum():.2f} ед.</li>
        </ul>
        </div>

        <hr style='border: 2px solid {NornikColors.PRIMARY_BLUE}; margin: 30px 0;'>

        <div style='background-color: #fffef0; padding: 20px; border-radius: 10px; border-left: 5px solid {NornikColors.ACCENT_ORANGE};'>
        <h3 style='color: {NornikColors.ACCENT_ORANGE}; margin-top: 0;'>📄 Файлы с результатами:</h3>
        <p style='font-size: 14px; line-height: 1.8;'>
        При сохранении будут созданы:<br>
        • <b>Excel файл</b> - таблицы со всеми данными и расчетами<br>
        • <b>Исторический_анализ.md</b> - подробные пояснения расчетов исторических метрик<br>
        • <b>Прогноз_закупки.md</b> - подробные пояснения расчетов прогноза<br>
        </p>
        </div>

        <p style='color: white; background-color: {NornikColors.SUCCESS}; font-weight: bold; font-size: 16px; text-align: center; padding: 15px; border-radius: 10px; margin-top: 30px;'>
        ✅ Анализ завершен! Нажмите "💾 Сохранить в Excel" для экспорта результатов
        </p>
            """
            logger.info("✓ HTML сводка сформирована")

            logger.info("Установка текста в QLabel...")
            self.results_label.setText(summary)
            logger.info("✓ Результаты отображены в UI")

        except Exception as e:
            logger.error(f"Ошибка при отображении результатов: {e}")
            logger.error(traceback.format_exc())

            # Показать минимальную версию
            try:
                simple_summary = f"""
                <h2 style='color: {NornikColors.PRIMARY_BLUE};'>📊 Результаты анализа запасов</h2>

                <p style='font-size: 16px;'><b>✅ Анализ завершен успешно!</b></p>

                <p style='color: {NornikColors.SUCCESS}; font-weight: bold; font-size: 14px;'>
                Нажмите "💾 Сохранить в Excel" для просмотра результатов
                </p>
                """
                self.results_label.setText(simple_summary)
                logger.info("✓ Показана минимальная версия результатов")
            except Exception as e2:
                logger.error(f"Критическая ошибка отображения: {e2}")
                logger.error(traceback.format_exc())

    def export_results(self):
        """Экспортировать результаты в Excel"""
        if not self.analysis_results:
            show_message_box(
                self,
                "Ошибка",
                "Нет результатов для экспорта. Сначала выполните анализ.",
                "error"
            )
            return

        # Диалог сохранения
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить результаты",
            f"Анализ_запасов_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel Files (*.xlsx)"
        )

        if file_path:
            # Экспорт
            success = export_full_report(
                file_path,
                df_historical=self.analysis_results['historical'],
                explanation_historical=self.analysis_results['historical_explanation'],
                df_forecast=self.analysis_results['forecast'],
                explanation_forecast=self.analysis_results['forecast_explanation']
            )

            if success:
                show_message_box(
                    self,
                    "Успех",
                    f"Результаты успешно сохранены в:\n{file_path}",
                    "success"
                )
            else:
                show_message_box(
                    self,
                    "Ошибка",
                    "Не удалось сохранить файл",
                    "error"
                )

    def show_help(self):
        """Показать справку"""
        help_text = """
        <h2 style='color: #0077C8;'>Справка по использованию</h2>

        <h3>Порядок работы:</h3>
        <ol>
            <li><b>Загрузите исторические данные</b> - Excel файл с остатками материалов</li>
            <li><b>Выберите режим прогнозирования:</b>
                <ul>
                    <li>Загрузите готовый прогноз ИЛИ</li>
                    <li>Используйте автоматический прогноз (рекомендуется)</li>
                </ul>
            </li>
            <li><b>Настройте параметры</b> (опционально)</li>
            <li><b>Нажмите "Выполнить анализ"</b></li>
            <li><b>Сохраните результаты в Excel</b></li>
        </ol>

        <h3>📊 СТРУКТУРА ФАЙЛА ИСТОРИЧЕСКИХ ДАННЫХ:</h3>

        <h4 style='color: #004C97;'>✅ Обязательные колонки:</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0;'>
            <tr style='background-color: #004C97; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Формат</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Дата, Date, Период, Month, Месяц</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Дата (ГГГГ-ММ-ДД)</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Материал, Material, Товар, Артикул, SKU, Item</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Текст</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Начальный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Начальный остаток, Start Balance, Остаток на начало</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Конечный остаток</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Конечный остаток, End Balance, Остаток на конец</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            </tr>
        </table>

        <h4 style='color: #0077C8;'>⭐ Рекомендуемые колонки (для точного анализа):</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0;'>
            <tr style='background-color: #0077C8; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Формат</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Филиал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Филиал, Branch, Склад, Warehouse, Подразделение</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Текст</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Потребление</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Потребление, Consumption, Расход, Usage, Использование</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Стоимость</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Стоимость, Cost, Цена, Price, Стоимость конечная</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            </tr>
        </table>

        <h4 style='color: #FF9800;'>⚠️ Важно:</h4>
        <ul>
            <li>Формат файла: <b>.xlsx</b> или <b>.xls</b></li>
            <li>Даты должны быть в <b>формате даты</b> (не текст!)</li>
            <li>Числа должны быть в <b>числовом формате</b> (не текст!)</li>
            <li>Минимум данных: <b>6-12 месяцев истории</b></li>
            <li>Рекомендуется: <b>12-24 месяца</b> для точного прогноза</li>
        </ul>

        <h3>📈 СТРУКТУРА ФАЙЛА ПРОГНОЗНЫХ ДАННЫХ (опционально):</h3>

        <h4 style='color: #004C97;'>✅ Обязательные колонки:</h4>
        <table style='width: 100%; border-collapse: collapse; margin: 10px 0;'>
            <tr style='background-color: #004C97; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонка</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Варианты названий</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Формат</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Дата</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Дата, Date, Период</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Дата (ГГГГ-ММ-ДД)</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Материал</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Материал, Material, Товар</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Текст</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>Плановый спрос</b></td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Плановый спрос, Demand, Forecast, Прогноз, План</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Число</td>
            </tr>
        </table>

        <p style='background-color: #E3F2FD; padding: 10px; border-radius: 5px;'>
        <b>💡 Совет:</b> Вместо загрузки прогнозного файла используйте режим
        <b>"Автоматический прогноз"</b> - система сама сгенерирует прогноз на основе исторических данных!
        </p>

        <h3>📞 Техническая поддержка:</h3>
        <p>При возникновении вопросов обратитесь в службу технической поддержки Норникель Спутник.</p>

        <h3>📁 Шаблоны файлов:</h3>
        <p>Примеры правильно оформленных файлов находятся в папке: <br>
        <code>C:\\dev\\analysis\\datasets\\</code></p>

        <h4 style='color: #004C97;'>Два готовых шаблона на выбор:</h4>

        <table style='width: 100%; border-collapse: collapse; margin: 10px 0;'>
            <tr style='background-color: #004C97; color: white;'>
                <th style='padding: 8px; border: 1px solid #ddd;'>Шаблон</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Колонок</th>
                <th style='padding: 8px; border: 1px solid #ddd;'>Когда использовать</th>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>historical_data_template.xlsx</b><br>(упрощенный)</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>7</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Нет данных о поступлениях и ценах.<br>Все 7 колонок используются приложением.</td>
            </tr>
            <tr>
                <td style='padding: 8px; border: 1px solid #ddd;'><b>historical_data_correct_template.xlsx</b><br>(полный) ⭐</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>9</td>
                <td style='padding: 8px; border: 1px solid #ddd;'>Есть данные о поступлениях и ценах.<br>7 колонок используются приложением,<br>2 колонки (Поступление, Цена) - для прозрачности.</td>
            </tr>
        </table>

        <h4 style='color: #FF9800;'>⚡ ВАЖНО: Какие поля обязательны?</h4>

        <p style='background-color: #FFF3E0; padding: 10px; border-radius: 5px; border-left: 4px solid #FF9800;'>
        <b>Минимум для работы (4 поля):</b><br>
        ✅ Дата<br>
        ✅ Материал<br>
        ✅ Начальный остаток<br>
        ✅ Конечный остаток<br>
        <br>
        <b>Крайне рекомендуется (1 поле):</b><br>
        ⭐⭐⭐ <b>Потребление</b> - БЕЗ этого поля прогноз будет менее точным!<br>
        <br>
        <b>Рекомендуется (2 поля):</b><br>
        ⭐ Филиал - для анализа по складам<br>
        ⭐ Конечная стоимость - для расчета opportunity cost<br>
        <br>
        <b>Дополнительно (не используются приложением):</b><br>
        📊 Поступление - для балансового уравнения (только в полном шаблоне)<br>
        📊 Цена за единицу - для расчета стоимости (только в полном шаблоне)
        </p>

        <h4 style='color: #4CAF50;'>✅ Упрощенный шаблон (7 колонок):</h4>
        <p style='font-family: monospace; background-color: #E8F5E9; padding: 10px; border-radius: 5px;'>
        1. Дата ✅<br>
        2. Филиал ⭐<br>
        3. Материал ✅<br>
        4. Начальный остаток ✅<br>
        5. Конечный остаток ✅<br>
        6. Потребление ⭐⭐⭐<br>
        7. Конечная стоимость ⭐
        </p>
        <p><b>Все 7 колонок используются приложением!</b></p>

        <h4 style='color: #2196F3;'>⭐ Полный шаблон (9 колонок):</h4>
        <p style='font-family: monospace; background-color: #E3F2FD; padding: 10px; border-radius: 5px;'>
        1. Дата ✅<br>
        2. Филиал ⭐<br>
        3. Материал ✅<br>
        4. Начальный остаток ✅<br>
        5. <b>Поступление 📊</b> (не используется приложением - для прозрачности)<br>
        6. Потребление ⭐⭐⭐<br>
        7. Конечный остаток ✅<br>
        8. <b>Цена за единицу 📊</b> (не используется приложением - для расчетов в Excel)<br>
        9. Конечная стоимость ⭐
        </p>
        <p><b>7 из 9 колонок используются приложением!</b><br>
        2 дополнительные колонки для полноты данных и балансового уравнения:<br>
        <code>Конечный остаток = Начальный остаток + Поступление - Потребление</code></p>

        <p style='background-color: #E3F2FD; padding: 10px; border-radius: 5px;'>
        <b>💡 Вывод:</b> Оба шаблона корректно работают с приложением!<br>
        Используйте <b>упрощенный</b> (7 колонок) для большинства случаев.<br>
        Используйте <b>полный</b> (9 колонок) если хотите видеть балансовое уравнение.
        </p>
        """

        msg = QMessageBox(self)
        msg.setWindowTitle("Справка")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(help_text)
        msg.setStyleSheet(get_message_box_style("info"))
        msg.exec()


def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)

    # Настройки приложения
    app.setApplicationName("Норникель Спутник - Анализ запасов")
    app.setOrganizationName("Норникель Спутник")

    # Применить глобальные стили
    app.setStyleSheet(get_scrollbar_style())

    # Создать и показать главное окно
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
