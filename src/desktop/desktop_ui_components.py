
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))
"""
Переиспользуемые UI компоненты для desktop приложения Норникель Спутник.
"""

from PyQt6.QtWidgets import (
    QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout,
    QWidget, QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor
from src.desktop.desktop_ui_styles import *


class NornikPrimaryButton(QPushButton):
    """Основная кнопка в фирменном стиле"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_primary_button_style())
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class NornikSecondaryButton(QPushButton):
    """Вторичная кнопка в фирменном стиле"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_secondary_button_style())
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class NornikTitleLabel(QLabel):
    """Заголовок в фирменном стиле"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_label_title_style())
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class NornikHeadingLabel(QLabel):
    """Подзаголовок в фирменном стиле"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_label_heading_style())


class NornikCaptionLabel(QLabel):
    """Подпись в фирменном стиле"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(get_label_caption_style())


class NornikCard(QFrame):
    """Карточка (металлическая деталь) в фирменном стиле"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_card_style())
        self.setFrameShape(QFrame.Shape.StyledPanel)


class FileUploadCard(QFrame):
    """Карточка загрузки файла"""
    file_selected = pyqtSignal(str)  # Сигнал при выборе файла

    def __init__(self, title, description, file_type="Excel", parent=None):
        super().__init__(parent)
        self.file_path = None
        self.file_type = file_type

        # Основной макет
        layout = QVBoxLayout()
        layout.setSpacing(NornikMetrics.PADDING_MEDIUM)

        # Заголовок
        title_label = NornikHeadingLabel(title)
        layout.addWidget(title_label)

        # Описание
        desc_label = NornikCaptionLabel(description)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Метка с именем файла
        self.file_label = QLabel("Файл не выбран")
        self.file_label.setStyleSheet(f"""
            QLabel {{
                color: {NornikColors.TEXT_SECONDARY};
                font-size: {NornikFonts.SIZE_BODY}px;
                padding: {NornikMetrics.PADDING_SMALL}px;
                background-color: {NornikColors.BACKGROUND};
                border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
            }}
        """)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)

        # Кнопка выбора файла
        self.select_btn = NornikSecondaryButton(f"📁 Выбрать {file_type} файл")
        self.select_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_btn)

        # Индикатор статуса
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"font-size: {NornikFonts.SIZE_CAPTION}px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setStyleSheet(get_file_upload_style())

    def select_file(self):
        """Открыть диалог выбора файла"""
        file_filter = "Excel Files (*.xlsx *.xls)"
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Выберите {self.file_type} файл",
            "",
            file_filter
        )

        if file_path:
            self.file_path = file_path
            # Показать только имя файла
            import os
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"✓ {file_name}")
            self.file_label.setStyleSheet(f"""
                QLabel {{
                    color: {NornikColors.SUCCESS};
                    font-size: {NornikFonts.SIZE_BODY}px;
                    font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
                    padding: {NornikMetrics.PADDING_SMALL}px;
                    background-color: #E8F5E9;
                    border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
                }}
            """)
            self.status_label.setText("")
            self.file_selected.emit(file_path)

    def set_status(self, message, status_type="info"):
        """Установить статус (info, success, warning, error)"""
        color_map = {
            "info": NornikColors.INFO,
            "success": NornikColors.SUCCESS,
            "warning": NornikColors.WARNING,
            "error": NornikColors.ERROR
        }
        color = color_map.get(status_type, NornikColors.INFO)

        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: {NornikFonts.SIZE_CAPTION}px;
                font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
            }}
        """)

    def clear(self):
        """Очистить выбор файла"""
        self.file_path = None
        self.file_label.setText("Файл не выбран")
        self.file_label.setStyleSheet(f"""
            QLabel {{
                color: {NornikColors.TEXT_SECONDARY};
                font-size: {NornikFonts.SIZE_BODY}px;
                padding: {NornikMetrics.PADDING_SMALL}px;
                background-color: {NornikColors.BACKGROUND};
                border-radius: {NornikMetrics.BORDER_RADIUS_SMALL}px;
            }}
        """)
        self.status_label.setText("")


class NornikProgressBar(QProgressBar):
    """Прогресс-бар в фирменном стиле"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(get_progress_bar_style())
        self.setTextVisible(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


class NornikHeader(QWidget):
    """Шапка приложения с логотипом"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Основной макет
        layout = QHBoxLayout()
        layout.setContentsMargins(
            NornikMetrics.PADDING_LARGE,
            NornikMetrics.PADDING_MEDIUM,
            NornikMetrics.PADDING_LARGE,
            NornikMetrics.PADDING_MEDIUM
        )

        # Логотип (текстовая версия, т.к. нет изображения)
        logo_container = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setSpacing(0)

        logo_text = QLabel("НОРНИКЕЛЬ")
        logo_text.setStyleSheet(f"""
            QLabel {{
                font-size: 20px;
                font-weight: {NornikFonts.WEIGHT_BOLD};
                color: {NornikColors.DARK_BLUE};
                letter-spacing: 2px;
            }}
        """)

        subtitle_text = QLabel("СПУТНИК")
        subtitle_text.setStyleSheet(f"""
            QLabel {{
                font-size: {NornikFonts.SIZE_CAPTION}px;
                font-weight: {NornikFonts.WEIGHT_REGULAR};
                color: {NornikColors.GRAY};
                letter-spacing: 3px;
            }}
        """)

        logo_layout.addWidget(logo_text)
        logo_layout.addWidget(subtitle_text)
        logo_container.setLayout(logo_layout)

        layout.addWidget(logo_container)

        # Название приложения
        app_title = QLabel("Анализ и прогнозирование запасов")
        app_title.setStyleSheet(f"""
            QLabel {{
                font-size: {NornikFonts.SIZE_HEADING}px;
                font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
                color: {NornikColors.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(app_title, 1, Qt.AlignmentFlag.AlignCenter)

        # Добавить растяжку справа для баланса
        layout.addStretch()

        # Фон шапки
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {NornikColors.WHITE};
                border-bottom: 3px solid {NornikColors.PRIMARY_BLUE};
            }}
        """)

        self.setLayout(layout)
        self.setFixedHeight(80)


class InfoCard(QFrame):
    """Информационная карточка с иконкой"""

    def __init__(self, title, description, icon="ℹ️", color=None, parent=None):
        super().__init__(parent)

        if color is None:
            color = NornikColors.PRIMARY_BLUE

        layout = QHBoxLayout()
        layout.setSpacing(NornikMetrics.PADDING_MEDIUM)

        # Иконка
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                padding: {NornikMetrics.PADDING_MEDIUM}px;
            }}
        """)
        layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        # Текстовое содержимое
        content_layout = QVBoxLayout()
        content_layout.setSpacing(NornikMetrics.PADDING_SMALL)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-size: {NornikFonts.SIZE_HEADING}px;
                font-weight: {NornikFonts.WEIGHT_SEMIBOLD};
                color: {color};
            }}
        """)

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            QLabel {{
                font-size: {NornikFonts.SIZE_BODY}px;
                color: {NornikColors.TEXT_SECONDARY};
            }}
        """)

        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)

        layout.addLayout(content_layout, 1)

        self.setLayout(layout)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {NornikColors.WHITE};
                border-left: 4px solid {color};
                border-radius: {NornikMetrics.BORDER_RADIUS_MEDIUM}px;
                padding: {NornikMetrics.PADDING_MEDIUM}px;
            }}
        """)


def show_message_box(parent, title, message, message_type="info"):
    """
    Показать диалоговое окно в фирменном стиле.

    Args:
        parent: Родительский виджет
        title: Заголовок
        message: Текст сообщения
        message_type: Тип сообщения ("info", "success", "warning", "error")
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet(get_message_box_style(message_type))

    # Установить иконку
    icon_map = {
        "info": QMessageBox.Icon.Information,
        "success": QMessageBox.Icon.Information,
        "warning": QMessageBox.Icon.Warning,
        "error": QMessageBox.Icon.Critical
    }
    msg_box.setIcon(icon_map.get(message_type, QMessageBox.Icon.Information))

    return msg_box.exec()


def show_question_box(parent, title, message):
    """Показать диалог с вопросом (Да/Нет)"""
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet(get_message_box_style("info"))
    msg_box.setIcon(QMessageBox.Icon.Question)
    msg_box.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )

    # Русификация кнопок
    msg_box.button(QMessageBox.StandardButton.Yes).setText("Да")
    msg_box.button(QMessageBox.StandardButton.No).setText("Нет")

    return msg_box.exec() == QMessageBox.StandardButton.Yes
