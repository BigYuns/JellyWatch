import urllib2
import json
API_KEY = 'b81798e1095198040b90ecb3438a52d7'
url = 'api.openweathermap.org/data/2.5/weather?lat=35&lon=139'

def add_weather_to_sighting(sighting):
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units=metric&appid={2}'.format(sighting.lat, sighting.lng, API_KEY)
    data = json.load(urllib2.urlopen(url))
    sighting.location_name = data['name']
    condition_id = data['weather'][0]['id']
    sighting.weather = weather_from_id(condition_id)
    sighting.wind_speed = data['wind']['speed'] # meters/sec
    sighting.temperature = data['main']['temp']

def weather_from_id(id):
    # take ids from: http://openweathermap.org/weather-conditions
    # turn into one of: ['sunny', 'cloudy', 'overcast', 'rainy', 'snowy', 'other']
    if id >= 200 and id <= 299:
        # thunderstorm
        return 'rainy'
    if id >= 300 and id <= 399:
        # drizzle
        return 'rainy'
    if id >= 500 and id <= 599:
        # rainy
        return 'rainy'
    if id >= 600 and id <= 699:
        # snow
        return 'snowy'
    if id >= 700 and id <= 799:
        # 'atmosphere'
        return 'other'
    if id == 800:
        # clear
        return 'sunny'
    if id >= 801 and id <= 803:
        return 'cloudy'
    if id == 804:
        return 'overcast'
    if id in (901, 902):
        # hurricane/tropical storm
        return 'rainy'
    if id == 906:
        # hail
        return 'snowy'
    if id >= 951 and id <= 962:
        # various wind things
        return 'sunny'
    return 'other'
    