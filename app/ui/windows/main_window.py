from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from app.ui.sidebar.sidebar_widget import SidebarWidget
from app.ui.pages.analytics_page import AnalyticsPage
from app.ui.pages.oi_page import OiPage
from app.ui.pages.price_page import PricePage
from app.ui.pages.logs_page import LogsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Торгово-аналитическая платформа MS")
        self.setMinimumSize(1000, 600)

        # --- центральный виджет ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        central_widget.setLayout(main_layout)

        # --- sidebar ---
        self.sidebar = SidebarWidget()
        self.sidebar.setFixedWidth(200)

        # --- страницы ---
        self.stack = QStackedWidget()

        self.analytics_page = AnalyticsPage()
        self.oi_page = OiPage()
        self.price_page = PricePage()
        self.logs_page = LogsPage()

        self.stack.addWidget(self.analytics_page)  # 0
        self.stack.addWidget(self.oi_page)         # 1
        self.stack.addWidget(self.price_page)      # 2
        self.stack.addWidget(self.logs_page)       # 3

        # --- сборка ---
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)


        # --- связи ---
        self.sidebar.analytics_button.clicked.connect(lambda: self.switch_page(0))
        self.sidebar.oi_button.clicked.connect(lambda: self.switch_page(1))
        self.sidebar.price_button.clicked.connect(lambda: self.switch_page(2))
        self.sidebar.logs_button.clicked.connect(lambda: self.switch_page(3))

        # --- дефолт ---
        self.switch_page(0)

    def switch_page(self, index: int):
        self.stack.setCurrentIndex(index)