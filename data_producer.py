import json
import random

def generate_database():
    print("--- GENERATING DATABASE.JSON ---")
    
    # 1. Create the Current Release
    current_release = {
        "product_id": "REL-2024-X1",
        "artist": "Lunar Echo",
        "genre": "Melodic Techno",
        "mood_tags": ["Dark", "Hypnotic", "Driving"],
        "bpm": 126,
        "energy_score": 0.85,
        "marketing_budget": 15000,
        "historical_daily_sales": [
            120, 135, 140, 155, 150, 180, 200, 210, 205, 230,
            250, 270, 260, 290, 310, 305, 320, 340, 360, 350
        ]
    }

    # 2. Create Competitors (for the Market Radar)
    competitors = [
        {"name": "Solar Flare", "bpm": 128, "energy_score": 0.92, "sales_velocity": 450},
        {"name": "Deep Blue", "bpm": 122, "energy_score": 0.65, "sales_velocity": 120},
        {"name": "Neon Sky", "bpm": 130, "energy_score": 0.78, "sales_velocity": 890},
        {"name": "Void State", "bpm": 125, "energy_score": 0.88, "sales_velocity": 310}
    ]

    # 3. Create Customers (for the Map)
    customers = [
        {"id": "B2B-01", "name": "Berlin Underground", "avg_order_val": 4500, "genre_affinity": 0.95, "region": "EMEA"},
        {"id": "B2B-02", "name": "Tokyo Beats", "avg_order_val": 3200, "genre_affinity": 0.88, "region": "APAC"},
        {"id": "B2B-03", "name": "London Vinyl", "avg_order_val": 2800, "genre_affinity": 0.45, "region": "EMEA"},
        {"id": "B2B-04", "name": "NY Mainstream", "avg_order_val": 8500, "genre_affinity": 0.12, "region": "NA"},
        {"id": "B2B-05", "name": "Ibiza Reseller", "avg_order_val": 6000, "genre_affinity": 0.91, "region": "EMEA"},
        {"id": "B2B-06", "name": "Paris Indie", "avg_order_val": 1500, "genre_affinity": 0.60, "region": "EMEA"}
    ]

    # 4. Market Signals
    market_signals = {
        "competitor_drop": True,
        "tiktok_trend_volume": "High",
        "similar_artist_performance": "+15%"
    }

    full_db = {
        "current_release": current_release,
        "competitors": competitors,
        "customers": customers,
        "market_signals": market_signals
    }

    with open("database.json", "w") as f:
        json.dump(full_db, f, indent=2)
    
    print("✅ Success: database.json created.")

if __name__ == "__main__":
    generate_database()