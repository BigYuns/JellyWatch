FAKE_ACCOUNTS = [
	{username: "lynn", "password": "123", isAdmin: true, organization: false},
	{username: "savethebay", "password": "savethebae", isAdmin: false, organization: true},
	{username: "n8", "password": "wow", isAdmin: false, organization: false}
]

Data = {
	loggedIn: false,
	individualName: null,
	isAdmin: false,
	logIn: function(username, password, callback) {
		/* 
		username and password are strings
		callback is a function(correct_username, correct_password),
		where correct_username and correct_password are true/false.
		If both are true, login succeeded.
		
		Once you're done logging in, individualName may be set, or it might be null.
		if it's null, they've logged in with an organizational account,
		so we need to ask them THEIR name. set Data.individualName = <that name> before submitting any jellyfish sightings.
		*/
		setTimeout(function() {
			for (var i=0; i<FAKE_ACCOUNTS.length; i++) {
				var acct = FAKE_ACCOUNTS[i];
				var correctName = (acct.username == username);
				var correctPwd = (acct.password == password);
				if (correctName) {
					if (correctPwd) {
						Data.loggedIn = true;
						Data.individualName = acct.organization ? null : username;
						Data.isAdmin = acct.isAdmin;
						callback(true, true);
					} else {
						callback(true, false)
					}
					return
				}
			}
			callback(false, false);
		}, 300);
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
	}
}
