import requests
from bs4 import BeautifulSoup
from config import HEADERS


def round_price(price: int) -> int:
    return int(round(price / 100.0)) * 100


def parse_price(url: str) -> str:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ").lower()

        if "нет в наличии" in text or "предзаказ" in text:
            return "по запросу"

        price_tag = soup.select_one("[itemprop=price]")
        if not price_tag:
            return "по запросу"

        price = int(float(price_tag["content"]))
        price = round_price(price)

        return f"{price:,}".replace(",", " ") + "р"

    except Exception:
        return "по запросу"
