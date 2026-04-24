import time
from datetime import date, datetime, timedelta

from loguru import logger

from app.api.moex_client import MoexClient
from app.repository.price_repository import PriceRepository


START_DEFAULT = date(2023, 1, 1)
STEP_DAYS = 500

SLEEP_REQUEST = 0.4
SLEEP_TICKER = 1.0


class PriceSyncService:
    def __init__(self):
        self.repo = PriceRepository()
        self.api = MoexClient()

    def _get_yesterday(self):
        return datetime.now().date() - timedelta(days=1)

    def _parse_price_history(self, ticker, response_json):
        candles = response_json.get("candles", {})
        columns = candles.get("columns", [])
        data = candles.get("data", [])

        price_data = []

        for row in data:
            item = dict(zip(columns, row))
            price_date = item["begin"][:10]

            price_data.append(
                (
                    ticker,
                    price_date,
                    item.get("open"),
                    item.get("high"),
                    item.get("low"),
                    item.get("close"),
                    item.get("volume"),
                )
            )

        return price_data

    def sync_price_history(self):
        logger.info("Запущена синхронизация цен")

        tickers = self.repo.get_ticker_list()
        total_tickers = len(tickers)

        logger.info(f"Найдено тикеров для проверки: {total_tickers}")

        if total_tickers == 0:
            logger.warning("Синхронизация цен остановлена: тикеры не найдены")
            return

        end_date = self._get_yesterday()

        total_loaded = 0
        updated_tickers = 0
        skipped_tickers = 0
        failed_ranges = 0

        for index, ticker in enumerate(tickers, start=1):
            # logger.info(f"[{index}/{total_tickers}] Проверка тикера {ticker}")

            last_date = self.repo.get_last_price_date(ticker)

            if last_date:
                start_date = last_date + timedelta(days=1)
                # logger.info(f"{ticker}: последняя запись в БД — {last_date}")
            else:
                start_date = START_DEFAULT
                logger.info(f"{ticker}: данных в БД нет, загрузка с {START_DEFAULT}")

            if start_date > end_date:
                skipped_tickers += 1
                # logger.info(f"{ticker}: данные актуальны, загрузка не требуется")
                continue

            ticker_loaded = 0
            current_start = start_date

            while current_start <= end_date:
                current_end = current_start + timedelta(days=STEP_DAYS)

                if current_end > end_date:
                    current_end = end_date

                date_from = current_start.isoformat()
                date_till = current_end.isoformat()

                # logger.info(f"{ticker}: запрос цен за период {date_from} — {date_till}")

                try:
                    response_json = self.api.get_price_history(
                        ticker=ticker,
                        date_from=date_from,
                        date_till=date_till,
                    )

                    price_data = self._parse_price_history(ticker, response_json)

                    if price_data:
                        self.repo.insert_price_batch(price_data)
                        ticker_loaded += len(price_data)
                        total_loaded += len(price_data)

                        logger.success(
                            f"{ticker}: загружено {len(price_data)} записей "
                            f"за период {date_from} — {date_till}"
                        )
                    else:
                        logger.warning(
                            f"{ticker}: MOEX вернул пустой ответ "
                            f"за период {date_from} — {date_till}"
                        )

                except Exception as error:
                    failed_ranges += 1
                    logger.error(
                        f"{ticker}: ошибка загрузки за период "
                        f"{date_from} — {date_till}: {error}"
                    )

                current_start = current_end + timedelta(days=1)
                time.sleep(SLEEP_REQUEST)

            if ticker_loaded > 0:
                updated_tickers += 1
                logger.success(f"{ticker}: всего загружено {ticker_loaded} записей")
            else:
                logger.info(f"{ticker}: новых записей не загружено")

            time.sleep(SLEEP_TICKER)

        logger.success(
            "Синхронизация цен завершена. "
            f"Обновлено тикеров: {updated_tickers}. "
            f"Пропущено актуальных тикеров: {skipped_tickers}. "
            f"Всего загружено записей: {total_loaded}. "
            f"Ошибочных диапазонов: {failed_ranges}."
        )