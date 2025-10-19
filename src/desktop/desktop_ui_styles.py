"""
Стили и константы брендбука Норникель Спутник для PyQt6 приложения.

Основано на nornik.json - фирменный стиль компании.
"""

# ==================== ЦВЕТА БРЕНДА ====================
# Основные цвета Норникель Спутник
class NornikColors:
    """Фирменные цвета Норникель Спутник"""

    # Основные цвета
    PRIMARY_BLUE = "#0077C8"      # Синий (Pantone 3005)
    DARK_BLUE = "#004C97"         # Темно-синий (Pantone 2945)
    WHITE = "#FFFFFF"
    GRAY = "#626262"              # Серый (Cool Gray 10)
    LIGHT_GRAY = "#C8C8C8"        # Светло-серый (Cool Gray 3)

    # Дополнительные цвета
    TURQUOISE = "#009DA8"         # Бирюзовый (Pantone 7710 C)
    PURPLE = "#A64CDD"            # Фиолетовый (Pantone 7447 C)

    # Системные цвета для UI
    BACKGROUND = "#F5F5F5"        # Фон приложения
    SURFACE = "#FFFFFF"           # Поверхность карточек
    TEXT_PRIMARY = "#212121"      # Основной текст
    TEXT_SECONDARY = "#626262"    # Вторичный текст
    BORDER = "#E0E0E0"            # Границы

    # Статусные цвета
    SUCCESS = "#4CAF50"
    WARNING = "#FF9800"
    ERROR = "#F44336"
    INFO = PRIMARY_BLUE


# ==================== ШРИФТЫ ====================
class NornikFonts:
    """Фирменные шрифты Норникель Спутник"""

    # Основные шрифты (с fallback на системные)
    PRIMARY = "Proxima Nova, Segoe UI, Arial, sans-serif"
    SECONDARY = "IBM Plex Mono, Consolas, Courier New, monospace"
    SYSTEM = "Tahoma, Segoe UI, Arial, sans-serif"

    # Размеры шрифтов
    SIZE_TITLE = 24        # Заголовки
    SIZE_HEADING = 18      # Подзаголовки
    SIZE_BODY = 14         # Основной текст
    SIZE_CAPTION = 12      # Подписи
    SIZE_SMALL = 10        # Мелкий текст

    # Вес шрифтов
    WEIGHT_LIGHT = 300
    WEIGHT_REGULAR = 400
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700


# ==================== РАЗМЕРЫ И ОТСТУПЫ ====================
class NornikMetrics:
    """Размеры и отступы для UI элементов"""

    # Отступы
    PADDING_SMALL = 8
    PADDING_MEDIUM = 16
    PADDING_LARGE = 24
    PADDING_XLARGE = 32

    # Закругления углов (металлические детали имеют скругленные углы)
    BORDER_RADIUS_SMALL = 4
    BORDER_RADIUS_MEDIUM = 8
    BORDER_RADIUS_LARGE = 12

    # Размеры элементов
    BUTTON_HEIGHT = 40
    INPUT_HEIGHT = 36
    LOGO_HEIGHT = 60
    ICON_SIZE_SMALL = 16
    ICON_SIZE_MEDIUM = 24
    ICON_SIZE_LARGE = 32


# ==================== QSS СТИЛИ (Qt Style Sheets) ====================

def get_main_window_style():
    """Стиль главного окна приложения"""
    return f"""
    QMainWindow {{
        background-color: {NornikColors.BACKGROUND};
    }}

    QWidget {{
        font-family: {NornikFonts.SYSTEM};
        font-size: {NornikFonts.SIZE_BODY}px;
        color: {NornikColors.TEXT_PRIMARY};
    }}
    """


