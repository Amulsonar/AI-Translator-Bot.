import os
import threading
import time
from flask import Flask
import telebot
import google.generativeai as genai

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live and Clean!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# .strip() lagane se space ki problem 100% khatam ho jayegi
BOT_TOKEN = os.environ.get('BOT_TOKEN', '').strip()
GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '').strip()

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Fresh Start! Bot ab ekdum sahi kaam karega. Kuch bhi likhiye!")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        prompt = f"Translate the following text to Hindi and Gujarati separately: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "AI Connect nahi ho pa raha. Nayi key check karein.")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    print("Bot is starting fresh...")
    bot.infinity_polling(skip_pending=True)
    
