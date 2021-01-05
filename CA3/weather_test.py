import json
import config
from weatherapi import extract_weather

# pylint: disable= unsubscriptable-object
with open('config.json', 'r') as f:
    json_file = json.load(f)
    weather_api_key= json_file["weather_api_key"]
    city = json_file['city_name']

weather_json = {
    
    'weather':[{
        'id':500,
        'main':'Rain',
        'description':'light rain',
        'icon':'10n'
    }],
    'base':'stations',
    'main':{
        'temp':293.54,
        'feels_like':284.96,
        'pressure':1016,
        'humidity':93
    },
    'visibility':10000,
    'wind':{
        'speed':3,
        'deg':121
    },
    'rain':{
        '1h':0.81
    },
    'clouds':{
        'all':18
    },
    'dt':1604877233,
    'sys':{
        'type':3,
        'id':2005600,
        'country':'GB',
        'sunrise':1604819889,
        'sunset':1604853461
    },
    'timezone':0,
    'id':2649808,
    'name':'Exeter',
    'cod':200
}

def weather_test_one():
    weather = int(extract_weather(weather_json,city))
    assert weather['temperature'] == 20

def weather_test_two():
    weather = int(extract_weather(weather_json,city))
    assert weather['description'] == 'light rain'
    
def weather_test_three():
    weather = int(extract_weather(weather_json,city))
    assert weather['humidity'] == 93