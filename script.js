// Landmark data: Coordinates and descriptions
const landmarks = [
    {
        name: "Place de la Bourse",
        desc: "Home to the world's largest reflecting pool, the Miroir d'Eau.",
        coords: [44.8412, -0.5699],
        zoom: 17
    },
    {
        name: "La Grosse Cloche",
        desc: "A stunning 15th-century belfry and one of the oldest belfries in France.",
        coords: [44.8357, -0.5714],
        zoom: 17
    },
    {
        name: "Cathédrale Saint-André",
        desc: "Bordeaux's primary cathedral, where Eleanor of Aquitaine was married.",
        coords: [44.8376, -0.5772],
        zoom: 17
    },
    {
        name: "Monument aux Girondins",
        desc: "A grand fountain and column honoring the Girondist revolutionaries.",
        coords: [44.8443, -0.5744],
        zoom: 17
    },
    {
        name: "Pont de Pierre",
        desc: "The first bridge built over the Garonne river, commissioned by Napoleon.",
        coords: [44.8378, -0.5645],
        zoom: 16
    },
    {
        name: "Cité du Vin",
        desc: "A unique cultural center dedicated to the universal heritage of wine.",
        coords: [44.8624, -0.5501],
        zoom: 17
    },
    {
        name: "Grand Théâtre",
        desc: "Considered one of the most beautiful 18th-century theaters in the world.",
        coords: [44.8428, -0.5742],
        zoom: 17
    }
];

// Initialize the map
const map = L.map('map', {
    zoomControl: false // We'll move or hide it for a cleaner UI
}).setView([44.8378, -0.5792], 14);

// Add custom zoom control position
L.control.zoom({
    position: 'topright'
}).addTo(map);

// Load CartoDB Positron (Light & Minimal)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 20
}).addTo(map);

// Landmarks list element
const landmarksList = document.getElementById('landmarks-list');

// Function to handle card clicks
function focusLandmark(coords, zoom, marker) {
    map.flyTo(coords, zoom, {
        duration: 1.5,
        easeLinearity: 0.25
    });
    marker.openPopup();
}

// Generate markers and cards
landmarks.forEach(landmark => {
    // 1. Create Marker
    const marker = L.marker(landmark.coords).addTo(map);
    marker.bindPopup(`
        <div class="popup-content">
            <h3>${landmark.name}</h3>
            <p>${landmark.desc}</p>
        </div>
    `);

    // 2. Create UI Card
    const card = document.createElement('div');
    card.className = 'landmark-card';
    card.innerHTML = `
        <h3>${landmark.name}</h3>
        <p>${landmark.desc}</p>
    `;

    // 3. Add Click Event
    card.addEventListener('click', () => {
        focusLandmark(landmark.coords, landmark.zoom, marker);
    });

    // 4. Append to list
    landmarksList.appendChild(card);
});

// Add a slight delay for better visual flow
window.addEventListener('load', () => {
    document.querySelector('.main-header').style.opacity = '1';
    document.querySelector('.landmarks-list-container').style.opacity = '1';
});
