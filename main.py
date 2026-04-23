import os
import threading
import time
from flask import Flask
import telebot
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return "Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Yahan humne model update kiya hai
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Active! Ab kuch likhiye.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Gemini ko instruction
        response = model.generate_content(f"Translate to Hindi and Gujarati: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        # Ye line humein batayegi ki asli error kya hai
        print(f"Gemini Error: {e}")
        bot.reply_to(message, f"AI Error: {str(e)[:50]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
