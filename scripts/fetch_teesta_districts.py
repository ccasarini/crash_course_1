import requests
import json
import os

def fetch_teesta_districts():
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # We query for 'relation' where 'admin_level'=5 (Districts in Bangladesh) 
    # and the name matches our list.
    districts = ["Lalmonirhat", "Nilphamari", "Gaibandha", "Kurigram", "Rangpur"]
    
    # Build the query string
    district_queries = "".join([f'relation["boundary"="administrative"]["admin_level"="5"]["name"~"{d}"];' for d in districts])
    
    overpass_query = f"""
    [out:json][timeout:50];
    (
      {district_queries}
    );
    out body;
    >;
    out skel qt;
    """

    print("Fetching district boundaries from OSM... this might take a minute.")
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        data = response.json()
        print("Data received! Converting to GeoJSON...")
        
        # A simple way to handle OSM relations for boundaries
        # Note: Complex boundaries (multipolygons) can be tricky, 
        # but for this scale, we'll try a simplified approach.
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        # We'll use a library-free approach to parse the relations into polygons
        # Extract nodes
        nodes = {node['id']: (node['lon'], node['lat']) for node in data['elements'] if node['type'] == 'node'}
        
        # Extract ways
        ways = {way['id']: [nodes[node_id] for node_id in way.get('nodes', []) if node_id in nodes] 
                for way in data['elements'] if way['type'] == 'way'}
        
        # Extract relations (the actual districts)
        for rel in data['elements']:
            if rel['type'] == 'relation':
                name = rel.get('tags', {}).get('name', 'Unknown')
                print(f"Processing: {name}")
                
                # Combine ways into a single boundary
                # This is a simplification; real relations can have inner/outer rings
                coords = []
                for member in rel.get('members', []):
                    if member['type'] == 'way' and member['ref'] in ways:
                        coords.extend(ways[member['ref']])
                
                if coords:
                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [coords] # Simplified: assumes one single loop
                        },
                        "properties": rel.get('tags', {})
                    }
                    geojson['features'].append(feature)
        
        output_path = 'data/teesta_districts.geojson'
        with open(output_path, 'w') as f:
            json.dump(geojson, f, indent=2)
            
        print(f"Success! Saved to {output_path}")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    fetch_teesta_districts()
