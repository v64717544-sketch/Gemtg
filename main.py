import logging
import os
import threading
from flask import Flask, render_template
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# --- 1. НАСТРОЙКА TELEGRAM БОТА ---
# Вставь сюда свой реальный API-ключ от Google AI Studio
client = genai.Client(api_key="ТВОЙ_API_КЛЮЧ_GEMINI")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  print(f"Telegram-бот получил: {user_message}")

  try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_message,
    )
    await update.message.reply_text(response.text)
  except Exception as e:
    print(f"Ошибка ИИ в боте: {e}")
    await update.message.reply_text(
        "Произошла ошибка при обращении к нейросети."
    )


def run_telegram_bot():
  """Запуск бота в фоновом потоке с твоим токеном"""
  TOKEN = "8935773236:AAGlK8Ee3PyVVUQw5V-43tF5WnlhUb-qlRE"
  app_bot = ApplicationBuilder().token(TOKEN).build()
  app_bot.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
  )
  print("Telegram-бот запущен в фоновом режиме...")
  app_bot.run_polling()


# --- 2. НАСТРОЙКА САЙТА (FLASK) ---
app = Flask(__name__)

PRODUCTS = [
    {
        "id": 1,
        "name": "Аккумуляторный шуруповерт Pro",
        "price": 45000,
        "category": "Электроинструмент",
        "image": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=500&q=60",
    },
    {
        "id": 2,
        "name": "Угловая шлифмашина (Болгарка)",
        "price": 32000,
        "category": "Электроинструмент",
        "image": "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=500&q=60",
    },
    {
        "id": 3,
        "name": "Набор ручного инструмента 94 пр.",
        "price": 68000,
        "category": "Ручной инструмент",
        "image": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc?auto=format&fit=crop&w=500&q=60",
    },
    {
        "id": 4,
        "name": "Профессиональный перфоратор",
        "price": 85000,
        "category": "Электроинструмент",
        "image": "https://images.unsplash.com/photo-1508873696983-2df5c920ac1c?auto=format&fit=crop&w=500&q=60",
    },
]


@app.route("/")
def index():
  return render_template("index.html", products=PRODUCTS)


@app.route("/contacts")
def contacts():
  return render_template("contacts.html")


# --- 3. ЗАПУСК ВСЕЙ СИСТЕМЫ ---
if __name__ == "__main__":
  # Запускаем Telegram-бота в фоновом потоке
  bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
  bot_thread.start()

  # Запуск веб-сервера (для Railway или локально)
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=False)
