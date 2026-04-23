from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class ControlTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.control = QTextEdit()
        self.control.setReadOnly(True)
        self.control.setPlaceholderText("Control will appear here...")

        layout.addWidget(self.control)
        self.setLayout(layout)