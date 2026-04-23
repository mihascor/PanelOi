from pathlib import Path


def load_logs_to_ui(limit: int = 300) -> str:
    """
    Загружает последние строки логов (свежие сверху)
    """

    log_path = Path("storage/logs/app.log")

    if not log_path.exists():
        return "Лог-файл не найден"

    try:
        with log_path.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        # берём последние строки
        lines = lines[-limit:]

        # переворачиваем (новые сверху)
        lines.reverse()

        return "".join(lines)

    except Exception as e:
        return f"Ошибка чтения логов: {e}"