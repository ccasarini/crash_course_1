import requests
import json
import os
import time

def fetch_single_district(district_name):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Simple query for one district
    overpass_query = f"""
    [out:json][timeout:30];
    relation["boundary"="administrative"]["admin_level"="5"]["name"~"{district_name}"];
    out body;
    >;
    out skel qt;
    """

    print(f"Fetching: {district_name}")
    try:
        response = requests.get(overpass_url, params={'data': overpass_query})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {district_name}")
            return None
    except Exception as e:
        print(f"Exception for {district_name}: {e}")
        return None

def process_osm_json(osm_data):
    # This is a basic OSM-to-GeoJSON converter
    nodes = {node['id']: (node['lon'], node['lat']) for node in osm_data['elements'] if node['type'] == 'node'}
    ways = {way['id']: [nodes[node_id] for node_id in way.get('nodes', []) if node_id in nodes] 
            for way in osm_data['elements'] if way['type'] == 'way'}
    
    features = []
    for rel in osm_data['elements']:
        if rel['type'] == 'relation':
            coords = []
            for member in rel.get('members', []):
                if member['type'] == 'way' and member['ref'] in ways:
                    coords.extend(ways[member['ref']])
            
            if coords:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coords]
                    },
                    "properties": rel.get('tags', {})
                })
    return features

def main():
    districts = ["Lalmonirhat", "Nilphamari", "Gaibandha", "Kurigram", "Rangpur"]
    all_features = []
    
    for d in districts:
        osm_data = fetch_single_district(d)
        if osm_data:
            features = process_osm_json(osm_data)
            all_features.extend(features)
        
        # Pause slightly between requests to be nice to the API
        time.sleep(2)
    
    if all_features:
        geojson = {
            "type": "FeatureCollection",
            "features": all_features
        }
        output_path = 'data/teesta_districts.geojson'
        with open(output_path, 'w') as f:
            json.dump(geojson, f, indent=2)
        print(f"Success! Saved {len(all_features)} districts to {output_path}")
    else:
        print("Failed to fetch any district data.")

if __name__ == "__main__":
    main()
