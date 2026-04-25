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

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Naya aur fast model
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Active ho gaya hai! Ab reply aayega.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Simple instruction
        response = model.generate_content(f"Translate to Hindi and Gujarati: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        # Agar ye fail ho toh purana model try karega
        try:
            alt_model = genai.GenerativeModel('gemini-pro')
            response = alt_model.generate_content(f"Translate to Hindi and Gujarati: {message.text}")
            bot.reply_to(message, response.text)
        except Exception as e2:
            bot.reply_to(message, f"AI Connection Error. Ek baar key check karein.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
