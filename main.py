import telebot
import google.generativeai as genai
import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# API Keys
BOT_TOKEN = os.environ.get('8149059077:AAHsh9V-IJz6C60-OAxK1SJQQWsZnz76ndQ')
GEMINI_KEY = os.environ.get('AIzaSyDF0QiVuxxmrzfYRZqHsz9W0Lq7_UI5QiE')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Naya Model Name (Zyada Stable)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Namaste! Main AI Translator Bot hoon.\n\nKoi bhi message bhejiye, main use Hindi aur Gujarati mein translate kar dunga.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        # Prompt ko aur clear kiya hai
        prompt = f"Translate the following text to both Hindi and Gujarati clearly. Format: \n\nHindi: [Translation]\nGujarati: [Translation]\n\nText: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "AI ne koi jawab nahi diya, fir se try karein.")
            
    except Exception as e:
        print(f"ERROR: {e}")
        # Error message mein thodi details taaki aapko pata chale kya hua
        bot.reply_to(message, f"⚠️ Gemini API issue. Check if API KEY is correct.\nError: {str(e)[:50]}")

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    bot.infinity_polling()
