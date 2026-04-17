import requests
import json
import time
from shapely.geometry import shape, Point

# 1. Fetch Shelter Data from Overpass (OSM)
# This includes general shelters, cyclone shelters, and emergency social facilities
SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

# Query for nodes and ways tagged as shelters or emergency social facilities
query = """
[out:json][timeout:180];
(
  node["amenity"="shelter"](20.5,88.0,26.8,92.8);
  way["amenity"="shelter"](20.5,88.0,26.8,92.8);
  node["social_facility"="emergency_shelter"](20.5,88.0,26.8,92.8);
  way["social_facility"="emergency_shelter"](20.5,88.0,26.8,92.8);
  node["shelter_type"~"cyclone|flood"](20.5,88.0,26.8,92.8);
  way["shelter_type"~"cyclone|flood"](20.5,88.0,26.8,92.8);
);
out center body;
"""

raw_features = []
success = False

print("Fetching Safe Hub (Shelter) data from Overpass API...")
for url in SERVERS:
    try:
        response = requests.get(url, params={'data': query}, timeout=190)
        if response.status_code == 200:
            data = response.json()
            for element in data.get('elements', []):
                # Handle both nodes (points) and ways (using 'center')
                coords = [element['lon'], element['lat']] if element['type'] == 'node' else [element['center']['lon'], element['center']['lat']]
                raw_features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": coords
                    },
                    "properties": element.get('tags', {})
                })
            success = True
            print(f"Successfully retrieved {len(raw_features)} potential shelters.")
            break
        else:
            print(f"Server {url} returned status {response.status_code}. Trying next...")
    except Exception as e:
        print(f"Error with server {url}: {e}")
    time.sleep(2)

if not success:
    print("Failed to fetch data from all Overpass servers.")
    exit(1)

# 2. Filter by Bangladesh Border
print("Filtering shelters to ensure they are within Bangladesh borders...")
try:
    with open('../data/bangladesh_border.geojson', 'r') as f:
        border_data = json.load(f)
        border_poly = shape(border_data['features'][0]['geometry'])

    filtered_features = []
    for feature in raw_features:
        point = Point(feature['geometry']['coordinates'])
        if border_poly.contains(point):
            filtered_features.append(feature)

    # 3. Save the results
    output = {
        "type": "FeatureCollection",
        "features": filtered_features
    }

    with open('../data/safe_hubs.geojson', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Success! Saved {len(filtered_features)} Safe Hubs to ../data/safe_hubs.geojson")

except FileNotFoundError:
    print("Error: bangladesh_border.geojson not found in ../data/. Saving unfiltered data.")
    with open('../data/safe_hubs.geojson', 'w') as f:
        json.dump({"type": "FeatureCollection", "features": raw_features}, f, indent=2)
except Exception as e:
    print(f"An error occurred during filtering: {e}")
