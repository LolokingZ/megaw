import asyncio
import logging
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Application, CommandHandler

BOT_TOKEN = "7634480398:AAHvADKAg5XGB91At9bYrcY-8CmRC5SG5sA"
CHAT_ID = 1192099192

URL = "https://gamblingcounting.com/mega-wheel"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_data():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        last_result = soup.select_one(".latest-number .ball")
        if last_result:
            return last_result.text.strip()
        return None
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return None

async def predict(update=None, context=None):
    angka = await get_data()
    if not angka:
        msg = "⚠️ Gagal ambil data Mega Wheel."
    else:
        try:
            prediksi = int(angka) + 1
        except:
            prediksi = "?"
        msg = f"🎯 Mega Wheel terakhir: {angka}\n🔮 Prediksi selanjutnya: {prediksi}"
    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def start(update, context):
    await update.message.reply_text("✅ Bot prediksi Mega Wheel aktif!\nGunakan /prediksi untuk hasil terbaru.")

async def main():
    global bot
    bot = Bot(BOT_TOKEN)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prediksi", predict))
    print("🤖 Bot berjalan...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(main())
    else:
        loop.run_until_complete(main())
