from collections import defaultdict
from datetime import datetime

from app.repository.oi_repository import OiRepository
from app.repository.price_repository import PriceRepository

# Данные для графиков ОИ и цены 

def build_oi_price_chart_data(paper: str) -> dict:
    """
    Готовит данные для графиков:
    - price: high/low (вертикальные линии)
    - oi: FIZ и YUR коэффициенты (-20..20)
    """

    price_repo = PriceRepository()
    oi_repo = OiRepository()

    price_rows = price_repo.get_price_by_ticker(paper)
    oi_rows = oi_repo.get_oi_by_paper(paper)

    # --- индекс OI по дате ---
    oi_by_date = {row["tradedate"]: row for row in oi_rows}

    result = {
        "dates": [],
        "price_high": [],
        "price_low": [],
        "fiz_koof": [],
        "yur_koof": [],
    }

    last_fiz = None
    last_yur = None

    for row in price_rows:
        date = row["date"]

        result["dates"].append(date)
        result["price_high"].append(row["high"])
        result["price_low"].append(row["low"])

        oi = oi_by_date.get(date)

        if oi:
            last_fiz = _calculate_koof(oi["FIZ_long"], oi["FIZ_short"])
            last_yur = _calculate_koof(oi["YUR_long"], oi["YUR_short"])

        result["fiz_koof"].append(last_fiz)
        result["yur_koof"].append(last_yur)

    return result


def _calculate_koof(long: int, short: int) -> float | None:
    """
    Расчёт коэффициента:
    - min == 0 → koof = max
    - знак: short > long → отрицательный
    - clamp: [-20, 20]
    """

    if long is None or short is None:
        return None

    min_val = min(long, short)
    max_val = max(long, short)

    if min_val == 0:
        koof = float(max_val)
    else:
        koof = max_val / min_val

    if short > long:
        koof = -koof

    # clamp
    if koof > 20:
        koof = 20
    if koof < -20:
        koof = -20

    return koof