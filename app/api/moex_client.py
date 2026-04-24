import http.client
import json
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("TOKEN")


class MoexClient:

    def get_price_history(self, ticker, date_from, date_till, interval=24):
        conn = http.client.HTTPSConnection("apim.moex.com")

        url = (
            f"/iss/engines/stock/markets/shares/boards/tqbr/securities/"
            f"{ticker}/candles.json"
            f"?from={date_from}&till={date_till}&interval={interval}"
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