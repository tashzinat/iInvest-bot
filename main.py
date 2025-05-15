
import logging
import os
import telegram
from telegram.ext import CommandHandler, Updater
from google.oauth2.service_account import Credentials
import gspread

# Настройки
BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к таблице
def get_sheet_data():
    try:
        creds = Credentials.from_service_account_file("creds.json", scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
        gc = gspread.authorize(creds)
        sheet = gc.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_records()
        return data
    except Exception as e:
        logger.error(f"Ошибка при подключении к таблице: {e}")
        return []

# Команды
def start(update, context):
    update.message.reply_text("Привет! Я — твой инвестиционный бот. Напиши /portfolio, чтобы увидеть портфель.")

def portfolio(update, context):
    data = get_sheet_data()
    if not data:
        update.message.reply_text("Не удалось получить данные. Проверь подключение к таблице.")
        return
    message = "📊 Твой портфель:
"
    for row in data:
        asset = row.get("Актив", "N/A")
        value = row.get("Текущая стоимость (€)", 0)
        message += f"- {asset}: {value} €\n"
    update.message.reply_text(message)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("portfolio", portfolio))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
