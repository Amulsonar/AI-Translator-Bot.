import telebot
import google.generativeai as genai
import os
from flask import Flask
import threading

# 1. Flask App Setup (Render ke 'Port Scan Timeout' ko fix karne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Active and Running!"

def run_flask():
    # Render hamesha PORT environment variable deta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. API Keys Configuration
# Yaad rahe: Inhe Render ke 'Environment Variables' mein add karna zaroori hai
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# 3. Bot Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Namaste! Main AI Translator Bot hoon.\n\nKoi bhi message bhejiye, main use Hindi aur Gujarati mein translate kar dunga.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    try:
        # Gemini AI se translation mangna
        prompt = f"Translate the following text to both Hindi and Gujarati clearly: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Thodi dikkat aa rahi hai, kripya baad mein koshish karein.")

# 4. Starting the Engine
if __name__ == "__main__":
    # Flask ko alag thread mein chalana taaki bot block na ho
    t = threading.Thread(target=run_flask)
    t.start()
    
    print("Bot is starting polling...")
    # Bot ko infinite loop mein daalna
    bot.infinity_polling()
    
