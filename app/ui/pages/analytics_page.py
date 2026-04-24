import json
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.services.build_oi_analytics import build_oi_analytics_data


BASE_DIR = Path(__file__).resolve().parents[3]
STATE_PATH = BASE_DIR / "storage" / "state" / "analytics_choice.json"


class AnalysisWindow(QDialog):
    def __init__(self, paper: str):
        super().__init__()

        self.setWindowTitle(f"Анализ: {paper}")

        layout = QVBoxLayout()

        title_label = QLabel(paper)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
            }
            """
        )

        layout.addWidget(title_label)
        self.setLayout(layout)

        self.setStyleSheet(
            """
            QDialog {
                background-color: #1e1e1e;
            }
            """
        )


class AnalyticsPage(QWidget):
    columns = [
        "futures",
        "paper",
        "FIZ_long",
        "FIZ_short",
        "YUR_long",
        "YUR_short",
        "direction",
        "FIZ_koof",
        "YUR_koof",
        "choice",
        "analysis",
    ]

    choice_highlight_columns = [
        "futures",
        "paper",
        "FIZ_long",
        "FIZ_short",
        "YUR_long",
        "YUR_short",
    ]

    def __init__(self):
        super().__init__()

        self.analytics_data = []
        self.selected_futures = self.load_analytics_choice_state()
        self.choice_buttons = {}

        self.table = QTableWidget()
        self.setup_analytics_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_analytics_table()

    def setup_analytics_table(self) -> None:
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.verticalHeader().setVisible(False)

        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet(
            """
            QTableWidget {
                background-color: #1e1e1e;
                alternate-background-color: #252525;
                color: #ffffff;
                gridline-color: #3a3a3a;
                border: 1px solid #3a3a3a;
            }

            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #3a3a3a;
                padding: 6px;
            }

            QTableWidget::item {
                padding: 4px;
            }

            QPushButton {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 4px 8px;
            }

            QPushButton:hover {
                background-color: #444444;
            }

            QPushButton:checked {
                background-color: #8a6d1f;
                color: #ffffff;
                border: 1px solid #c9a227;
                font-weight: bold;
            }
            """
        )

    def load_analytics_table(self) -> None:
        self.analytics_data = build_oi_analytics_data()

        self.table.setRowCount(len(self.analytics_data))
        self.choice_buttons.clear()

        for row_index, oi_row in enumerate(self.analytics_data):
            self.fill_analytics_row(row_index, oi_row)

        self.table.resizeColumnsToContents()

    def fill_analytics_row(self, row_index: int, oi_row: dict) -> None:
        futures = oi_row["futures"]

        for column_index, column_name in enumerate(self.columns):
            if column_name == "choice":
                self.add_choice_button(row_index, futures)
                continue

            if column_name == "analysis":
                self.add_analysis_button(row_index, oi_row["paper"])
                continue

            item = QTableWidgetItem(str(oi_row[column_name]))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.apply_direction_style(item, column_name, oi_row)
            self.table.setItem(row_index, column_index, item)

        self.apply_choice_row_style(row_index, futures)

    def add_choice_button(self, row_index: int, futures: str) -> None:
        button = QPushButton("choice")
        button.setCheckable(True)
        button.setChecked(futures in self.selected_futures)

        button.clicked.connect(
            lambda checked, current_futures=futures, current_row=row_index: (
                self.toggle_analytics_choice(current_futures, current_row, checked)
            )
        )

        self.choice_buttons[futures] = button

        column_index = self.columns.index("choice")
        self.table.setCellWidget(row_index, column_index, button)

    def add_analysis_button(self, row_index: int, paper: str) -> None:
        button = QPushButton("analysis")
        button.clicked.connect(
            lambda checked=False, current_paper=paper: self.open_analysis_window(current_paper)
        )

        column_index = self.columns.index("analysis")
        self.table.setCellWidget(row_index, column_index, button)

    def toggle_analytics_choice(self, futures: str, row_index: int, checked: bool) -> None:
        if checked:
            self.selected_futures.add(futures)
        else:
            self.selected_futures.discard(futures)

        self.save_analytics_choice_state()
        self.apply_choice_row_style(row_index, futures)

    def apply_choice_row_style(self, row_index: int, futures: str) -> None:
        is_selected = futures in self.selected_futures

        for column_name in self.choice_highlight_columns:
            column_index = self.columns.index(column_name)
            item = self.table.item(row_index, column_index)

            if item is None:
                continue

            if is_selected:
                item.setBackground(Qt.GlobalColor.darkYellow)
                item.setForeground(Qt.GlobalColor.white)
            else:
                item.setBackground(Qt.GlobalColor.transparent)
                item.setForeground(Qt.GlobalColor.white)

    def apply_direction_style(
        self,
        item: QTableWidgetItem,
        column_name: str,
        oi_row: dict,
    ) -> None:
        if column_name != "direction":
            return

        if oi_row["direction"] == "Long":
            item.setBackground(Qt.GlobalColor.darkGreen)
            item.setForeground(Qt.GlobalColor.white)
            return

        item.setBackground(Qt.GlobalColor.darkRed)
        item.setForeground(Qt.GlobalColor.white)

    def open_analysis_window(self, paper: str) -> None:
        analysis_window = AnalysisWindow(paper)
        analysis_window.showFullScreen()
        analysis_window.exec()

    def load_analytics_choice_state(self) -> set[str]:
        if not STATE_PATH.exists():
            return set()

        try:
            with open(STATE_PATH, "r", encoding="utf-8") as file:
                state_data = json.load(file)

            return set(state_data.get("selected_futures", []))

        except (json.JSONDecodeError, OSError):
            return set()

    def save_analytics_choice_state(self) -> None:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

        state_data = {
            "selected_futures": sorted(self.selected_futures),
        }

        with open(STATE_PATH, "w", encoding="utf-8") as file:
            json.dump(state_data, file, ensure_ascii=False, indent=4)