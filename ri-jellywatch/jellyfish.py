# scary code that talks to the professors' scary server
import urllib, urllib2, json

JELLYFISH_NAME_MAP = {
    7: "None",
    1: "Comb Jelly",
    2: "Moon Jelly",
    3: "Lion's Mane",
    4: "Singing Sea Nettle",
    5: "Portuguese Man-o-War",
    8: "Crystal Jellyfish",
    9: "Sea Squirt",
    6: "Other"
}

# http://quidditch.gis.brown.edu/arcgis_brown/rest/services/Jellyfish/Jellyfish_Sightings/FeatureServer/0/query?where=&objectIds=&time=&geometry=%7B%0D%0A%22xmin%22+%3A+-71.71953840599997%2C+%22ymin%22+%3A+41.316380485000025%2C+%22xmax%22+%3A+-71.21517891999997%2C+%22ymax%22+%3A+41.82090434500003%2C%0D%0A%22spatialReference%22+%3A+%7B%22wkid%22+%3A+4326%7D%0D%0A%7D&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelEnvelopeIntersects&distance=&units=esriSRUnit_Foot&relationParam=&outFields=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&gdbVersion=&returnDistinctValues=false&returnIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&multipatchOption=&resultOffset=&resultRecordCount=&f=pjson

"""
XMin: -71.71953840599997
YMin: 41.316380485000025
XMax: -71.21517891999997
YMax: 41.82090434500003
"""

def process_feature(feature):
    feature['name'] = JELLYFISH_NAME_MAP[int(feature['attributes']['CommonName'])]
    return feature

def get_jellyfish(lat_min=-71.71953840599997, lat_max=-71.21517891999997, lon_min=41.316380485000025, lon_max=41.82090434500003):
    geometry = {"xmin": lat_min, "xmax": lat_max, "ymin": lon_min, "ymax": lon_max, "spatialReference": 4326}
    params = {
        "geometryType": "esriGeometryEnvelope",
        "geometry": geometry,
        "spatialRel": "esriSpatialRelEnvelopeIntersects",
        "f": "json"
    }
    url = "http://quidditch.gis.brown.edu/arcgis_brown/rest/services/Jellyfish/Jellyfish_Sightings/FeatureServer/0/query?" + urllib.urlencode(params)
    response = json.load(urllib2.urlopen(url))
    features = map(process_feature, response['features'])
    return features

if __name__ == '__main__':
    print get_jellyfish()
