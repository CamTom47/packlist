import requests
from secret import TOMORROW_API_KEY

def get_weather_information(lat, lng):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={lat},{lng}&timesteps=1d&apikey={TOMORROW_API_KEY}"

    resp = requests.get(url)
    json_resp = resp.json()
        
    daily_weather = json_resp["timelines"]["daily"]
    
    return daily_weather

def get_weather_highs_lows(lat, lng):
    daily_weather = get_weather_information(lat, lng)
    weather_info = {'temp_high': None,
                    'temp_low': None,
                    'chance_of_rain': None};
    
    for day in daily_weather:
        
        #comparing temp highs
        if not weather_info["temp_high"]:
            weather_info["temp_high"] = day["values"]["temperatureMax"]
            
        else:
            if weather_info["temp_high"] <= day["values"]["temperatureMax"]:
                weather_info["temp_high"] = day["values"]["temperatureMax"]

        
        #comparing temp lows
        if not weather_info["temp_low"]:
            weather_info["temp_low"] = day["values"]["temperatureMin"]
            
        else:
            if weather_info["temp_low"] >= day["values"]["temperatureMin"]:
                weather_info["temp_low"] = day["values"]["temperatureMin"]
        
        #comparing chance of precipitation
        if not weather_info["chance_of_rain"]:
            weather_info["chance_of_rain"] = day["values"]["precipitationProbabilityAvg"]
            
        else:
            if weather_info["chance_of_rain"] <= day["values"]["precipitationProbabilityAvg"]:
                weather_info["chance_of_rain"] = day["values"]["precipitationProbabilityAvg"]
        
    return weather_info




# sunriseTime
# sunsetTime
# date to time
