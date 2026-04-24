import http.client
import json
import sqlite3
import os
import time
from datetime import datetime, timedelta
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
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2026, 4, 23)

INTERVAL = 24
STEP_DAYS = 500

SLEEP_BETWEEN_REQUESTS = 0.4
SLEEP_BETWEEN_TICKERS = 1.0

MAX_RETRIES = 3


# ======================
# DB
# ======================
def get_ticker_list():
    """Получаем уникальные тикеры из futures_oi"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT paper FROM futures_oi")

    tickers = [row[0] for row in cursor.fetchall() if row[0]]

    conn.close()
    return tickers


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


# ======================
# API
# ======================
def fetch_price_chunk(ticker, date_from, date_till):
    conn = http.client.HTTPSConnection("apim.moex.com")

    url = (
        f"/iss/engines/stock/markets/shares/boards/tqbr/securities/"
        f"{ticker}/candles.json"
        f"?from={date_from}&till={date_till}&interval={INTERVAL}"
    )

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()

    if res.status != 200:
        raise Exception(f"HTTP {res.status}")

    data = res.read()
    return json.loads(data.decode("utf-8"))


def parse_candles(ticker, response_json):
    candles = response_json.get("candles", {})
    columns = candles.get("columns", [])
    data = candles.get("data", [])

    result = []

    for row in data:
        item = dict(zip(columns, row))
        date = item["begin"][:10]

        result.append(
            (
                ticker,
                date,
                item.get("open"),
                item.get("high"),
                item.get("low"),
                item.get("close"),
                item.get("volume"),
            )
        )

    return result


# ======================
# MAIN LOGIC
# ======================
def process_ticker(ticker, index, total):
    print(f"\n[{index}/{total}] Тикер: {ticker}")

    current_start = START_DATE
    ticker_total = 0

    while current_start < END_DATE:
        current_end = current_start + timedelta(days=STEP_DAYS)

        if current_end > END_DATE:
            current_end = END_DATE

        from_str = current_start.strftime("%Y-%m-%d")
        till_str = current_end.strftime("%Y-%m-%d")

        print(f"  → {from_str} → {till_str}")

        # retry логика
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = fetch_price_chunk(ticker, from_str, till_str)
                price_data = parse_candles(ticker, response)

                insert_price_data(price_data)

                print(f"    ✔ {len(price_data)} записей")

                ticker_total += len(price_data)
                break

            except Exception as e:
                print(f"    ⚠ попытка {attempt}: {e}")

                if attempt == MAX_RETRIES:
                    print("    ❌ пропуск диапазона")
                else:
                    time.sleep(1)

        current_start = current_end + timedelta(days=1)
        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"  ✔ Итого по {ticker}: {ticker_total}")


def main():
    print(f"Токен: {TOKEN[:10]}...")

    tickers = get_ticker_list()
    total = len(tickers)

    print(f"Найдено тикеров: {total}")

    for i, ticker in enumerate(tickers, start=1):
        process_ticker(ticker, i, total)
        time.sleep(SLEEP_BETWEEN_TICKERS)

    print("\n====================")
    print("Готово.")


if __name__ == "__main__":
    main()