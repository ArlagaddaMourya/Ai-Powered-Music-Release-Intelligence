import os
import json
import random
import numpy as np
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# --- MACHINE LEARNING IMPORTS ---
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# --- CONFIGURATION ---
os.environ['GRPC_DNS_RESOLVER'] = 'native'
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found.")
else:
    genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    context_id: str = "REL-2024-X1"

# --- DATA HELPERS ---
def load_data():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

def get_release_by_id(data, release_id):
    return next((r for r in data.get('releases', []) if r['id'] == release_id), None)

# --- API ENDPOINTS ---

@app.get("/")
async def read_root():
    return FileResponse('index.html')

@app.get("/api/database")
async def get_full_database():
    return load_data()

@app.get("/api/release/{release_id}")
async def get_specific_release(release_id: str):
    data = load_data()
    release = get_release_by_id(data, release_id)
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    return release

# --- 1. FORECASTING (Added Gradient Boosting) ---
@app.get("/api/forecast/{release_id}")
async def get_forecast(release_id: str, algo: str = "linear"):
    data = load_data()
    release = get_release_by_id(data, release_id)
    if not release: return []
    
    history = release['stats']['history']
    days_to_predict = 7
    predictions = []

    X = np.array(range(len(history))).reshape(-1, 1)
    y = np.array(history)

    # A. LINEAR REGRESSION
    if algo == "linear":
        z = np.polyfit(X.flatten(), y, 1)
        p = np.poly1d(z)
        for i in range(days_to_predict):
            predictions.append(max(0, int(p(len(history) + i))))

    # B. POLYNOMIAL REGRESSION
    elif algo == "polynomial":
        z = np.polyfit(X.flatten(), y, 2)
        p = np.poly1d(z)
        for i in range(days_to_predict):
            predictions.append(max(0, int(p(len(history) + i))))

    # C. GRADIENT BOOSTING (NEW!)
    elif algo == "gradient_boosting":
        # GBR is powerful but needs reshaping. 
        model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=42)
        model.fit(X, y)
        
        for i in range(days_to_predict):
            next_day = np.array([[len(history) + i]])
            pred = model.predict(next_day)[0]
            predictions.append(max(0, int(pred)))

    # D. MOVING AVERAGE
    elif algo == "moving_average":
        window = 3
        avg_val = sum(history[-window:]) / window
        for i in range(days_to_predict):
            val = avg_val * (1 + (0.01 * i))
            predictions.append(max(0, int(val)))

    # E. EXPONENTIAL
    elif algo == "exponential":
        alpha = 0.8
        last_val = history[0]
        for val in history[1:]:
            last_val = alpha * val + (1 - alpha) * last_val
        for i in range(days_to_predict):
            predictions.append(max(0, int(last_val)))

    else:
        return await get_forecast(release_id, "linear")
        
    return predictions

