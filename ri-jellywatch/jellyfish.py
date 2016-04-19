#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
the `sighting` dictionary looks like this:
{
    "lat": -74.048730,
    "lng": 100.2932,
    "species_counts": {"Comb Jelly": "5-10", "Moon jelly": "10-20"}, // other options are 'cucumber or basket comb jelly', 'lion’s mane', 'stinging sea nettle', 'crystal jelly', 'cross jelly', 'man of war', 'salps', 'freshwater jellyfish', 'other', 'i don’t know. see photos.' 
    "nearby_species": ["Horseshoe crabs"],
    "microalgae_blooms": ["Green Sea lettuce (Ulva)", "Red algae (Grateloupia)"], // (or ["None observed"])
    "water_clarity": "Turbid",
    "attached_seaweed": true,
    "water_uses": ["Sunbathing", "Fishing from shore"] // (or ["No one is using the water"]) 
}

make sure to use the exact text names from the doc
"""


from google.appengine.ext import ndb

jellyfish_names = ['comb jelly', 'cucumber or basket comb jelly', 'moon jelly', u'lion’s mane', 'stinging sea nettle', 'crystal jelly', 'cross jelly', 'man of war', 'salps', 'freshwater jellyfish', 'other', 'i don’t know. see photos.']

class Sighting(ndb.Model):
    species_counts = ndb.JsonProperty() # dictionary of {"Jellyfish common name": "5-10"}, etc
    date = ndb.DateTimeProperty(auto_now_add=True)
    nearby_species = ndb.StringProperty(repeated=True) # array of nearby species choices=['horseshoe crabs']
    water_uses = ndb.StringProperty(repeated=True) # choices=['no one is using the water', 'sunbathing', 'swimming', 'fishing from shore', 'boating']
    
    weather = ndb.StringProperty() # choices=['sunny', 'cloudy', 'overcast', 'rainy', 'snowy']
    windy = ndb.StringProperty() # choices=['low', 'medium', 'high']
    water_clarity = ndb.StringProperty() # choices=['clear', 'turbid']
    attached_seaweed = ndb.BooleanProperty()
    microalgae_blooms = ndb.StringProperty(repeated=True) # choices=['none observed', 'green sea lettuce (ulva)', 'red algae (grateloupia)', 'brown seaweed', 'other']
    
    photo_urls = ndb.StringProperty(repeated=True)
    
    # location = ndb.GeoPtProperty()
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()
    
    def to_json(self):
        return {
            "geometry": {"x": self.lat, "y": self.lng}
        }
    
    def import_json(self, json_obj):
        fields = ['species_counts', 'nearby_species', 'water_uses', 'water_clarity', 'attached_seaweed', 'microalgae_blooms', 'lat', 'lng']
        for field in fields:
            val = json_obj.get(field)
            if isinstance(val, unicode) or isinstance(val, str): val = val.lower()
            setattr(self, field, json_obj.get(field))
    
    @classmethod
    def insert_json(cls, json_obj):
        sighting = Sighting()
        sighting.import_json(json_obj)
        # TODO: fetch weather data
        sighting.put()
        return sighting

def get_jellyfish(lat_min=-1000, lat_max=1000, lon_min=-1000, lon_max=1000):
    matches = Sighting.query(ndb.AND(Sighting.lat >= lat_min, Sighting.lat <= lat_max)).fetch()
    matches = [m for m in matches if m.lng >= lon_min and m.lng <= lon_max]
    # Sighting.lng >= lon_min, Sighting.lng <= lon_max
    return [j.to_json() for j in matches]