def get_primary_button_style():
    """Стиль основной кнопки (синяя)"""
    return f"""
    QPushButton {{
        background-color: {NornikColors.PRIMARY_BLUE};
        color: {NornikColors.WHITE};
        border: none;
        border-radius: {NornikMetrics.BORDER_RADIUS_MEDIUM}px;
        padding: {NornikMetrics.PADDING_MEDIUM}px {NornikMetrics.PADDING_LARGE}px;
        font-size: {NornikFonts.SIZE_BODY}px;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
        min-height: {NornikMetrics.BUTTON_HEIGHT}px;
    }}

    QPushButton:hover {{
        background-color: {NornikColors.DARK_BLUE};
    }}

    QPushButton:pressed {{
        background-color: #003366;
    }}

    QPushButton:disabled {{
        background-color: {NornikColors.LIGHT_GRAY};
        color: {NornikColors.GRAY};
    }}
    """


def get_secondary_button_style():
    """Стиль вторичной кнопки (белая с рамкой)"""
    return f"""
    QPushButton {{
        background-color: {NornikColors.WHITE};
        color: {NornikColors.PRIMARY_BLUE};
        border: 2px solid {NornikColors.PRIMARY_BLUE};
        border-radius: {NornikMetrics.BORDER_RADIUS_MEDIUM}px;
        padding: {NornikMetrics.PADDING_MEDIUM}px {NornikMetrics.PADDING_LARGE}px;
        font-size: {NornikFonts.SIZE_BODY}px;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
        min-height: {NornikMetrics.BUTTON_HEIGHT}px;
    }}

    QPushButton:hover {{
        background-color: {NornikColors.PRIMARY_BLUE};
        color: {NornikColors.WHITE};
    }}

    QPushButton:pressed {{
        background-color: {NornikColors.DARK_BLUE};
    }}

    QPushButton:disabled {{
        background-color: {NornikColors.BACKGROUND};
        color: {NornikColors.LIGHT_GRAY};
        border-color: {NornikColors.LIGHT_GRAY};
    }}
    """


def get_file_upload_style():
    """Стиль области загрузки файлов"""
    return f"""
    QFrame {{
        background-color: {NornikColors.WHITE};
        border: 2px dashed {NornikColors.PRIMARY_BLUE};
        border-radius: {NornikMetrics.BORDER_RADIUS_LARGE}px;
        padding: {NornikMetrics.PADDING_LARGE}px;
    }}

    QFrame:hover {{
        border-color: {NornikColors.DARK_BLUE};
        background-color: #F0F8FF;
    }}
    """


def get_input_style():
    """Стиль полей ввода"""
    return f"""
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {NornikColors.WHITE};
        border: 1px solid {NornikColors.BORDER};
        border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        padding: {NornikMetrics.PADDING_SMALL}px {NornikMetrics.PADDING_MEDIUM}px;
        font-size: {NornikFonts.SIZE_BODY}px;
        min-height: {NornikMetrics.INPUT_HEIGHT}px;
    }}

    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 2px solid {NornikColors.PRIMARY_BLUE};
    }}

    QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
        background-color: {NornikColors.BACKGROUND};
        color: {NornikColors.GRAY};
    }}
    """


def get_card_style():
    """Стиль карточки (металлическая деталь)"""
    return f"""
    QFrame {{
        background-color: {NornikColors.WHITE};
        border: 1px solid {NornikColors.BORDER};
        border-radius: {NornikMetrics.BORDER_RADIUS_LARGE}px;
        padding: {NornikMetrics.PADDING_LARGE}px;
    }}
    """


def get_table_style():
    """Стиль таблиц"""
    return f"""
    QTableWidget {{
        background-color: {NornikColors.WHITE};
        border: 1px solid {NornikColors.BORDER};
        border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        gridline-color: {NornikColors.BORDER};
        font-size: {NornikFonts.SIZE_BODY}px;
    }}

    QTableWidget::item {{
        padding: {NornikMetrics.PADDING_SMALL}px;
    }}

    QTableWidget::item:selected {{
        background-color: {NornikColors.PRIMARY_BLUE};
        color: {NornikColors.WHITE};
    }}

    QHeaderView::section {{
        background-color: {NornikColors.DARK_BLUE};
        color: {NornikColors.WHITE};
        padding: {NornikMetrics.PADDING_MEDIUM}px;
        border: none;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
    }}
    """


