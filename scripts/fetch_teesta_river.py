import requests
import json
import os

def fetch_teesta_river():
    # 1. Define the Overpass API URL
    overpass_url = "https://overpass-api.de/api/interpreter"

    # 2. Define the Query
    # [out:json] -> We want the result in JSON format
    # way["waterway"="river"]["name"~"Teesta"] -> Find lines tagged as 'river' with 'Teesta' in the name
    # (._; >;); -> This tells Overpass to include the individual points (nodes) that make up the lines
    overpass_query = """
    [out:json][timeout:25];
    (
      way["waterway"="river"]["name"~"Teesta"];
    );
    out body;
    >;
    out skel qt;
    """

    print("Sending request to Overpass API... this may take a moment.")
    
    # 3. Send the request
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        data = response.json()
        print("Data received! Processing into GeoJSON...")
        
        # 4. Convert OSM JSON to GeoJSON
        # We manually build the GeoJSON structure here
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        # Extract nodes (points) for lookup
        nodes = {node['id']: (node['lon'], node['lat']) for node in data['elements'] if node['type'] == 'node'}
        
        # Extract ways (lines)
        for element in data['elements']:
            if element['type'] == 'way':
                coordinates = []
                for node_id in element.get('nodes', []):
                    if node_id in nodes:
                        coordinates.append(nodes[node_id])
                
                if coordinates:
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "LineString",
                            "coordinates": coordinates
                        },
                        "properties": element.get('tags', {})
                    }
                    geojson['features'].append(feature)
        
        # 5. Save the file
        output_path = 'data/teesta_river.geojson'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(geojson, f, indent=2)
            
        print(f"Success! Teesta River GeoJSON saved to: {output_path}")
    else:
        print(f"Error: API returned status code {response.status_code}")

if __name__ == "__main__":
    fetch_teesta_river()
