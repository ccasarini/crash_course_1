import json
from shapely.geometry import shape, Point

# 1. Load the Bangladesh border
with open('flood-map/bangladesh_border.geojson', 'r') as f:
    border_data = json.load(f)

# The border is a MultiPolygon (the first feature in the file)
border_shape = shape(border_data['features'][0]['geometry'])

# 2. Load the current flood data
with open('flood-map/bangladesh_floods.geojson', 'r') as f:
    flood_data = json.load(f)

# 3. Filter: Keep only points that are 'within' the border shape
filtered_features = []
removed_count = 0

for feature in flood_data['features']:
    point = Point(feature['geometry']['coordinates'])
    if border_shape.contains(point):
        filtered_features.append(feature)
    else:
        removed_count += 1

# 4. Save the new filtered data
new_flood_data = {
    "type": "FeatureCollection",
    "features": filtered_features
}

with open('flood-map/bangladesh_floods.geojson', 'w') as f:
    json.dump(new_flood_data, f, indent=2)

print(f"Success! Kept {len(filtered_features)} points and removed {removed_count} points outside the border.")
