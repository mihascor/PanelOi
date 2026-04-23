from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
)

from app.ui.tabs.system_control_tab import ControlTab
from app.ui.tabs.analysis_table_tab import TableTab


# --- Главное окно ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Торгово-аналитическая платформа MS")
        self.setMinimumSize(1000, 600)

        # --- Центральный виджет ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # --- Верхняя панель ---
        button_layout = QHBoxLayout()

        self.table_button = QPushButton("Таблица - ОИ")
        self.control_button = QPushButton("Пульт")

        self.table_button.setCheckable(True)
        self.control_button.setCheckable(True)

        button_layout.addWidget(self.table_button)
        button_layout.addWidget(self.control_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # --- Стек вкладок ---
        self.stack = QStackedWidget()

        self.table_tab = TableTab()
        self.control_tab = ControlTab()

        self.stack.addWidget(self.table_tab)   # index 0
        self.stack.addWidget(self.control_tab) # index 1

        main_layout.addWidget(self.stack)

        # --- Связка кнопок ---
        self.table_button.clicked.connect(lambda: self.switch_tab(0))
        self.control_button.clicked.connect(lambda: self.switch_tab(1))

        # --- Дефолт ---
        self.switch_tab(0)

    def switch_tab(self, index: int):
        self.stack.setCurrentIndex(index)

        # обновляем состояние кнопок
        self.table_button.setChecked(index == 0)
        self.control_button.setChecked(index == 1)