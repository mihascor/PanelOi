def get_dark_stylesheet() -> str:
    """Глобальная темная тема для всего приложения"""

    return """
    /* --- БАЗА --- */
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
        font-size: 16px;
    }

    /* --- КНОПКИ --- */
    QPushButton {
        background-color: #2d2d2d;
        border: 1px solid #3c3c3c;
        padding: 6px 12px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #3a3a3a;
    }

    QPushButton:pressed {
        background-color: #505050;
    }

    /* активная кнопка */
    QPushButton:checked {
        background-color: #2a5270;
        color: white;
    }

    /* --- INPUT --- */
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #252526;
        border: 1px solid #3c3c3c;
        padding: 5px;
    }

    /* --- ТАБЛИЦЫ --- */
    QTableView {
        background-color: #1e1e1e;
        gridline-color: #3c3c3c;
        selection-background-color: #264f78;
    }

    QHeaderView::section {
        background-color: #2d2d2d;
        padding: 5px;
        border: none;
    }

    /* --- SCROLL --- */
    QScrollBar:vertical {
        background: #1e1e1e;
        width: 10px;
    }

    QScrollBar::handle:vertical {
        background: #3c3c3c;
        min-height: 20px;
    }

    /* --- УБИРАЕМ БЕЛОЕ В ТАБЛИЦЕ --- */

    QTableCornerButton::section {
        background-color: #2d2d2d;
        border: none;
    }

    QHeaderView {
        background-color: #2d2d2d;
    }

    QHeaderView::section {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }

    /* вертикальные номера строк */
    QTableView::verticalHeader {
        background-color: #2d2d2d;
    }
    /* --- TABS (QTabWidget) --- */

    QTabWidget::pane {
        border: 1px solid #3c3c3c;
        background-color: #1e1e1e;
    }

    /* сами вкладки */
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 6px 12px;
        margin-right: 2px;
        border: 1px solid #3c3c3c;
        border-bottom: none;
    }

    /* активная вкладка */
    QTabBar::tab:selected {
        background-color: #2a5270;
        color: #ffffff;
    }

    /* при наведении */
    QTabBar::tab:hover {
        background-color: #3a3a3a;
    }

    /* --- SIDEBAR --- */

    QWidget#sidebar {
        border-right: 1px solid #555555;
        background-color: #1e1e1e;
    }

    QTextEdit {
        font-family: Consolas, monospace;
        font-size: 16px;
    }

    /* --- QTableWidget (analytics) --- */

    QTableWidget {
        background-color: #1e1e1e;
        alternate-background-color: #252525;
        color: #ffffff;
        gridline-color: #3a3a3a;
        border: 1px solid #3a3a3a;
    }

    QTableWidget::item {
        padding: 4px;
    }

    /* --- КНОПКИ В ТАБЛИЦЕ --- */

    QTableWidget QPushButton {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #555555;
        border-radius: 4px;
        padding: 4px 8px;
        min-width: 90px;
    }

    QTableWidget QPushButton:hover {
        background-color: #444444;
    }

    QTableWidget QPushButton:checked {
        background-color: #8a6d1f;
        color: #ffffff;
        border: 1px solid #c9a227;
        font-weight: bold;
    }
    # --- АНАЛИЗ ОИ ГРАФИКИ --- */
    QLabel#analysisTitle {
        color: #ffffff;
        font-size: 28px;
        font-weight: bold;
    }
    """