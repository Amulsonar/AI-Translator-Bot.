import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

# 1. Flask setup (Render ke "Port" error ko khatam karne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running Live!"

def run_flask():
    # Render hamesha PORT 10000 mangta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. Bot aur Gemini Setup
# (Ye keys aapne Render ke Environment Variables mein pehle se dali hui hain)
BOT_TOKEN = ('8149059077:AAHs-p7lr1v7CQhPh6XCdQpzR5Idu0BnKxY')
GEMINI_KEY = ('AIzaSyA1q4yIT7OaBKDKPkuIManewyMnntMlXuE')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Bot Commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bhai, aapka AI Translator bot ab Live hai! Kuch bhi likho, main Hindi aur Gujarati mein translate kar dunga.")

@bot.message_handler(func=lambda m: True)
def translate_text(message):
    try:
        # Gemini ko instruction de rahe hain
        prompt = f"Translate the following text to Hindi and Gujarati. Keep it simple: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Thodi dikkat aa rahi hai, ek baar API key check karein.")

# 4. Main Function (Flask aur Bot dono ko ek saath chalane ke liye)
if __name__ == "__main__":
    # Flask ko alag thread mein chalayenge
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Bot polling shuru
    print("Bot is starting...")
    bot.polling(none_stop=True)

        
