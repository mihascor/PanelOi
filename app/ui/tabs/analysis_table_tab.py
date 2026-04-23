from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)


# Таб с таблицей данных
class TableTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Таблица (заглушка)
        self.table = QTableWidget()
        self.table.setRowCount(5)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Col 1", "Col 2", "Col 3"])

        # Пример заполнения
        self.table.setItem(0, 0, QTableWidgetItem("Test"))

        layout.addWidget(self.table)

        self.setLayout(layout)