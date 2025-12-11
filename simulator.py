import json
import time
import random
import os

# Configuration
DATA_FILE = "data.json"

def generate_live_data():
    """Generates a random state of the music market."""
    
    # 1. Simulate Forecast Data (Time Series)
    # As time moves, the 'future' becomes slightly different
    base_sales = random.randint(4000, 6000)
    noise = [random.randint(-500, 800) for _ in range(7)]
    forecast_p50 = [
        base_sales + (i * 1000) + n 
        for i, n in enumerate(noise)
    ]

    # 2. Simulate Customer Clusters (Moving dots)
    cluster1_x = [random.randint(10, 25) for _ in range(10)]
    cluster1_y = [random.randint(20, 35) for _ in range(10)]
    
    # 3. Simulate System Status (Architecture)
    latency = random.randint(15, 120)
    token_usage = random.randint(40000, 90000)

    # 4. Construct the JSON Structure
    data = {
        "timestamp": time.time(),
        "system_status": {
            "api_latency_ms": latency,
            "gpu_load_percent": random.randint(20, 95),
            "tokens_used": token_usage
        },
        "forecast": {
            "labels": ['T+0', 'T+15', 'T+30', 'T+45', 'T+60', 'T+75', 'T+90'],
            "p50": forecast_p50,
            "p90": [x * 1.15 for x in forecast_p50],
            "p10": [x * 0.85 for x in forecast_p50]
        },
        "clusters": {
            "high_vol": {"x": cluster1_x, "y": cluster1_y},
            "niche": {"x": [x + 30 for x in cluster1_x], "y": [y + 30 for y in cluster1_y]},
            "target": {"x": [43], "y": [56]}
        },
        "latest_alert": {
            "msg": f"Real-time update received. Latency: {latency}ms",
            "type": "info" if latency < 80 else "warning"
        }
    }
    
    return data

if __name__ == "__main__":
    print(f"--- 📡 DATA SIMULATOR STARTED ---")
    print(f"Writing to {DATA_FILE} every 3 seconds...")
    
    while True:
        live_data = generate_live_data()
        
        # Atomic write to avoid reading partial files
        with open(DATA_FILE, "w") as f:
            json.dump(live_data, f, indent=2)
            
        print(f"⚡ Updated {DATA_FILE} at {time.ctime()}")
        time.sleep(3)