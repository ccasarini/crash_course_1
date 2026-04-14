import pandas as pd
import json

def excel_to_geojson(excel_file, geojson_file):
    df = pd.read_excel(excel_file)
    
    # Clean the data (remove rows without lat/long)
    df = df.dropna(subset=['lat', 'long'])
    
    features = []
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['long']), float(row['lat'])]
            },
            "properties": {
                "id": str(row['ID']),
                "glide_number": str(row['GlideNumber']),
                "country": str(row['Country']),
                "other_country": str(row['OtherCountry']),
                "area": str(row['Area']),
                "began": str(row['Began']),
                "ended": str(row['Ended']),
                "validation": str(row['Validation']),
                "dead": str(row['Dead']),
                "displaced": str(row['Displaced']),
                "main_cause": str(row['MainCause']),
                "severity": str(row['Severity'])
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
    excel_to_geojson('floodarchive.xlsx', 'flood_data.geojson')
