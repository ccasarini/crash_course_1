// Initialize the map, centered on Asia
var map = L.map('map').setView([34.0479, 100.6197], 4); // 4 is the zoom level

// Add background map (OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Load the GeoJSON file specifically for Asia
fetch('asia_floods.geojson')
    .then(response => response.json())
    .then(data => {
        // Add the GeoJSON data to the map
        L.geoJSON(data, {
            // Function to add a popup to each point
            onEachFeature: function (feature, layer) {
                var popupContent = "<b>Country: </b>" + feature.properties.country + "<br>" +
                                   "<b>Date: </b>" + feature.properties.date + "<br>" +
                                   "<b>Cause: </b>" + feature.properties.cause + "<br>" +
                                   "<b>Deaths: </b>" + feature.properties.dead;
                layer.bindPopup(popupContent);
            },
            // Style the markers (simple circles)
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 6,
                    fillColor: "#ff7800", // Orange
                    color: "#000",
                    weight: 1,
                    opacity: 1,
                    fillOpacity: 0.8
                });
            }
        }).addTo(map);
    })
    .catch(error => console.error('Error loading the GeoJSON file:', error));
