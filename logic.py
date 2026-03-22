import os
import google.generativeai as genai

# --- CONFIGURATION ---
# Apni Gemini API Key yahan dalein ya Koyeb ke Environment Variables mein set karein
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBMM464tvuXMj0cqtse3lhyN_8EBZ2I4eY')

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_ai_translation(user_text, target_language):
    """
    User ke text ko analyze karke 3-line format mein translate karta hai.
    """
    
    # AI ke liye strict instruction (Prompt)
    prompt = f"""
    You are an expert translator. Translate the following text: '{user_text}' to {target_language}.
    
    Provide the output strictly in this 3-line format:
    1. Text: [Original source text]
    2. Pronounce: [How to pronounce the source text using {target_language} script phonetically]
    3. Translate: [The actual meaning in {target_language}]

    Example if China to Gujarati:
    1. Text: 你好
    2. Pronounce: નિ-હાઓ
    3. Translate: નમસ્તે
    """

    try:
        response = model.generate_content(prompt)
        
        # Agar AI response de raha hai toh use return karein
        if response.text:
            return response.text
        else:
            return "AI Error: Response empty."
            
    except Exception as e:
        print(f"Error in Gemini AI: {e}")
        return "Sorry, AI abhi thoda busy hai. Please baad mein try karein."

# Test karne ke liye (Optional)
# print(get_ai_translation("How are you?", "Gujarati"))
