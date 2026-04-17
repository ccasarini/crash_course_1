import json
from math import radians, cos, sin, asin, sqrt

# Function to calculate distance between two points on Earth in meters
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 # Radius of earth in meters
    return c * r

# 1. Load the datasets
with open('../data/bangladesh_floods.geojson', 'r') as f:
    floods = json.load(f)['features']

with open('../data/health_facilities.geojson', 'r') as f:
    health_sites = json.load(f)['features']

# 2. Identify sites at risk (within 1km of any flood)
at_risk_sites = []
for site in health_sites:
    site_lon, site_lat = site['geometry']['coordinates']
    is_at_risk = False
    
    for flood in floods:
        flood_lon, flood_lat = flood['geometry']['coordinates']
        distance = haversine(site_lon, site_lat, flood_lon, flood_lat)
        
        if distance <= 1000: # 1 km
            is_at_risk = True
            # Store the distance and flood info for the popup later
            site['properties']['risk_distance'] = round(distance)
            site['properties']['risk_cause'] = flood['properties'].get('cause', 'Unknown flood')
            break
            
    if is_at_risk:
        at_risk_sites.append(site)

# 3. Save the smaller dataset
output = {
    "type": "FeatureCollection",
    "features": at_risk_sites
}

with open('../data/at_risk_health_facilities.geojson', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Analysis complete! Found {len(at_risk_sites)} health sites within 1km of a flood event.")
