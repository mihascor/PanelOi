from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Здесь будет аналитическая таблица")
        layout.addWidget(label)

        self.setLayout(layout)