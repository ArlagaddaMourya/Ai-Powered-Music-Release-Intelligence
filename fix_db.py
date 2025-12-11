import json
import os

# 1. Define the correct, perfect structure manually
correct_structure = {
  "current_release": {
    "product_id": "REL-2024-X1",
    "artist": "Lunar Echo",
    "genre": "Melodic Techno",
    "bpm": 126,
    "energy_score": 0.85,
    "marketing_budget": 15000,
    "historical_daily_sales": [120, 135, 142, 110, 155, 170, 190, 210, 205, 230, 245, 260, 280, 290]
  },
  "competitors": [
    { "name": "Solar Flare", "bpm": 128, "energy_score": 0.92, "sales_velocity": 450 },
    { "name": "Deep State", "bpm": 124, "energy_score": 0.78, "sales_velocity": 320 },
    { "name": "Neon Horizon", "bpm": 130, "energy_score": 0.88, "sales_velocity": 410 }
  ],
  "customers": [
    { "id": "B2B-01", "name": "Berlin Underground", "avg_order_val": 4500, "genre_affinity": 0.95, "region": "EMEA" },
    { "id": "B2B-02", "name": "Tokyo Synth", "avg_order_val": 3200, "genre_affinity": 0.88, "region": "APAC" },
    { "id": "B2B-03", "name": "NY Club Corp", "avg_order_val": 5100, "genre_affinity": 0.72, "region": "NA" }
  ],
  "market_signals": {
    "competitor_drop": True,
    "tiktok_trend_volume": "High",
    "similar_artist_performance": "+15%"
  }
}

# 2. Force write this structure to the file
file_path = 'database.json'

print(f"Old file size: {os.path.getsize(file_path)} bytes")

with open(file_path, 'w') as f:
    json.dump(correct_structure, f, indent=2)

print("------------------------------------------------")
print("✅ FIXED: database.json has been overwritten.")
print("✅ It is now a Dictionary (Object), not a List.")
print("------------------------------------------------")r