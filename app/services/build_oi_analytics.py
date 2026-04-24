from loguru import logger

from app.repository.oi_repository import OiRepository


def calculate_oi_koof(long_value: int | None, short_value: int | None) -> float:
    """
    Считает коэффициент между long и short.
    Если минимальное значение равно 0, возвращает максимальное.
    """
    long_value = long_value or 0
    short_value = short_value or 0

    max_value = max(long_value, short_value)
    min_value = min(long_value, short_value)

    if min_value == 0:
        return round(float(max_value), 1)

    return round(max_value / min_value, 1)


def calculate_oi_direction(yur_long: int | None, yur_short: int | None) -> str:
    """
    Определяет направление по юридическим лицам.
    """
    yur_long = yur_long or 0
    yur_short = yur_short or 0

    if yur_long >= yur_short:
        return "Long"

    return "Short"


def build_oi_analytics_data() -> list[dict]:
    """
    Формирует данные аналитики ОИ для UI.
    """
    logger.info("Формирование данных аналитики ОИ")

    oi_repository = OiRepository()
    oi_rows = oi_repository.get_latest_oi_by_futures()

    analytics_data = []

    for oi_row in oi_rows:
        fiz_long = oi_row.get("FIZ_long") or 0
        fiz_short = oi_row.get("FIZ_short") or 0
        yur_long = oi_row.get("YUR_long") or 0
        yur_short = oi_row.get("YUR_short") or 0

        analytics_data.append(
            {
                "futures": oi_row.get("futures", ""),
                "paper": oi_row.get("paper", ""),
                "FIZ_long": fiz_long,
                "FIZ_short": fiz_short,
                "YUR_long": yur_long,
                "YUR_short": yur_short,
                "direction": calculate_oi_direction(yur_long, yur_short),
                "FIZ_koof": calculate_oi_koof(fiz_long, fiz_short),
                "YUR_koof": calculate_oi_koof(yur_long, yur_short),
            }
        )

    logger.success("Данные аналитики ОИ сформированы")

    return analytics_data