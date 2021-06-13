// Creating map object
var myMap = L.map("map", {
  center: [40.7, -73.95],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// TODO:

// Store API query variables
var baseURL = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?";
// Add the dates in the ISO formats
var date = "$where=created_date between '' and ''";
// Add the complaint type
var complaint = "&complaint_type=";
// Add a limit
var limit = "&$limit=";



// Assemble API query URL
 
var full_url = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?complaint_type=%27Illegal%20Parking%27#34"
console.log(full_url)

// Grab the data with d3
d3.json(url, function(response) {

  console.log(response);

  var heatArray = [];

  for (var i = 0; i < response.length; i++) {
    var location = response[i].borough;

    if (location) {
      heatArray.push([location[1], location.coordinates[0]]);
    }
  }
  // Create a new marker cluster group

  // Loop through data

    // Set the data location property to a variable

    // Check for location property

      // Add a new marker to the cluster group and bind a pop-up

  // Add our marker cluster layer to the map
  var markers = L.markerClusterGroup();
  markers.addLayer(L.marker(getRandomLatLng(map)));
  ... Add more layers ...
  map.addLayer(markers);