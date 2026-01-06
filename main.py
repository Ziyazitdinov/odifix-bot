import asyncio
import json

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, CHANNEL_ID, UPDATE_INTERVAL_HOURS, HEADER_PRODUCTS
from parser import parse_price


def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"header_message_id": None}


def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_header_text() -> str:
    lines = [
        "Гарантия 7 дней со дня покупки на проверку",
        "Официальная гарантия 12 месяцев от Apple",
        "",
    ]

    # блок зарядок
    lines.append(f"Apple USB-C мощностью 20 Вт - {parse_price(HEADER_PRODUCTS['Apple USB-C мощностью 20 Вт'])}")
    lines.append(f"Apple Dual USB-C мощностью 35 Вт - {parse_price(HEADER_PRODUCTS['Apple Dual USB-C мощностью 35 Вт'])}")
    lines.append("")

    # блок AirPods
    airpods_order = [
        "AirPods Pro 3",
        "AirPods Pro 2 (USB-C)",
        "AirPods 4 с шумоподавлением",
        "AirPods 4",
        "AirPods Max Blue",
        "AirPods Max Midnight",
        "AirPods Max Orange",
        "AirPods Max Purple",
        "AirPods Max Starlight",
    ]
    for name in airpods_order:
        lines.append(f"{name} - {parse_price(HEADER_PRODUCTS[name])}")

    return "\n".join(lines)


async def update_header(bot: Bot):
    data = load_data()
    text = build_header_text()

    if not data.get("header_message_id"):
        msg = await bot.send_message(chat_id=CHANNEL_ID, text=text)
        data["header_message_id"] = msg.message_id
        save_data(data)
    else:
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=data["header_message_id"],
            text=text
        )


async def main():
    bot = Bot(token=BOT_TOKEN)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_header, "interval", hours=UPDATE_INTERVAL_HOURS, args=[bot])
    scheduler.start()

    # первый запуск сразу
    await update_header(bot)

    # держим процесс живым
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
