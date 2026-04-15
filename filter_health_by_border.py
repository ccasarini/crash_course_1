import json
from shapely.geometry import shape, Point

# 1. Load the Bangladesh border
with open('flood-map/bangladesh_border.geojson', 'r') as f:
    border_data = json.load(f)

border_shape = shape(border_data['features'][0]['geometry'])

# 2. Load the health facilities data
with open('bangladesh-map/health_facilities.geojson', 'r') as f:
    health_data = json.load(f)

# 3. Filter: Keep only points that are 'within' the border shape
filtered_features = []
removed_count = 0

for feature in health_data['features']:
    point = Point(feature['geometry']['coordinates'])
    if border_shape.contains(point):
        filtered_features.append(feature)
    else:
        removed_count += 1

# 4. Save the new filtered data
new_health_data = {
    "type": "FeatureCollection",
    "features": filtered_features
}

with open('bangladesh-map/health_facilities.geojson', 'w') as f:
    json.dump(new_health_data, f, indent=2)

print(f"Success! Kept {len(filtered_features)} health sites and removed {removed_count} points outside the border.")
