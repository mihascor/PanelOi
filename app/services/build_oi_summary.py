from pathlib import Path
import sqlite3
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "storage" / "db" / "PanelOi_db.db"


def build_oi_summary() -> dict:
    """
    Формирует сводку по данным OI для UI
    """

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # --- получаем список всех инструментов ---
    cursor.execute("SELECT paper FROM futures_list")
    paper_list = [row[0] for row in cursor.fetchall()]

    # --- получаем диапазоны дат по OI ---
    cursor.execute("""
        SELECT
            paper,
            MIN(tradedate),
            MAX(tradedate)
        FROM futures_oi
        GROUP BY paper
    """)

    oi_map = {
        row[0]: (row[1], row[2])
        for row in cursor.fetchall()
    }

    conn.close()

    rows = []

    total = len(paper_list)
    with_data = 0
    empty = 0

    for paper in paper_list:

        if paper in oi_map:
            min_date, max_date = oi_map[paper]

            # формат даты
            min_date = _format_date(min_date)
            max_date = _format_date(max_date)

            rows.append({
                "paper": paper,
                "min_date": min_date,
                "max_date": max_date,
                "status": "ok"
            })

            with_data += 1

        else:
            rows.append({
                "paper": paper,
                "min_date": "",
                "max_date": "",
                "status": "empty"
            })

            empty += 1

    return {
        "rows": rows,
        "total": total,
        "with_data": with_data,
        "empty": empty
    }


def _format_date(date_str: str) -> str:
    """
    Преобразует YYYY-MM-DD → DD.MM.YYYY
    """

    if not date_str:
        return ""

    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
    except Exception:
        return date_str