import requests
import json
import time

# A list of different Overpass servers to try if one is busy
SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.n.host.de/api/interpreter"
]

# A very efficient query: Nodes (points) only for hospitals and clinics in a box around Bangladesh
query = """
[out:json][timeout:180];
(
  node["amenity"="hospital"](20.5,88.0,26.8,92.8);
  node["amenity"="clinic"](20.5,88.0,26.8,92.8);
);
out body;
"""

success = False
for url in SERVERS:
    print(f"Trying server: {url}...")
    try:
        # We use a long timeout (3 minutes) to give the server time to think
        response = requests.get(url, params={'data': query}, timeout=190)
        
        if response.status_code == 200:
            data = response.json()
            features = []
            for element in data.get('elements', []):
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [element['lon'], element['lat']]
                    },
                    "properties": element.get('tags', {})
                })
            
            with open('bangladesh-map/health_facilities.geojson', 'w') as f:
                json.dump({"type": "FeatureCollection", "features": features}, f, indent=2)
            
            print(f"SUCCESS! Saved {len(features)} facilities to bangladesh-map/health_facilities.geojson")
            success = True
            break
        else:
            print(f"Server returned status {response.status_code}. Moving to next mirror...")
            
    except Exception as e:
        print(f"Connection failed: {e}. Moving to next mirror...")
    
    # Wait a tiny bit before trying the next one to be polite to the servers
    time.sleep(2)

if not success:
    print("\nAll servers are currently busy with high traffic. Please wait 5-10 minutes and run 'python3 fetch_health_data.py' again.")