# --- 2. CLUSTERING (K-MEANS) ---
@app.get("/api/clusters")
async def get_customer_segments():
    """
    Uses K-Means to group customers into 3 segments based on:
    1. Average Order Value (Money)
    2. BPM Preference (Taste)
    """
    data = load_data()
    customers = data.get('customers', [])
    if not customers: return []

    # Prepare Data for ML (Money, BPM)
    X = np.array([[c['avg_order_val'], c['bpm']] for c in customers])
    
    # Scale Data (Important for K-Means)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Run K-Means (3 Clusters: e.g., Low, Mid, High value)
    kmeans = KMeans(n_clusters=min(3, len(customers)), random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    labels = kmeans.labels_

    # Format output for Chart.js
    segments = []
    for i, customer in enumerate(customers):
        segments.append({
            "name": customer['name'],
            "x": customer['bpm'],      # X-Axis: Taste
            "y": customer['avg_order_val'], # Y-Axis: Money
            "cluster": int(labels[i])  # Color group
        })
        
    return segments

# --- 3. ADVANCED CMO STRATEGY ---
@app.get("/api/marketing/{release_id}")
async def get_marketing_strategy(release_id: str):
    data = load_data()
    release = get_release_by_id(data, release_id)
    if not release: return {"strategy": "Release not found"}
    
    # We ask the AI to act as a Chief Marketing Officer and return stylized HTML
    prompt = f"""
    Act as a visionary Chief Marketing Officer for a top record label.
    Create a high-stakes launch strategy for:
    
    ARTIST: {release['artist']}
    TRACK: {release['track_name']}
    GENRE: {release['genre']}
    BUDGET: ${release['stats']['budget']}
    SENTIMENT: {release['stats']['sentiment']}/10
    
    OUTPUT FORMAT:
    Return ONLY raw HTML code (no markdown backticks, no ```html wrapper). 
    Use Tailwind CSS classes for styling. Make it colorful and modern.
    
    STRUCTURE:
    1. A "Campaign Vibe" headline (Bold, large).
    2. Three distinct colored cards (divs with rounded corners and shadows):
       - Card 1 (Gradient Purple/Pink): "The Viral Hook" (Specific TikTok/Reels concept).
       - Card 2 (Blue): "Target Persona" (Describe the exact fan avatar).
       - Card 3 (Green): "Budget Split" (Show exact percentages for Ads vs Influencers vs Content).
    3. A final "CMO Note" at the bottom in italics.
    
    Do not use markdown. Just raw HTML string.
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Clean up if AI adds markdown wrapper by mistake
        clean_html = response.text.replace("```html", "").replace("```", "")
        return {"strategy": clean_html}
    except:
        return {"strategy": "<div class='text-red-500'>AI Connection Error. Check API Key.</div>"}

# --- 4. FAST ASSET GENERATION ---
@app.get("/api/generate-asset/{release_id}")
async def generate_asset(release_id: str):
    data = load_data()
    release = get_release_by_id(data, release_id)
    if not release: return {"error": "No release"}

    genre_styles = {
        "Melodic Techno": "neon lights, futuristic, purple haze, abstract geometric, 4k render",
        "Deep House": "sunset, ibiza beach, luxury yacht, cocktail, cinematic lighting",
        "Cyberpunk Bass": "cyberpunk city, glitch art, matrix code, neon rain, sci-fi",
        "Liquid DnB": "fluid art, blue water, abstract flow, motion blur, smooth",
        "Lo-Fi Beats": "anime aesthetic, rainy window, cozy room, cat, coffee",
        "Synthwave": "retro car, 80s grid, palm trees, vaporwave, neon pink sun",
        "Industrial Techno": "concrete texture, factory smoke, dark warehouse, industrial",
        "Future Bass": "colorful smoke, festival crowd, lasers, vibrant clouds",
        "Trap": "urban city night, gold chain, luxury sports car, street lights",
        "Ambient": "nebula, stars, galaxy, aurora borealis, peaceful nature",
        "Trance": "laser light show, tunnel, speed lines, energy, euphoria",
        "Dubstep": "speaker system, shockwave, lightning, explosion, dark energy",
        "Indie Dance": "disco ball, dance floor, retro fashion, vinyl record",
        "Nu-Disco": "glitter, roller skates, 70s style, funk, vibrant colors",
        "Hardstyle": "red lasers, massive stage, fireworks, hardstyle festival"
    }

    genre = release.get('genre', 'Unknown')
    base_prompt = genre_styles.get(genre, f"{genre} music abstract art")
    encoded_prompt = base_prompt.replace(" ", "%20")
    random_seed = random.randint(1000, 9999)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={random_seed}"
    return {"image_url": image_url, "keywords": base_prompt}

# --- 5. TRIGGERS & CHAT ---
@app.get("/api/triggers/{release_id}")
async def get_triggers(release_id: str):
    data = load_data()
    release = get_release_by_id(data, release_id)
    if not release: return []
    signals = release.get('market_signals', {})
    alerts = []
    if signals.get('competitor_drop'):
        alerts.append({"type": "Competition Alert", "color": "red", "msg": "Major competitor released today."})
    if signals.get('tiktok_trend') in ["High", "Viral"]:
        alerts.append({"type": "Viral Signal", "color": "green", "msg": "Genre trending on TikTok."})
    return alerts

@app.post("/api/chat")
async def chat_with_data(request: ChatRequest):
    data = load_data()
    full_context = json.dumps(data)
    prompt = f"""
    You are the Chief Intelligence Officer.
    DATABASE: {full_context}
    User Question: {request.message}
    Answer professionally and concise.
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        return {"response": f"AI Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    print("--- Enterprise Label Platform Online ---")
    uvicorn.run(app, host="127.0.0.1", port=8001)