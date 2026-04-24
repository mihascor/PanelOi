# main.py — точка входа

import sys
import ctypes
from PyQt6.QtWidgets import QApplication

from app.ui.windows.main_window import MainWindow
from app.core.theme.dark_theme import get_dark_stylesheet
from app.core.logging.logger_config import setup_logger
from app.services.sync_price_history import PriceSyncService

from loguru import logger

setup_logger()


def main():
    app = QApplication(sys.argv)    # создаём приложение

    # Тема
    app.setStyleSheet(get_dark_stylesheet()) # устанавливаем темную тему
    logger.info("Торгово-аналитическая платформа MS запущена")

    # Главное окно
    window = MainWindow() # создаём главное окно
    PriceSyncService().sync_price_history() # синхронизируем цены при запуске
    window.showMaximized() # запускаем в развернутом виде
    # window.show()        # для отладки в окне


    # включаем тёмный заголовок (Windows 10/11)
    try:
        hwnd = window.winId()
        value = ctypes.c_int(1)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            int(hwnd),
            20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except Exception:
        pass

    sys.exit(app.exec())


if __name__ == "__main__":
    main()