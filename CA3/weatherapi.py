import requests
import json
import config
from flask import Markup

with open('config.json', 'r') as f:
    json_file = json.load(f)
    weather_api_key= json_file["weather_api_key"]
    city = json_file['city_name']

def extract_weather(weather_api_key,city_name):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city_name
    # print response object
    x = requests.get(complete_url).json()
    if x["cod"] != "404":
        y = x['main']
        current_temperature = y["temp"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
    # print following values
    print(" Temperature (in Celcius ) = " +
    str(round(current_temperature - 273.15)) +
		"\n Humidity (in percentage) = " + str(current_humidity) +
		"\n Description = " + str(weather_description))
    
if __name__ == '__main__':
    (extract_weather(weather_api_key,city))

    