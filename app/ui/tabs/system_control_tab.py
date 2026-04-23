from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QTabWidget,
)

from app.services.load_logs_to_ui import load_logs_to_ui


class ControlTab(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        # --- Вкладки ---
        self.tabs = QTabWidget()

        # =========================
        # Вкладка ОИ
        # =========================
        oi_tab = QWidget()
        oi_layout = QVBoxLayout()

        self.load_oi_button = QPushButton("Обновить историю ОИ")

        self.oi_text = QTextEdit()
        self.oi_text.setReadOnly(True)
        self.oi_text.setPlaceholderText("Здесь будет информация по ОИ...")

        oi_layout.addWidget(self.load_oi_button)
        oi_layout.addWidget(self.oi_text)
        oi_tab.setLayout(oi_layout)

        self.tabs.addTab(oi_tab, "Работа с futures_oi")

        # =========================
        # Вкладка Цены
        # =========================
        price_tab = QWidget()
        price_layout = QVBoxLayout()

        self.load_price_button = QPushButton("Обновить историю цены")

        self.price_text = QTextEdit()
        self.price_text.setReadOnly(True)
        self.price_text.setPlaceholderText("Здесь будет информация по ценам...")

        price_layout.addWidget(self.load_price_button)
        price_layout.addWidget(self.price_text)
        price_tab.setLayout(price_layout)

        self.tabs.addTab(price_tab, "Работа с paper_price")

        # =========================
        # Вкладка Логи
        # =========================
        logs_tab = QWidget()
        logs_layout = QVBoxLayout()

        self.show_logs_button = QPushButton("Логи общие")

        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setPlaceholderText("Здесь будут отображаться логи...")

        logs_layout.addWidget(self.show_logs_button)
        logs_layout.addWidget(self.logs_text)
        logs_tab.setLayout(logs_layout)

        self.tabs.addTab(logs_tab, "Читать логи")

        # --- Сборка ---
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        # --- Связи ---
        self.show_logs_button.clicked.connect(self.show_logs)

    # =========================
    # Методы
    # =========================
    def show_logs(self):
        logs_text = load_logs_to_ui()
        self.logs_text.setPlainText(logs_text)