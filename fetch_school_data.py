import requests
import json
import time

SERVERS = ["https://overpass-api.de/api/interpreter", "https://lz4.overpass-api.de/api/interpreter"]
query = """[out:json][timeout:180];node["amenity"="school"](20.5,88.0,26.8,92.8);out body;"""

for url in SERVERS:
    try:
        r = requests.get(url, params={'data': query}, timeout=190)
        if r.status_code == 200:
            data = r.json()
            features = [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [e['lon'], e['lat']]}, "properties": e.get('tags', {})} for e in data.get('elements', [])]
            with open('bangladesh-map/schools.geojson', 'w') as f:
                json.dump({"type": "FeatureCollection", "features": features}, f)
            print(f"Fetched {len(features)} schools.")
            break
    except: continue

# 2. Filter by border and Run Risk Analysis
from shapely.geometry import shape, Point
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2
    return 2 * asin(sqrt(a)) * 6371000

with open('flood-map/bangladesh_border.geojson', 'r') as f: border_poly = shape(json.load(f)['features'][0]['geometry'])
with open('flood-map/bangladesh_floods.geojson', 'r') as f: floods = json.load(f)['features']
with open('bangladesh-map/schools.geojson', 'r') as f: schools = json.load(f)['features']

filtered_schools = []
at_risk_schools = []

for s in schools:
    p = Point(s['geometry']['coordinates'])
    if border_poly.contains(p):
        filtered_schools.append(s)
        # Check risk
        for f in floods:
            if haversine(s['geometry']['coordinates'][0], s['geometry']['coordinates'][1], f['geometry']['coordinates'][0], f['geometry']['coordinates'][1]) <= 1000:
                s['properties']['risk_dist'] = "within 1km"
                at_risk_schools.append(s)
                break

with open('bangladesh-map/schools.geojson', 'w') as f: json.dump({"type": "FeatureCollection", "features": filtered_schools}, f)
with open('bangladesh-map/at_risk_schools.geojson', 'w') as f: json.dump({"type": "FeatureCollection", "features": at_risk_schools}, f)
print(f"Done: {len(filtered_schools)} schools in BD, {len(at_risk_schools)} at risk.")
