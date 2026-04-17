import json

# Define the Teesta Basin bounding box (same as used for shelters)
TEESTA_BBOX = {
    "min_lat": 25.2,
    "max_lat": 26.5,
    "min_lon": 88.5,
    "max_lon": 89.8
}

def filter_health_sites():
    try:
        with open('../data/health_facilities.geojson', 'r') as f:
            data = json.load(f)
        
        teesta_health = []
        for feature in data['features']:
            lon, lat = feature['geometry']['coordinates']
            
            if (TEESTA_BBOX['min_lat'] <= lat <= TEESTA_BBOX['max_lat'] and
                TEESTA_BBOX['min_lon'] <= lon <= TEESTA_BBOX['max_lon']):
                teesta_health.append(feature)
        
        output = {
            "type": "FeatureCollection",
            "features": teesta_health
        }
        
        with open('../data/teesta_health_facilities.geojson', 'w') as f:
            json.dump(output, f, indent=2)
            
        print(f"Filtered {len(teesta_health)} health sites in the Teesta Basin area.")
        
    except Exception as e:
        print(f"Error filtering health sites: {e}")

if __name__ == "__main__":
    filter_health_sites()
