from pathlib import Path
import sqlite3
from datetime import date


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "storage" / "db" / "PanelOi_db.db"


class PriceRepository:

    def get_last_price_date(self, ticker: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT MAX(date)
            FROM paper_price
            WHERE ticker = ?
            """,
            (ticker,),
        )

        result = cursor.fetchone()[0]
        conn.close()

        if result:
            return date.fromisoformat(result)

        return None

    def insert_price_batch(self, price_data):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        query = """
            INSERT OR IGNORE INTO paper_price
            (ticker, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.executemany(query, price_data)
        conn.commit()
        conn.close()

    def get_ticker_list(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT paper FROM futures_oi")

        tickers = [row[0] for row in cursor.fetchall() if row[0]]

        conn.close()
        return tickers
    
    def get_price_by_ticker(self, ticker: str) -> list[dict]:
        query = """
            SELECT date, high, low
            FROM paper_price
            WHERE ticker = ?
            ORDER BY date
        """

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (ticker,))
            rows = cursor.fetchall()

        return [dict(row) for row in rows]