from pathlib import Path
import sqlite3

from loguru import logger


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "storage" / "db" / "PanelOi_db.db"


class OiRepository:
    def get_latest_oi_by_futures(self) -> list[dict]:
        """
        Получает последние данные ОИ по каждому уникальному futures.
        SQL находится только в repository.
        """
        query = """
            SELECT
                foi.futures,
                foi.paper,
                foi.tradedate,
                foi.FIZ_long,
                foi.FIZ_short,
                foi.YUR_long,
                foi.YUR_short
            FROM futures_oi foi
            INNER JOIN (
                SELECT
                    futures,
                    MAX(tradedate) AS latest_tradedate
                FROM futures_oi
                GROUP BY futures
            ) latest
                ON foi.futures = latest.futures
                AND foi.tradedate = latest.latest_tradedate
            ORDER BY foi.futures
        """

        try:
            with sqlite3.connect(DB_PATH) as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()

            return [dict(row) for row in rows]

        except sqlite3.Error as error:
            logger.error(f"Ошибка чтения последних данных ОИ из базы: {error}")
            return []