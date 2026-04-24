"""
Источники обноллены.
Мне надо написать скрипт который буду запускать вручную, один раз для заполнения таблицы paper_price.
Размещу его в assistant\filling, он небудет отвечать требованиям к структуре проекта, так как он будет использоваться только один раз, и не будет частью основного приложения.
Данные для запроса:
import http.client

conn = http.client.HTTPSConnection("apim.moex.com")
payload = ''
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer <token>'
}
conn.request("GET", "/iss/engines/stock/markets/shares/boards/tqbr/securities/:ticker/candles.json", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
---
ticker
string
required
Код ценной бумаги, например 'SBER' берем из БД, таблица futures_oi, колонка paper.

Query Parameters
from
date-time
Начало периода (ISO 8601) - запросим с 2024года.

till
date-time
Окончание периода (ISO 8601) - до 06/04/2026

interval
integer
Possible values: [1, 10, 60, 24, 7, 31, 4] -  период сделаем = 24, так как нам нужны дневные свечи.

Интервал свечи (1-мин, 10-мин, 60-мин, 24-день, 7-неделя, 31-месяц, 4-квартал)

Токен лежит в файле .env, который находится в корне проекта, и называется TOKEN. 
данные 
Таблица для заполнения:
CREATE TABLE "paper_price" (
        "id"    INTEGER,
        "ticker"        TEXT,
        "date"  DATE,
        "open"  REAL,
        "close" REAL,
        "high"  REAL,
        "low"   REAL,
        "volume"        INTEGER,
        PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX idx_unique_ticker_date
ON paper_price (ticker, date);
Надо забрать и поместить в таблицу paper_price, которая уже создана в БД. Столбцы таблицы: id, ticker, date, open, high, low, close, volume.
Я предлагаю написать написать первую версию с фиксированным тикетом - SBER
"""
