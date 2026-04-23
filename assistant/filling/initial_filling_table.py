"""
Первичное заполнение таблицы futures_oi

- берет futures_list из БД
- делает запрос к MOEX
- парсит OI
- сохраняет в SQLite
"""

import http.client
import json
import os
import sqlite3
import ssl
from datetime import datetime

from dotenv import load_dotenv


# =========================
# CONFIG
# =========================
DB_PATH = r"C:\tap_ms\storage\tap_ms.db"

DATE_FROM = "2020-01-03"
DATE_TILL = "2026-04-06"

# =========================
# TOKEN
# =========================
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не найден")


# =========================
# DB
# =========================
conn_db = sqlite3.connect(DB_PATH)
cursor = conn_db.cursor()

cursor.execute("SELECT futures, paper FROM futures_list")
futures_list = cursor.fetchall()


# =========================
# SSL (фикс зависания)
# =========================
ssl_context = ssl._create_unverified_context()


# =========================
# HEADERS
# =========================
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}


# =========================
# ОСНОВНОЙ ЦИКЛ
# =========================
for futures, paper in futures_list:
    print(f"Обработка {futures}")

    endpoint = (
        f"/iss/analyticalproducts/futoi/securities/{futures}.json"
        f"?from={DATE_FROM}&till={DATE_TILL}&latest=1"
    )

    # новое соединение на каждый запрос
    conn = http.client.HTTPSConnection(
        "apim.moex.com",
        timeout=10,
        context=ssl_context
    )

    try:
        conn.request("GET", endpoint, body=None, headers=headers)
        res = conn.getresponse()

        if res.status != 200:
            print(f"Ошибка {futures}: {res.status}")
            continue

        data = json.loads(res.read().decode("utf-8"))

    except Exception as e:
        print(f"Ошибка запроса {futures}: {e}")
        continue

    finally:
        conn.close()

    # =========================
    # ПАРСИНГ
    # =========================
    rows = data.get("futoi", {}).get("data", [])
    columns = data.get("futoi", {}).get("columns", [])

    if not rows:
        print(f"{futures}: нет данных")
        continue

    idx = {col: i for i, col in enumerate(columns)}

    result = {}

    for row in rows:
        tradedate = row[idx["tradedate"]]
        clgroup = row[idx["clgroup"]]

        pos_long = abs(row[idx["pos_long"]])
        pos_short = abs(row[idx["pos_short"]])

        if tradedate not in result:
            result[tradedate] = {
                "FIZ_long": 0,
                "FIZ_short": 0,
                "YUR_long": 0,
                "YUR_short": 0,
            }

        if clgroup == "FIZ":
            result[tradedate]["FIZ_long"] = pos_long
            result[tradedate]["FIZ_short"] = pos_short

        elif clgroup == "YUR":
            result[tradedate]["YUR_long"] = pos_long
            result[tradedate]["YUR_short"] = pos_short

    # =========================
    # ЗАПИСЬ В БД
    # =========================
    for tradedate, values in result.items():
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO futures_oi (
                    futures,
                    paper,
                    tradedate,
                    FIZ_long,
                    FIZ_short,
                    YUR_long,
                    YUR_short
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                futures,
                paper,
                tradedate,
                values["FIZ_long"],
                values["FIZ_short"],
                values["YUR_long"],
                values["YUR_short"],
            ))

        except Exception as e:
            print(f"Ошибка записи {futures} {tradedate}: {e}")

    conn_db.commit()


# =========================
# ЗАВЕРШЕНИЕ
# =========================
conn_db.close()

print("Готово")