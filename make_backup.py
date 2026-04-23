import shutil
from pathlib import Path
from datetime import datetime
import os

# =========================
# НАСТРОЙКИ
# =========================
PROJECT_DIR = Path(r"C:\Users\PC\PanelOi")
BACKUP_DIR = PROJECT_DIR / "backups"
TEMP_DIR = PROJECT_DIR / "_backup_temp"

DB_FILE = PROJECT_DIR / "storage" / "db" / "PanelOi_db.db"

# =========================
# ПРОВЕРКИ
# =========================
if not PROJECT_DIR.exists():
    raise Exception("PROJECT_DIR не найден")

if not DB_FILE.exists():
    raise Exception("БД не найдена")

# защита от пустой БД
if DB_FILE.stat().st_size < 10_000:
    raise Exception("БД подозрительно маленькая (<10KB). Остановка.")

# =========================
# ПОДГОТОВКА
# =========================
BACKUP_DIR.mkdir(exist_ok=True)

# чистим временную папку если осталась
if TEMP_DIR.exists():
    shutil.rmtree(TEMP_DIR)

# =========================
# ИСКЛЮЧЕНИЯ
# =========================
EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "backups",
    "_backup_temp"
}

EXCLUDE_FILES = {
    ".env"  # если не хочешь класть токен в архив
}

def ignore_filter(dir, files):
    ignored = []

    for name in files:
        full_path = Path(dir) / name

        if name in EXCLUDE_DIRS and full_path.is_dir():
            ignored.append(name)

        elif name in EXCLUDE_FILES and full_path.is_file():
            ignored.append(name)

    return ignored

# =========================
# КОПИРОВАНИЕ ПРОЕКТА
# =========================
shutil.copytree(
    PROJECT_DIR,
    TEMP_DIR,
    ignore=ignore_filter
)

# =========================
# СОЗДАНИЕ АРХИВА
# =========================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

archive_path = BACKUP_DIR / f"PanelOi_backup_{timestamp}"

shutil.make_archive(
    base_name=str(archive_path),
    format="zip",
    root_dir=TEMP_DIR
)

# =========================
# ОТДЕЛЬНЫЙ БЭКАП БД
# =========================
db_backup_path = BACKUP_DIR / f"PanelOi_db_{timestamp}.db"
shutil.copy(DB_FILE, db_backup_path)

# =========================
# ОЧИСТКА
# =========================
shutil.rmtree(TEMP_DIR)

print(f"Бэкап проекта: {archive_path}.zip")
print(f"Бэкап БД: {db_backup_path}")