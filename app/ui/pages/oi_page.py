from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from app.services.build_oi_summary import build_oi_summary
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLabel


class OiPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.summary_label = QLabel()

        # --- кнопка обновления ---
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setFixedHeight(40)

        # --- поле вывода ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Инструмент",
            "С даты",
            "По дату",
            "Статус"
        ])

        # растягиваем таблицу
        self.table.horizontalHeader().setStretchLastSection(True)

        # --- сборка ---
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.table)
        layout.addWidget(self.summary_label)

        self.setLayout(layout)

        # --- связи ---
        self.refresh_button.clicked.connect(self.load_data)

        # --- первичная загрузка ---
        self.load_data()

    def load_data(self):
        data = build_oi_summary()
        rows = data["rows"]

        total = data["total"]
        with_data = data["with_data"]
        empty = data["empty"]

        self.table.clearContents()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(row["paper"]))
            self.table.setItem(i, 1, QTableWidgetItem(row["min_date"]))
            self.table.setItem(i, 2, QTableWidgetItem(row["max_date"]))
            self.table.setItem(i, 3, QTableWidgetItem(row["status"]))

        self.summary_label.setText(
            f"📊 Всего: {total}   |   ✅ {with_data}   |   ❌ {empty}"
        )

    