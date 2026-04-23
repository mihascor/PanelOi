from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton



class SidebarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")

        layout = QVBoxLayout()
        

        # кнопки навигации
        self.analytics_button = QPushButton("Аналитика")
        self.oi_button = QPushButton("ОИ")
        self.price_button = QPushButton("Цены")
        self.logs_button = QPushButton("Логи")

        # добавляем в layout
        layout.addWidget(self.analytics_button)
        layout.addWidget(self.oi_button)
        layout.addWidget(self.price_button)
        layout.addWidget(self.logs_button)

        layout.addStretch()

        self.setLayout(layout)