import os
import random
import asyncio
from aiogram import Bot

# --- НАСТРОЙКИ (заполни своими данными) ---
TOKEN = os.environ.get("BOT_TOKEN")
MOM_ID = int(os.environ.get("MOM_ID"))
YOUR_ID = int(os.environ.get("YOUR_ID"))
# ------------------------------------------

async def send_daily_gift():
    quotes_file = "quotes.txt"
    pointer_file = "pointer.txt"

    # Списки для настроения
    greetings = [
        "Добрый день, мамуль! ☀️",
        "Чудесного дня! ✨",
        "Мама, улыбнись! Сегодня будет отличный день. ❤️",
        "Посылаю тебе лучи хорошего настроения из Эквадора! 🌈",
        "Пусть это утро будет самым добрым! ☕",
        "Мамочка, хорошего тебе настроения на весь день!🌸"
    ]
    
    emoji_tails = ["🌸", "🙏", "💖", "🍃", "🦋", "☀️", "🕊️", "☕"]

    # 1. Загружаем цитаты
    if not os.path.exists(quotes_file):
        print("❌ Файл quotes.txt не найден!")
        return
    
    with open(quotes_file, "r", encoding="utf-8") as f:
        quotes = [line.strip() for line in f if line.strip()]

    if not quotes:
        print("❌ Файл с цитатами пуст!")
        return

    # 2. Читаем позицию
    index = 0
    if os.path.exists(pointer_file):
        with open(pointer_file, "r") as f:
            try:
                index = int(f.read().strip())
            except:
                index = 0

    bot = Bot(token=TOKEN)
    
    try:
        if index < len(quotes):
            current_quote = quotes[index]
            
            # Собираем сообщение
            header = random.choice(greetings)
            tail = random.choice(emoji_tails)
            full_text = f"{header}\n\n{current_quote}\n\n{tail}"
            
            # Отправка
            await bot.send_message(MOM_ID, full_text)
            
            # Сохраняем индекс
            index += 1
            with open(pointer_file, "w") as f:
                f.write(str(index))
            
            print(f"✅ Отправлено маме! (Цитата №{index})")
        else:
            await bot.send_message(YOUR_ID, "📢 Хозяйка, цитаты закончились!")
            print("⚠️ Цитаты закончились.")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await bot.send_message(YOUR_ID, f"❌ Бот сломался: {e}")
    finally:
        await bot.session.close()

# Запуск
if __name__ == "__main__":
    asyncio.run(send_daily_gift())