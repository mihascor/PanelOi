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
    """