def get_progress_bar_style():
    """Стиль прогресс-бара"""
    return f"""
    QProgressBar {{
        background-color: {NornikColors.BACKGROUND};
        border: 1px solid {NornikColors.BORDER};
        border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        text-align: center;
        color: {NornikColors.TEXT_PRIMARY};
        font-size: {NornikFonts.SIZE_BODY}px;
        height: 24px;
    }}

    QProgressBar::chunk {{
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {NornikColors.PRIMARY_BLUE},
            stop:1 {NornikColors.DARK_BLUE}
        );
        border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
    }}
    """


def get_label_title_style():
    """Стиль заголовка"""
    return f"""
    QLabel {{
        font-size: {NornikFonts.SIZE_TITLE}px;
        font-weight: {NornikFonts.WEIGHT_BOLD};
        color: {NornikColors.DARK_BLUE};
        padding: {NornikMetrics.PADDING_MEDIUM}px 0;
    }}
    """


def get_label_heading_style():
    """Стиль подзаголовка"""
    return f"""
    QLabel {{
        font-size: {NornikFonts.SIZE_HEADING}px;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
        color: {NornikColors.PRIMARY_BLUE};
        padding: {NornikMetrics.PADDING_SMALL}px 0;
    }}
    """


def get_label_caption_style():
    """Стиль подписи"""
    return f"""
    QLabel {{
        font-size: {NornikFonts.SIZE_CAPTION}px;
        color: {NornikColors.TEXT_SECONDARY};
    }}
    """


def get_scrollbar_style():
    """Стиль скроллбара"""
    return f"""
    QScrollBar:vertical {{
        background-color: {NornikColors.BACKGROUND};
        width: 12px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background-color: {NornikColors.LIGHT_GRAY};
        border-radius: 6px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {NornikColors.GRAY};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    QScrollBar:horizontal {{
        background-color: {NornikColors.BACKGROUND};
        height: 12px;
        margin: 0;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {NornikColors.LIGHT_GRAY};
        border-radius: 6px;
        min-width: 20px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background-color: {NornikColors.GRAY};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0;
    }}
    """


def get_tab_widget_style():
    """Стиль вкладок"""
    return f"""
    QTabWidget::pane {{
        border: 1px solid {NornikColors.BORDER};
        border-radius: {NornikMetrics.BORDER_RADIUS_MEDIUM}px;
        background-color: {NornikColors.WHITE};
        padding: {NornikMetrics.PADDING_MEDIUM}px;
    }}

    QTabBar::tab {{
        background-color: {NornikColors.BACKGROUND};
        color: {NornikColors.TEXT_SECONDARY};
        padding: {NornikMetrics.PADDING_MEDIUM}px {NornikMetrics.PADDING_LARGE}px;
        border: 1px solid {NornikColors.BORDER};
        border-bottom: none;
        border-top-left-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        border-top-right-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        margin-right: 4px;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
    }}

    QTabBar::tab:selected {{
        background-color: {NornikColors.PRIMARY_BLUE};
        color: {NornikColors.WHITE};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {NornikColors.LIGHT_GRAY};
    }}
    """


def get_message_box_style(message_type="info"):
    """Стиль диалоговых окон"""
    color_map = {
        "info": NornikColors.INFO,
        "success": NornikColors.SUCCESS,
        "warning": NornikColors.WARNING,
        "error": NornikColors.ERROR
    }
    color = color_map.get(message_type, NornikColors.INFO)

    return f"""
    QMessageBox {{
        background-color: {NornikColors.WHITE};
    }}

    QMessageBox QLabel {{
        color: {NornikColors.TEXT_PRIMARY};
        font-size: {NornikFonts.SIZE_BODY}px;
    }}

    QMessageBox QPushButton {{
        background-color: {color};
        color: {NornikColors.WHITE};
        border: none;
        border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
        padding: {NornikMetrics.PADDING_SMALL}px {NornikMetrics.PADDING_LARGE}px;
        min-width: 80px;
        font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
    }}

    QMessageBox QPushButton:hover {{
        background-color: {NornikColors.DARK_BLUE};
    }}
    """
