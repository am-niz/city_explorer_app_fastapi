import datetime 
import requests


OPEN_WEATHER_MAP_URL = "http://api.openweathermap.org/data/2.5/weather"
API_KEY = 'b5809735937dbb4931ae0689ee5f7c61'
city_name="kochi"

def kelvin_to_celsius_and_fahrenheit(kelvin):
    cesius = kelvin - 273.15
    fahrenheit = cesius * (9/5) + 32
    return cesius, fahrenheit

def fetch_weather_data(city_name):   
    REQ_URL = f"{OPEN_WEATHER_MAP_URL}?q={city_name}&appid={API_KEY}"
    response = requests.get(REQ_URL).json()

    temp_kelvin = response['main']['temp']
    temp_ceslsius, temp_fahrenheit = kelvin_to_celsius_and_fahrenheit(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_and_fahrenheit(feels_like_kelvin)

    humidity = response['main']['humidity']
    
    description = response['weather'][0]['description']

    wind_speed = response['wind']['speed'] 

    sun_rise_time = datetime.datetime.utcfromtimestamp(response['sys']["sunrise"] + response['timezone'])           
    sun_set_time = datetime.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

    print(f"Temperature in {city_name}: {temp_ceslsius:.2f}'C {temp_fahrenheit:.2f}'F")
    print(f"Wind Speed: {wind_speed}Km/h")
    print(f"Looks Like: {description}")
    print(f"Temperature Feels Like: {feels_like_celsius:.2f}'C {feels_like_fahrenheit:.2f}'F")
    print(f"Humidity: {humidity}")
    print(f"Sun Rise At: {sun_rise_time}")
    print(f"Sun Set At: {sun_set_time}")

fetch_weather_data(city_name)
