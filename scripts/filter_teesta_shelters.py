import json

# Define the Teesta Basin bounding box (approximate for the 5 key districts)
TEESTA_BBOX = {
    "min_lat": 25.2,
    "max_lat": 26.5,
    "min_lon": 88.5,
    "max_lon": 89.8
}

def filter_shelters():
    try:
        with open('../data/safe_hubs.geojson', 'r') as f:
            data = json.load(f)
        
        teesta_shelters = []
        for feature in data['features']:
            lon, lat = feature['geometry']['coordinates']
            
            if (TEESTA_BBOX['min_lat'] <= lat <= TEESTA_BBOX['max_lat'] and
                TEESTA_BBOX['min_lon'] <= lon <= TEESTA_BBOX['max_lon']):
                teesta_shelters.append(feature)
        
        output = {
            "type": "FeatureCollection",
            "features": teesta_shelters
        }
        
        with open('../data/teesta_safe_hubs.geojson', 'w') as f:
            json.dump(output, f, indent=2)
            
        print(f"Filtered {len(teesta_shelters)} shelters in the Teesta Basin area.")
        
    except Exception as e:
        print(f"Error filtering shelters: {e}")

if __name__ == "__main__":
    filter_shelters()
