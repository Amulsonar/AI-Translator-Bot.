import os
import threading
import time
from flask import Flask
import telebot
import google.generativeai as genai

# 1. Flask setup Render ke liye
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Keys fetch karna (Render Environment se)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# 3. Model setup (Correct Path ke saath)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Namaste! Bot ab nayi energy ke saath active hai. Kuch bhi likhiye!")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Prompt ko thoda aur clear kiya hai
        response = model.generate_content(f"Translate to Hindi and Gujarati: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        # Asli error check karne ke liye
        error_name = type(e).__name__
        bot.reply_to(message, f"Arey bhai error aa gaya! ({error_name})")
        print(f"Detail Error: {e}")

if __name__ == "__main__":
    # Flask start
    threading.Thread(target=run_flask).start()
    
    # Conflict khatam karne ke liye
    bot.remove_webhook()
    time.sleep(1)
    
    print("Bot is starting...")
    bot.infinity_polling(skip_pending=True)
