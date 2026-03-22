import os
import requests
from flask import Flask, request, render_template_string
from telebot import TeleBot, types

# --- CONFIGURATION (IMPORTANT!) ---
# Replace these with your actual tokens/keys
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE') 
# MINI_APP_URL will be your Koyeb URL + '/miniapp' after deployment
MINI_APP_URL = os.environ.get('MINI_APP_URL', 'https://your-koyeb-app-name.koyeb.app/miniapp')

# Initialize Flask App and TeleBot
app = Flask(__name__)
bot = TeleBot(BOT_TOKEN, threaded=False) # threaded=False for better cloud hosting compatibility

# --- TELEGRAM BOT LOGIC ---

# 1. Handle /start command - Welcomes users and shows the Mini App button
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_first_name = message.from_user.first_name
    
    # Create the inline keyboard button to launch the Mini App
    markup = types.InlineKeyboardMarkup()
    # The 'web_app' key is what makes it a Mini App button
    mini_app_btn = types.InlineKeyboardButton(text="🌍 Open Translator", web_app=types.WebAppInfo(url=MINI_APP_URL))
    markup.add(mini_app_btn)

    welcome_text = f"Hello {user_first_name}! Welcome to the Global AI Translator.\n\n" \
                   f"Tap the button below to launch our translation Mini App."
    
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# --- FLASK WEB SERVER LOGIC (For Webhook and Mini App Hosting) ---

# 2. Webhook route to receive messages from Telegram
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content-type', 403

# 3. Route to serve the Mini App (templates/index.html)
@app.route('/miniapp', methods=['GET'])
def serve_miniapp():
    # Attempt to read the index.html from the 'templates' folder
    try:
        # Get the path to index.html within the 'templates' folder
        template_path = os.path.join(app.root_path, 'templates', 'index.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return render_template_string(html_content)
    except FileNotFoundError:
        # Fallback if index.html is missing (useful for debugging)
        return "<h1>Error: templates/index.html not found!</h1>", 404

# 4. Root route (just a placeholder)
@app.route('/', methods=['GET'])
def index():
    return "<h1>Translator Bot Server is Running!</h1>"

# --- MAIN EXECUTION ---

if __name__ == '__main__':
    # When deployed on platforms like Koyeb, the platform sets the PORT variable
    port = int(os.environ.get('PORT', 5000))
    
    # In production, we'd set up a webhook here. For local/testing, we might use polling.
    # If BOT_TOKEN and MINI_APP_URL are not set as env vars, assume polling for local test.
    if 'YOUR_TELEGRAM_BOT_TOKEN_HERE' in BOT_TOKEN:
        print("Starting bot in polling mode (local test)...")
        bot.remove_webhook()
        bot.infinity_polling()
    else:
        # Production deployment (webhook mode is generally better for cloud hosting)
        # Note: Koyeb setup will require setting up the webhook URL on Telegram.
        # This setup typically requires a separate deployment step to set the webhook.
        # To keep it simple, you could also use polling on Koyeb, but webhook is cleaner.
        print("Starting Flask server for webhook...")
        app.run(host='0.0.0.0', port=port)
