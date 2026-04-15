import pandas as pd
import json
from shapely.geometry import shape, Point

def excel_to_geojson(excel_file, geojson_file, border_file=None):
    df = pd.read_excel(excel_file)
    
    # Clean the data (remove rows without lat/long)
    df = df.dropna(subset=['lat', 'long'])
    
    # Strip spaces and filter for Bangladesh
    df['Country'] = df['Country'].astype(str).str.strip()
    df = df[df['Country'] == 'Bangladesh']
    
    # Load border if provided
    border_shape = None
    if border_file:
        with open(border_file) as f:
            border_data = json.load(f)
            border_shape = shape(border_data['features'][0]['geometry'])
    
    features = []
    for _, row in df.iterrows():
        lon, lat = float(row['long']), float(row['lat'])
        point = Point(lon, lat)
        
        is_inside = True
        if border_shape:
            is_inside = border_shape.contains(point)
            
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "id": str(row['ID']),
                "cause": str(row['MainCause']),
                "date_start": str(row['Began']).split(' ')[0],
                "date_end": str(row['Ended']).split(' ')[0],
                "dead": int(row['Dead']) if pd.notnull(row['Dead']) else 0,
                "displaced": int(row['Displaced']) if pd.notnull(row['Displaced']) else 0,
                "severity": float(row['Severity']) if pd.notnull(row['Severity']) else 1.0,
                "is_inside_border": is_inside
            }
        }
        features.append(feature)
        
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    with open(geojson_file, 'w') as f:
        json.dump(geojson, f, indent=2)

if __name__ == "__main__":
    excel_to_geojson('floodarchive.xlsx', 'bangladesh_floods.geojson', 'bangladesh_border.geojson')
