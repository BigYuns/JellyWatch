
var jellyfishColors = {
"comb jelly": "#50e3c2",
"cigar jelly": "#f8e71c",
"moon jelly": "#bd10e0",
"lion's mane": "#4a90e2",
"stinging sea nettle": "#d0021b",
"crystal jelly": "#f5a623",
"cross jelly": "#417505",
"man o' war": "#282249",
"salps": "#ff57ac",
"freshwater jellyfish": "#deff00",
"other (see photos)": "#cacaca"
}

function topJellyfishForSighting(sighting) {
	var top = 'other (see photos)';
	var topCount = 0;
	Object.keys(sighting.jellyfish).forEach(function(name) {
		var count = parseFloat(sighting.jellyfish[name].split(' '));
		if (count > topCount) {
			top = name;
		}
	});
	return top;
}

function iconForJellyfish(sighting) {
	var topJelly = topJellyfishForSighting(sighting);
	return {
        path: google.maps.SymbolPath.CIRCLE,
        strokeColor: "black",
		fillColor: jellyfishColors[topJelly] || '#cacaca',
		fillOpacity: 1,
        scale: 8,
		strokeWeight: 2
    }
}
