/* Handles Google Map Component */

var mapOptions = {
	//center: {lat: 30.310912, lng: -96.301664},
	center: {lat: 0.0, lng: 0.0},
	zoom: 2
};

var map = new google.maps.Map(document.getElementById('map-canvas'), 
							  mapOptions); 

//google.maps.event.addDomListener(window, 'load', initialize);
