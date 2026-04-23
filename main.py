# main.py — точка входа

import sys
from PyQt6.QtWidgets import QApplication

from app.ui.windows.main_window import MainWindow
from app.core.theme.dark_theme import get_dark_stylesheet
from app.core.logging.logger_config import setup_logger

from loguru import logger

setup_logger()


def main():
    app = QApplication(sys.argv)

    # Тема
    app.setStyleSheet(get_dark_stylesheet())
    logger.info("Торгово-аналитическая платформа MS запущена")

    # Главное окно
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()