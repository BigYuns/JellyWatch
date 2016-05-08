//getJellyfishForMap: function(lat_min, lat_max, lon_min, lon_max, callback)
//game plan: 
//i am going to create a map; get four corrner coordinates of the function 
// passs in the function 
//checking compatability by testing for the presence of the geolocation object:
var index_check = new Set();

MapPos = null;

function copyBounds(b) {
	return new google.maps.LatLngBounds(b.getSouthWest(), b.getNorthEast());
}

function expandBounds(bounds, scale) {
	var span = bounds.toSpan();
	var center = bounds.getCenter();
	var firstPointToAdd = new google.maps.LatLng({lat: center.lat() + span.lat() * scale / 2, lng: center.lng() + span.lng() * scale / 2});
	var secondPointToAdd = new google.maps.LatLng({lat: center.lat() - span.lat() * scale / 2, lng: center.lng() - span.lng() * scale / 2});
	return copyBounds(bounds).extend(firstPointToAdd).extend(secondPointToAdd);
}

function boundsContainsBounds(big, little) {
	return big.equals(copyBounds(big).union(little));
}

function initMap() {
    var mapOptions = {
      zoom: 13,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
	  center: {lat: 41.82696354880109, lng: -71.4032554100936}
    };//maptOptions
	var map = new google.maps.Map(document.getElementById('googleMap'), mapOptions); 
	
	var lastBoundsFetched = null;
	
    google.maps.event.addListener(map, 'bounds_changed', function(){
  	  	MapPos = {lat: map.getCenter().lat(), lng: map.getCenter().lng()};
		
		var needsReload = (!lastBoundsFetched || !boundsContainsBounds(lastBoundsFetched, map.getBounds()))
		if (needsReload) {
			
			var bounds = expandBounds(map.getBounds(), 1.5);
			lastBoundsFetched = bounds;
	        var lat_min = bounds.getSouthWest().lat(); 
	        var lat_max = bounds.getNorthEast().lat(); 
	        var lon_min = bounds.getSouthWest().lng(); 
	        var lon_max = bounds.getNorthEast().lng();
     
	        Data.getJellyfishForMap(lat_min, lat_max, lon_min, lon_max, function(data){
	          //problem: whenever a user moves the map around, the maker is newly created. 
	          //if the data is the same, don't great a marker/ once you get the data, set the data zero. 
	          for (var i=0; i<data.length; i++){            
	            var icon = {
	              url: "http://i.giphy.com/SmYfl1HKMJjri.gif",
	              size: new google.maps.Size(20, 20),
	              origin: new google.maps.Point(0, 0),
	              anchor: new google.maps.Point(0, 32)
	            }; //icon
	            if(!index_check.has(i)){
	              var jellyMarker = new google.maps.Marker({
	                map: map,
	                draggable:false,
	                optimized: false, 
	  			  position: {lat: data[i].geometry.x, lng: data[i].geometry.y},
	  				icon: iconForJellyfish(data[i])
	                //icon: icon
	              });//jellyMarker
	  			(function(sighting, jellyMarker) {
	  				jellyMarker.addListener('click', function() {
	  					var content = $("<dl></dl>");
	  					Object.keys(sighting.jellyfish).forEach(function(jellyType) {
	  						content.append($("<dt></dt>").text(jellyType));
	  						content.append($("<dd></dd>").text(sighting.jellyfish[jellyType]));
	  					});
					
	  					content.append($("<dt></dt>").text("Date"));
	  					content.append($("<dd></dd>").text(sighting.date));
					
	  					content.append($("<dt></dt>").text("Created by"));
	  					content.append($("<dd></dd>").text(sighting.user));
	  					content.find("dt").css('font-weight', 'bold');
					
	  					var w = new google.maps.InfoWindow({
	  						content: $(content).html()
	  					})
	  				    w.open(map, jellyMarker);
	  				})
	  			})(data[i], jellyMarker);
	              jellyMarker.setMap(map); 
	              index_check.add(i); 
	            }//if
	          }//for loop
	        }); //callback function
		} // if needsReload
    });  //addListener
	
  // GEOLOCATION:
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position){
      var pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };//pos
	  MapPos = pos;
      map.setCenter(pos);
    }, function(){ //getcurrentPosition first paremet done
      handleLocationError(true, map.getCenter());
    }); //second argumentof get curentposition
  }else {
    // Browser doesn't support Geolocation
    handleLocationError(false, map.getCenter());
  }//else
}//initMap 

function handleLocationError(browserHasGeolocation, pos) {
  alert(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}
