import os
import threading
import time
from flask import Flask
import telebot
import google.generativeai as genai

# 1. Flask setup (Render ke liye zaruri hai)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running Securely"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Render Environment se Keys fetch karna
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# 3. Stable Gemini-Pro Model (Isme 404 error nahi aayega)
model = genai.GenerativeModel('models/gemini-pro')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bhai, bot ekdam ready hai! Kuch bhi likho, main Hindi aur Gujarati mein translate kar dunga.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Gemini ko instruction dena
        prompt = f"Translate this text to Hindi and Gujarati separately: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "AI ne reply nahi diya, fir se koshish karein.")
            
    except Exception as e:
        # Agar koi error aaye toh bot uska naam batayega
        error_name = type(e).__name__
        bot.reply_to(message, f"Dhyan dein ({error_name}): AI connect nahi ho raha.")
        print(f"Detail: {e}")

if __name__ == "__main__":
    # Flask ko background thread mein start karein
    threading.Thread(target=run_flask).start()
    
    # Purane conflicts saaf karne ke liye
    bot.remove_webhook()
    time.sleep(1)
    
    print("Bot is starting now...")
    bot.infinity_polling(skip_pending=True)
    
