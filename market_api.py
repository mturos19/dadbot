import requests
import json
import time
from typing import Optional, Dict, Any
from datetime import datetime

BASE_URL = "https://api.darkerdb.com/v1/market"

def get_all_market_items(
    limit: int = 100,  # Increased default limit
    condense: bool = True
) -> Dict[str, Any]:
    """
    Fetch all market items from Dark and Darker API.
    
    Args:
        limit: Maximum number of results to return
        condense: Whether to condense the results
    
    Returns:
        Dict containing the API response
    """
    params = {
        'limit': limit,
        'condense': 1 if condense else 0
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching market data: {e}")
        return {}

def monitor_market(
    interval: float = 60.0,  # Time between requests in seconds
    output_file: str = "market_data.json",
    store_history: bool = True
):
    """
    Continuously monitor the market and save results.
    
    Args:
        interval: Time between API calls in seconds
        output_file: File to save the latest market data
        store_history: If True, saves each response with timestamp
    """
    print(f"Starting market monitor. Polling every {interval} seconds...")
    
    while True:
        try:
            # Get current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Fetch market data
            market_data = get_all_market_items()
            
            if market_data:
                # Save latest data
                with open(output_file, 'w') as f:
                    json.dump(market_data, f, indent=2)
                print(f"[{timestamp}] Market data updated in {output_file}")
                
                # Optionally save historical data
                if store_history:
                    history_file = f"data/raw/market_data_{timestamp}.json"
                    with open(history_file, 'w') as f:
                        json.dump(market_data, f, indent=2)
            
            # Wait for next interval
            time.sleep(interval)
            
        except KeyboardInterrupt:
            print("\nMarket monitor stopped by user")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

# Test the API
if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    os.makedirs("data/raw", exist_ok=True)
    
    # Start monitoring
    monitor_market(
        interval=60,  # Poll every 60 seconds
        output_file="data/raw/latest_market_data.json",
        store_history=True
    )