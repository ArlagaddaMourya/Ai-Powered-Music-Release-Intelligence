import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("------------------------------------------------")
print("🔍 DIAGNOSTIC TEST")
print("------------------------------------------------")

# 2. Check if key exists
if not api_key:
    print("❌ ERROR: API Key NOT found.")
    print("   Make sure you have a file named '.env' in this folder.")
    print("   It should contain: GEMINI_API_KEY=your_key_here")
else:
    print(f"✅ API Key found (starts with: {api_key[:6]}...)")

    try:
        print("⏳ Connecting to Google Gemini...")
        genai.configure(api_key=api_key)
        
        # --- STEP 3: LIST MODELS FIRST (To debug the 404 error) ---
        print("📋 Checking available models for your API key:")
        available_models = []
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"   - {m.name}")
                    available_models.append(m.name)
        except Exception as e:
            print(f"   ⚠️ Could not list models: {e}")

        # --- STEP 4: SELECT A VALID MODEL ---
        # We try to use Flash, but if not available, we pick the first one from the list
        target_model = 'gemini-1.5-flash'
        
        # Check if our target needs the 'models/' prefix or not based on the list result
        if f"models/{target_model}" in available_models:
            target_model = f"models/{target_model}"
        elif available_models:
            # If flash isn't there, just pick the first one available
            print(f"\n⚠️ 'gemini-1.5-flash' not found. Switching to: {available_models[0]}")
            target_model = available_models[0]

        print(f"\n🚀 Testing generation with model: {target_model}")
        
        # --- STEP 5: GENERATE CONTENT ---
        model = genai.GenerativeModel(target_model)
        response = model.generate_content("Say 'Hello! I am working.' if you can hear me.")
        
        print("------------------------------------------------")
        print(f"✅ SUCCESS! AI Responded: {response.text}")
        print("------------------------------------------------")
        
    except Exception as e:
        print("------------------------------------------------")
        print("❌ CONNECTION FAILED")
        print(f"Error details: {e}")
        print("------------------------------------------------")
        print("Common fixes:")
        print("1. Your API key might not have access to the specific model name.")
        print("2. Check the list of models printed above and copy one exactly.")