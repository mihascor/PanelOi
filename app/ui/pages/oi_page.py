from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class OiPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Страница ОИ")
        layout.addWidget(label)

        self.setLayout(layout)