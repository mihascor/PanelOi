from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PricePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Страница цен")
        layout.addWidget(label)

        self.setLayout(layout)