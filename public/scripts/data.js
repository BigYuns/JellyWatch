Data = {
	user: null,
	token: null,
	logIn: function(email, password, callback) {
		/* 
		email and password are strings
		callback is called with a dictionary: {success: true/false, message: <an error message, if present>}
		
		Once you're done logging in, individualName may be set, or it might be null.
		if it's null, they've logged in with an organizational account,
		so we need to ask them THEIR name. set Data.individualName = <that name> before submitting any jellyfish sightings.
		*/
		Data.post('/users/login', {email: email, password: password}, function(resp) {
			if (resp) {
				if (resp.success) {
					Data.token = resp.token;
					Data.user = resp.user;
					localStorage.token = Data.token;
					localStorage.user = JSON.stringify(Data.user);
				}
				callback(resp);
			} else {
				callback({success: false});
			}
		})
	},
	logOut: function() {
		Data.user = null;
		Data.token = null;
		localStorage.user = null;
		localStorage.token = null;
	},
	getJellyfishForMap: function(latitude, longitude, callback) {
		/* callback is called w/ an array of jellyfish sightings nearby.
		each sighting looks like this:
		{
			latitude: 45.485904,
			longitude: -30.294834
		}
		*/
		console.log(latitude, longitude); 
		setTimeout(function() {
			callback([
				{latitude: 41.799005, longitude: -71.383581},
				{latitude: 41.775966, longitude: -71.367702},
				{latitude: 41.475001, longitude: -71.299896},
				{latitude: 41.606129, longitude: -71.304703}
			])
		}, 300);
	},
	submitJellyfishSighting: function(data, callback) {
		/*
		callback(success) is called with true/false
		data looks like this:
		{
			
		}
		*/
		setTimeout(function() {
			callback(true);
		}, 300);
	},
	// ADMIN FUNCTIONS:
	createOrUpdateAccount: function(email, password, isAdmin, isOrganizationalAccount, callback) {
		// callback returns true or false, for success or not
		// if the username already exists, we'll update it
		// only admins can call this
		var bool = function(b) { return b ? 'true' : 'false' }
		Data.post('/users/update', {email: email, password: password, is_admin: bool(isAdmin), is_organization: bool(isOrganizationalAccount)}, callback);
	},
	deleteAccount: function(email, callback) {
		// must be an admin
		// callback(success) is called w/ true or false
		Data.post('/users/delete', {email: email}, callback)
	},
	listUsers: function(callback) {
		/*
		callback(users) is called with a dictionary that looks like this:
		{
			"users": [ {"email": "abc@gmail.com", "is_admin": true, "is_organization": false} ],
			"message": <error message, or nothing>
		}
		must be an admin to call this
		*/
		Data.get('/users', {}, callback);
	},
	get: function(url, params, callback) {
		var http = new XMLHttpRequest();
		var reqURL = Data._url + url + "?" + Data._serialize(params);
		http.open("GET", reqURL, true);
		http.onreadystatechange = function() {
		    if(http.readyState == 4) {
				if (http.status == 200) {
			        callback(JSON.parse(http.responseText));
				} else {
					callback(null);
				}
		    }
		}
		http.send(null);
	},
	post: function(url, params, callback) {
		var http = new XMLHttpRequest();
		var reqURL = Data._url + url;
		http.open("POST", reqURL, true);
		http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		http.onreadystatechange = function() {
		    if(http.readyState == 4) {
				if (http.status == 200) {
			        callback(JSON.parse(http.responseText));
				} else {
					callback(null);
				}
		    }
		}
		http.send(Data._serialize(params));
	},
	_serialize: function(obj) {
	  var str = [];
	  if (this.token) obj.token = this.token;
	  for(var p in obj)
	     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	  return str.join("&");
	},
	_url: "https://ri-jellywatch.appspot.com",
	// _url: 'http://localhost:19080',
	_setup: function() {
		if (localStorage.user && localStorage.token) {
			Data.token = localStorage.token;
			Data.user = JSON.parse(localStorage.user)
		}
	}
}
Data._setup();

function initialize(sites) {
	console.log("sites + "+ sites); 
	//console.log("initialize: lat "+ sites[0].latitude); 
	//console.log("initialize: lng "+ sites[0].longitude); 
	console.log(lat); 
	console.log(lng); 
  var myCenter= new google.maps.LatLng(lat,lng); 
  var mapProp = {
    center:myCenter,
    zoom:5,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"), mapProp);
  var marker=new google.maps.Marker({
    position:myCenter,
    animation:google.maps.Animation.BOUNCE
    });

  marker.setMap(map);

}
google.maps.event.addDomListener(window, 'load', initialize);

var latitude = 41.8167681; 
var longitude = -71.3474485; 
Data.getJellyfishForMap(latitude,longitude,initialize); 

