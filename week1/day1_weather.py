import requests

# Change these to your city's coordinates
latitude = -1.29
longitude = 36.82

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "temperature_2m,wind_speed_10m,relative_humidity_2m",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    current = data["current"]
    units = data["current_units"]

    print("=== Current Weather ===")
    print(f"Temperature: {current['temperature_2m']} {units['temperature_2m']}")
    print(f"Wind speed:  {current['wind_speed_10m']} {units['wind_speed_10m']}")
    print(f"Humidity:    {current['relative_humidity_2m']}{units['relative_humidity_2m']}")
else:
    print("Request failed. Status:", response.status_code)