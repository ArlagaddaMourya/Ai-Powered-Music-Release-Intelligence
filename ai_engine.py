import google.generativeai as genai
import os
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression
import numpy as np

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 2. Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ Warning: GEMINI_API_KEY not found. AI features will fail.")

# --- THE AI AGENT FUNCTION ---
def chat_with_agent(query, current_release, batch_context):
    """
    Sends metadata to Gemini Pro to generate marketing assets.
    """
    if not api_key:
        return "Error: AI Key missing. Check .env file."

    try:
        # Initialize Model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Construct the Prompt
        system_prompt = f"""
        You are a Music Marketing AI.
        
        TRACK METADATA:
        Artist: {current_release.get('artist', 'Unknown')}
        Title: {current_release.get('product_id', 'Unknown')}
        Genre: {current_release.get('genre', 'Unknown')}
        Moods: {", ".join(current_release.get('mood_tags', []))}
        
        CONTEXT:
        {batch_context}
        
        TASK:
        {query}
        
        OUTPUT FORMAT:
        Keep it concise. Do not use markdown. Just raw text.
        """
        
        # Generate Content
        response = model.generate_content(system_prompt)
        return response.text
        
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def generate_forecast_logic(history):
    """
    Uses Linear Regression to predict the next 7 days based on history.
    """
    # 1. Prepare Data for Training
    # X = Day numbers (0, 1, 2, ...), y = Sales
    X = np.array(range(len(history))).reshape(-1, 1)
    y = np.array(history)

    # 2. Train the Real Model
    model = LinearRegression()
    model.fit(X, y)

    # 3. Predict the Future (Next 7 days)
    last_day = len(history)
    future_days = np.array(range(last_day, last_day + 7)).reshape(-1, 1)
    predictions = model.predict(future_days)

    # 4. Return results ensuring no negative sales
    return [max(0, int(p)) for p in predictions]