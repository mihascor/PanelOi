from loguru import logger
import sys
from pathlib import Path


def setup_logger() -> None:
    """Инициализация логирования для всего приложения"""

    # --- путь к логам ---
    log_dir = Path("storage/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"
    error_file = log_dir / "error.log"

    # --- сбрасываем дефолтный логгер ---
    logger.remove()

    # --- вывод в консоль ---
    logger.add(
        sys.stdout,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    )

    # --- основной лог ---
    logger.add(
        log_file,
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    )

    # --- ошибки отдельно ---
    logger.add(
        error_file,
        level="ERROR",
        rotation="5 MB",
        retention="30 days",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    )