from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from app.services.load_logs_to_ui import load_logs_to_ui


class LogsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # --- кнопка обновления ---
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.setFixedHeight(40)

        # --- поле логов ---
        self.logs_output = QTextEdit()
        self.logs_output.setReadOnly(True)

        # --- сборка ---
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.logs_output)

        self.setLayout(layout)

        # --- связи ---
        self.refresh_button.clicked.connect(self.load_logs)

        # --- первичная загрузка ---
        self.load_logs()

    def format_logs_to_html(self, logs: str) -> str:
        """
        Преобразует лог в HTML с подсветкой уровней
        """

        html_lines = []

        for line in logs.splitlines():
            if "ERROR" in line:
                color = "#ff6b6b"  # красный
            elif "WARNING" in line:
                color = "#f1c40f"  # жёлтый
            elif "SUCCESS" in line:
                color = "#2ecc71"  # зелёный
            else:
                color = "#aaaaaa"  # серый (INFO)

            html_lines.append(f'<span style="color:{color}">{line}</span>')

        return "<br>".join(html_lines)
    
    def load_logs(self):
        logs_text = load_logs_to_ui()

        # защита от слишком большого текста
        logs_text = logs_text[:50000]

        html = self.format_logs_to_html(logs_text)
        self.logs_output.setHtml(html)