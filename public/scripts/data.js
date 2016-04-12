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
					localStorage.user = Data.user;
					callback(resp);
				}
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
	createOrUpdateAccount: function(username, password, isAdmin, isOrganizationalAccount, callback) {
		// callback returns true or false, for success or not
		// if the username already exists, we'll update it
		// only admins can call this
		setTimeout(function() {
			if (Data.isAdmin) {
				FAKE_ACCOUNTS.push({username: username, password: password, organization: isOrganizationalAccount, isAdmin: isAdmin});
				callback(true);
			} else {
				callback(false);
			}
		}, 300);
	},
	deleteAccount: function(username, callback) {
		// must be an admin
		// callback(success) is called w/ true or false
		setTimeout(function() {
			if (Data.isAdmin) {
				FAKE_ACCOUNTS = FAKE_ACCOUNTS.filter(function(a) { return a.username != username });
				callback(true);
			} else {
				callback(false);
			}
		}, 300);
	},
	listUsers: function(callback) {
		/*
		callback(users) is called with an array that looks like this:
		
		FAKE_ACCOUNTS = [
			{username: "lynn", isAdmin: true, organization: false},
			{username: "savethebay", isAdmin: false, organization: true},
			{username: "n8", isAdmin: false, organization: false}
		]
		
		if you aren't an admin, it's called back w/ false
		
		*/
		setTimeout(function() {
			if (Data.isAdmin) {
				callback(FAKE_ACCOUNTS);
			} else {
				callback(null);
			}
		}, 300);
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
	  for(var p in obj)
	     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
	  return str.join("&");
	},
	_url: "https://ri-jellywatch.appspot.com",
	_setup: function() {
		if (localStorage.user && localStorage.token) {
			Data.token = localStorage.token;
			Data.user = JSON.parse(localStorage.user)
		}
	}
}
Data._setup();
