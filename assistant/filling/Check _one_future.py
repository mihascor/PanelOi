"""
Технический скрипт:
- Запрос данных по конкретному тикеру (futoi)
- Период: с 2020 года по сегодня
- latest=1 (последняя пятиминутка)
- Сохраняет JSON в текущую папку
"""

import http.client
import json
import os
from datetime import datetime

from dotenv import load_dotenv


# =========================
# Загрузка токена
# =========================
load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN не найден в .env")


# =========================
# Параметры
# =========================
TICKER = "VK"  
DATE_FROM = "2020-01-03"
DATE_TILL = "2026-04-06"
LATEST = 1

endpoint = (
    f"/iss/analyticalproducts/futoi/securities/{TICKER}.json"
    f"?from={DATE_FROM}&till={DATE_TILL}&latest={LATEST}"
)


# =========================
# Запрос
# =========================
conn = http.client.HTTPSConnection("apim.moex.com")

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

conn.request("GET", endpoint, headers=headers)

res = conn.getresponse()

if res.status != 200:
    raise Exception(f"Ошибка запроса: {res.status} {res.reason}")

data = res.read()


# =========================
# Парсинг JSON
# =========================
try:
    json_data = json.loads(data.decode("utf-8"))
except Exception as e:
    raise Exception(f"Ошибка парсинга JSON: {e}")


# =========================
# Сохранение
# =========================
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = (
    f"moex_{TICKER}_{DATE_FROM}_{DATE_TILL}_latest_{LATEST}_{timestamp}.json"
)

file_path = os.path.join(os.path.dirname(__file__), filename)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)


print(f"Файл сохранен: {file_path}")