import telebot
import google.generativeai as genai
import os
from flask import Flask
import threading

# 1. FLASK SETUP (Bot ko 24/7 zinda rakhne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 2. API KEYS (Directly Fixed)
# Maine yahan se os.environ.get hata diya hai taaki koi error na aaye
BOT_TOKEN = '8149059077:AAHsh9V-IJz6C60-OAxK1SJQQWsZnz76ndQ'
GEMINI_KEY = 'AIzaSyDF0Q1VuxxmrzfYRZQhsz9W0Lq7_UI5QiE'

# 3. BOT & AI CONFIGURATION
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Naya model use kar rahe hain jo fast hai
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. BOT HANDLERS
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Namaste! Main aapka AI Translator Bot hoon.\n\n"
        "Mujhe koi bhi message bhejiye, main use Hindi aur Gujarati mein translate kar dunga."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # AI ko instruction dena
        prompt = f"Translate the following text into Hindi and Gujarati. Format it clearly.\nText: {message.text}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "⚠️ AI ne koi response nahi diya. Phir se koshish karein.")
            
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Thodi dikkat aa rahi hai. Shayad API key ya network ka issue hai.")

# 5. EXECUTION
if __name__ == "__main__":
    # Flask ko alag thread mein chalana
    t = threading.Thread(target=run_flask)
    t.start()
    
    # Bot polling start karna
    print("Bot is starting polling...")
    bot.infinity_polling()

