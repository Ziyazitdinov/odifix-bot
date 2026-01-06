import asyncio
import json
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, CHANNEL_ID, HEADER_PRODUCTS, UPDATE_INTERVAL_HOURS
from parser import parse_price

bot = Bot(BOT_TOKEN)


def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_header_text():
    lines = [
        "Гарантия 7 дней со дня покупки на проверку",
        "Официальная гарантия 12 месяцев от Apple",
        ""
    ]

    for name, url in HEADER_PRODUCTS.items():
        price = parse_price(url)
        lines.append(f"{name} - {price}")

    return "\n".join(lines)


async def update_header():
    data = load_data()
    text = build_header_text()

    if data["header_message_id"] is None:
        msg = await bot.send_message(CHANNEL_ID, text)
        data["header_message_id"] = msg.message_id
        save_data(data)
    else:
        await bot.edit_message_text(
            chat_id=CHANNEL_ID,
            message_id=data["header_message_id"],
            text=text
        )


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_header, "interval", hours=UPDATE_INTERVAL_HOURS)
    scheduler.start()

    await update_header()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
