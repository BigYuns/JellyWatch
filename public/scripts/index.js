$(document).ready(function() {
	if (Data.isLoggedIn()) {
		document.getElementById('next_text').style.display = (Data.user && Data.user.is_admin) ? 'block' : 'none';
	} else {
		location.href = 'login.html'
	}

	function showMenu() {
		$("#menu").show();
	}

	function closeMenu() {
		$("#menu").hide();
	}

	function logOut() {
		Data.logOut()
		location.href = 'login.html';
	}

	function recordSighting() {
		location.href = 'form_page.html#' + MapPos.lat + ',' + MapPos.lng;
	}
	google.maps.event.addDomListener(window, 'load', initMap);
}); 


