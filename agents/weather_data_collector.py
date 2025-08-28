import requests

def get_live_weather(location, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    r = requests.get(url).json()
    weather = {
        "temp": r.get("main", {}).get("temp", ""),
        "status": r.get("weather", [{}])[0].get("main", ""),
        "desc": r.get("weather", [{}])[0].get("description", ""),
    }
    return weather
