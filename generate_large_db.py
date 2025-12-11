import json
import random
import uuid

def generate_large_database(num_competitors=50, num_customers=5000):
    print(f"--- GENERATING LARGE DATABASE ({num_customers} customers) ---")
    
    # 1. Current Release (Static)
    current_release = {
        "product_id": "REL-2024-X1",
        "artist": "Lunar Echo",
        "genre": "Melodic Techno",
        "mood_tags": ["Dark", "Hypnotic", "Driving"],
        "bpm": 126,
        "energy_score": 0.85,
        "marketing_budget": 15000,
        "workflow_status": "Marketing", # Default start stage
        "historical_daily_sales": [random.randint(100, 500) for _ in range(30)]
    }

    # 2. Generate Competitors
    competitors = []
    for i in range(num_competitors):
        competitors.append({
            "name": f"Competitor {i+1}",
            "bpm": random.randint(118, 135),
            "energy_score": round(random.uniform(0.5, 1.0), 2),
            "sales_velocity": random.randint(50, 1000)
        })

    # 3. Generate Customers
    customers = []
    regions = ["EMEA", "NA", "APAC", "LATAM"]
    for i in range(num_customers):
        customers.append({
            "id": f"B2B-{str(uuid.uuid4())[:8]}",
            "name": f"Customer {i+1} {random.choice(['Records', 'Club', 'Distro', 'Radio'])}",
            "avg_order_val": random.randint(500, 10000),
            "genre_affinity": round(random.uniform(0.1, 0.99), 2),
            "region": random.choice(regions)
        })

    # 4. Market Signals
    market_signals = {
        "competitor_drop": random.choice([True, False]),
        "tiktok_trend_volume": random.choice(["High", "Medium", "Low"]),
        "similar_artist_performance": f"{random.choice(['+', '-'])}{random.randint(5, 25)}%"
    }

    full_db = {
        "current_release": current_release,
        "competitors": competitors,
        "customers": customers,
        "market_signals": market_signals
    }

    with open("database.json", "w") as f:
        json.dump(full_db, f, indent=2)
    
    print(f"✅ Success: database.json created with {len(customers)} customers.")

if __name__ == "__main__":
    generate_large_database()
