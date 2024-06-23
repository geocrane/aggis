// Centre the map on the Isle of Wight
var map = L.map('map', {
    center: [55.796127, 49.106414],
    minZoom: 12,
    maxZoom: 14,
    zoom: 12
});

// Add the downloaded tiles
L.tileLayer('../static/tiles/{z}_{x}_{y}.png', {}).addTo(map);
