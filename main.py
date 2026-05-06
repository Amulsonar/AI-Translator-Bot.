import os
import threading
import time
from flask import Flask
import telebot
from google import genai

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Key saaf karna
BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '').strip()

bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot Active! Nayi library ke sath connect ho gaya hoon.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=f"Translate to Hindi and Gujarati: {message.text}"
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)[:50]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
    
