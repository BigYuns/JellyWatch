#!/usr/bin/env python
# -*- coding: utf-8 -*-


from google.appengine.ext import ndb
from collections import defaultdict
from csv import DictWriter
import weather
import users
import photo

jellyfish_names = ['comb jelly', 'cucumber or basket comb jelly', 'moon jelly', u'lion’s mane', 'stinging sea nettle', 'crystal jelly', 'cross jelly', 'man of war', 'salps', 'freshwater jellyfish', 'other', 'i don’t know. see photos.']

class Sighting(ndb.Model):
    species_counts = ndb.JsonProperty() # dictionary of {"Jellyfish common name": "5-10"}, etc
    date_inserted = ndb.DateTimeProperty(auto_now_add=True)
    nearby_species = ndb.StringProperty(repeated=True) # array of nearby species choices=['horseshoe crabs']
    water_uses = ndb.StringProperty(repeated=True) # choices=['no one is using the water', 'sunbathing', 'swimming', 'fishing from shore', 'boating']
    
    weather = ndb.StringProperty() # choices=['sunny', 'cloudy', 'overcast', 'rainy', 'snowy', 'other']
    wind_speed = ndb.FloatProperty() # meters/sec
    temperature = ndb.FloatProperty() # celsius
    water_clarity = ndb.StringProperty() # choices=['clear', 'turbid']
    attached_seaweed = ndb.BooleanProperty()
    microalgae_blooms = ndb.StringProperty(repeated=True) # choices=['none observed', 'green sea lettuce (ulva)', 'red algae (grateloupia)', 'brown seaweed', 'other']
    location_name = ndb.StringProperty()
    
    user_email = ndb.StringProperty()
    user_name = ndb.StringProperty()
    
    comment_input = ndb.TextProperty()
    photo_urls = ndb.StringProperty(repeated=True)
    
    date = ndb.StringProperty()
    time_of_day = ndb.StringProperty()
    
    # location = ndb.GeoPtProperty()
    lat = ndb.FloatProperty()
    lng = ndb.FloatProperty()
    
    def to_json(self):
        return {
            "geometry": {"x": self.lat, "y": self.lng}
        }
    
    def import_json(self, json_obj):
        fields = ['nearby_species', 'water_uses', 'water_clarity', 'weather', 'attached_seaweed', 'microalgae_blooms', 'lat', 'lng', 'date', 'time_of_day', 'user_name', 'comment_input']
        for field in fields:
            val = json_obj.get(field)
            if isinstance(val, unicode) or isinstance(val, str): val = val.lower()
            setattr(self, field, json_obj.get(field))
        self.species_counts = {k.lower(): v.lower() for k, v in json_obj['species_counts'].iteritems()}
        if json_obj.get('photo_url'):
            self.photo_urls = [photo.store_photo(json_obj.get('photo_url'))]
    
    @classmethod
    def insert_json(cls, json_obj, token):
        sighting = Sighting()
        user = users.user_for_token(token)
        sighting.user_email = user.key.id()
        sighting.import_json(json_obj)
        weather.add_weather_to_sighting(sighting)
        sighting.put()
        return sighting

def get_jellyfish(lat_min=-1000, lat_max=1000, lon_min=-1000, lon_max=1000):
    matches = Sighting.query(ndb.AND(Sighting.lat >= lat_min, Sighting.lat <= lat_max)).fetch()
    matches = [m for m in matches if m.lng >= lon_min and m.lng <= lon_max]
    # Sighting.lng >= lon_min, Sighting.lng <= lon_max
    return [j.to_json() for j in matches]


def get_sightings(limit=None):
    repeating_string_fields = ['water_uses', 'nearby_species', 'microalgae_blooms']
    single_fields = ['user_email', 'user_name', 'lat', 'lng', 'weather', 'wind_speed', 'attached_seaweed', 'date', 'time_of_day', 'location_name', 'temperature', 'comment_input']
    
    jellyfish_names = set()
    repeating_field_values = defaultdict(set)
    max_photo_fields = 0
    
    for sighting in Sighting.query().fetch():
        for field in repeating_string_fields:
            s = repeating_field_values[field]
            for val in getattr(sighting, field):
                s.add(val)
        for name in sighting.species_counts.keys():
            jellyfish_names.add(name)
        max_photo_fields = max(max_photo_fields, len(sighting.photo_urls))
    
    columns = list(single_fields)
    columns += list(jellyfish_names)
    for field in repeating_string_fields:
        columns += [field + u'=' + val for val in list(repeating_field_values[field])]
    columns += ['photo_{0}'.format(i+1) for i in xrange(max_photo_fields)]
    
    colset = set(columns)
    sightings = []
    
    for sighting in Sighting.query().order(-Sighting.date_inserted).fetch(limit=limit):
        d = {field: unicode(getattr(sighting, field)) for field in single_fields}
        for field in repeating_string_fields:
            for val in repeating_field_values[field]:
                d[field + u"=" + val] = "true" if val in getattr(sighting, field) else ""
        for species, count in sighting.species_counts.iteritems():
            d[species] = count
        
        for i in xrange(max_photo_fields):
            d['photo_{0}'.format(i+1)] = 'https://ri-jellywatch.appspot.com' + sighting.photo_urls[i] if i < len(sighting.photo_urls) else None
        
        if d.get('user_name') == 'null': d['user_name'] = ""
        
        d = {k: v for k,v in d.iteritems() if k in colset}
        sightings.append(d)
    
    return columns, sightings

def write_csv(file):
    headings, sightings = get_sightings()
    writer = DictWriter(file, headings)
    writer.writeheader()
    for sighting in sightings:
        writer.writerow(sighting)

# headings, sightings = jellyfish.get_recent()
def get_recent():
    return get_sightings(limit=20)
