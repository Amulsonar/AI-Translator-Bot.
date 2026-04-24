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

# Keys Render se uthayega
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Naya model version aur safety settings
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature": 0.7}
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot start ho gaya hai! Kuch bhi bhejiye.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Translation ke liye instruction
        prompt = f"Translate the following text to Hindi and Gujarati separately: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "AI ne response khali bheja hai.")
            
    except Exception as e:
        # Ye line humein asli error batayegi
        error_msg = str(e)
        print(f"Error: {error_msg}")
        bot.reply_to(message, f"Dhyan dein: {error_msg[:100]}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(skip_pending=True)
