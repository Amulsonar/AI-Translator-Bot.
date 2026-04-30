import os
import threading
import time
from flask import Flask
import telebot
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Keys fetch karke space saaf karna
BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '').strip()

bot = telebot.TeleBot(BOT_TOKEN)

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Active hai! Ab translation shuru karein.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Translation process
        response = model.generate_content(f"Translate to Hindi and Gujarati: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        # Error dikhane ke liye
        bot.reply_to(message, f"AI Error: {str(e)[:50]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    print("Bot starting...")
    bot.infinity_polling(skip_pending=True)
