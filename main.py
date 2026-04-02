import os
import google.generativeai as genai
from telebot import TeleBot

# Render se Keys uthane ka sahi tarika
BOT_TOKEN = os.environ.get('8149059077:AAHsh9V-IJz6C60-OAxK1SJQQWsZnz76ndQ')
GEMINI_KEY = os.environ.get('AIzaSyA1q4yIT7OaBKDKPkuIManewyMnntMlXuE')

bot = TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bhai, bot ab bilkul taiyaar hai! Kuch bhi likho, main translate kar dunga.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        prompt = f"Translate this to Hindi and Gujarati: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Yaar, Gemini connect nahi ho pa raha. API Key check karein.")

bot.polling()
        
