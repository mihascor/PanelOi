import http.client
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


# ======================
# PATH
# ======================
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "storage" / "db" / "PanelOi_db.db"

# ======================
# ENV
# ======================
load_dotenv(BASE_DIR / ".env")
TOKEN = os.getenv("TOKEN")

# ======================
# CONFIG
# ======================
TICKER = "SBER"
DATE_FROM = "2025-10-01"
DATE_TILL = "2026-04-24"
INTERVAL = 24


def get_price_data():
    """Получение свечей с MOEX"""
    conn = http.client.HTTPSConnection("apim.moex.com")

    url = f"/iss/engines/stock/markets/shares/boards/tqbr/securities/{TICKER}/candles.json?from={DATE_FROM}&till={DATE_TILL}&interval={INTERVAL}"

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()

    if res.status != 200:
        raise Exception(f"HTTP ошибка: {res.status}")

    data = res.read()
    return json.loads(data.decode("utf-8"))


def parse_candles(response_json):
    """Парсинг ответа MOEX"""
    candles = response_json.get("candles", {})
    columns = candles.get("columns", [])
    data = candles.get("data", [])

    result = []

    for row in data:
        item = dict(zip(columns, row))

        date = item["begin"][:10]  # YYYY-MM-DD

        result.append(
            (
                TICKER,
                date,
                item.get("open"),
                item.get("high"),
                item.get("low"),
                item.get("close"),
                item.get("volume"),
            )
        )

    return result


def insert_price_data(price_data):
    """Запись в БД"""
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


def main():
    print("Загрузка данных...")

    response = get_price_data()
    price_data = parse_candles(response)

    print(f"Получено записей: {len(price_data)}")

    insert_price_data(price_data)

    print("Готово.")


if __name__ == "__main__":
    main()