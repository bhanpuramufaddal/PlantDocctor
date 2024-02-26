import requests
import os

class WeatherForcaster:
    def __init__(self):

        self.url = "https://api.worldweatheronline.com/premium/v1/weather.ashx"
        self.params = {
            "num_of_days": 7,
            "format": "json",
            "key": os.environ.get("WEATHER_API_KEY"),
            "mca": "yes",
            "fx24": "yes",
            "aqi": "yes",
            "alerts": "yes",
        }

    def get_weather(self, latitude, longitude):
        self.params["q"] = f"{latitude},{longitude}"
        response = requests.get(self.url, params=self.params)
        return response.json()

    def generate_weather_summary(self, api_output):
        try:
            # Extracting current weather conditions
            current_conditions = api_output['data']['current_condition'][0]
            current_summary = (
                f"Current weather observation at {current_conditions['observation_time']}:\n"
                f"Temperature: {current_conditions['temp_C']}°C ({current_conditions['temp_F']}°F)\n"
                f"Condition: {current_conditions['weatherDesc'][0]['value']}\n"
                f"Wind: {current_conditions['windspeedKmph']} km/h from {current_conditions['winddir16Point']}\n"
                f"Humidity: {current_conditions['humidity']}%\n"
                f"Visibility: {current_conditions['visibility']} km\n"
                f"Pressure: {current_conditions['pressure']} mb\n"
                f"UV Index: {current_conditions.get('uvIndex', 'N/A')}\n"
            )

            # Extracting weather forecast for the next 24 hours
            today_forecast = api_output['data']['weather'][0]
            hourly_forecasts = today_forecast['hourly']
            next_24h_summary = "Weather forecast for the next 24 hours:\n"
            for forecast in hourly_forecasts:
                next_24h_summary += (
                    f"Time: {forecast['time']} - "
                    f"Temperature: {forecast['tempC']}°C ({forecast['tempF']}°F), "
                    f"Condition: {forecast['weatherDesc'][0]['value']}, "
                    f"Wind: {forecast['windspeedKmph']} km/h, "
                    f"Chance of rain: {forecast['chanceofrain']}%\n"
                )

            # Extracting weather forecast for the next 7 days
            weekly_forecast = api_output['data']['weather']
            next_7d_summary = "Weather forecast for the next 7 days:\n"
            for day in weekly_forecast:
                next_7d_summary += (
                    f"Date: {day['date']} - "
                    f"Max Temp: {day['maxtempC']}°C ({day['maxtempF']}°F), "
                    f"Min Temp: {day['mintempC']}°C ({day['mintempF']}°F), "
                    f"UV Index: {day['uvIndex']}\n"
                )

            # Combining all summaries
            full_summary = current_summary + "\n" + next_24h_summary + "\n" + next_7d_summary

            return full_summary
        except KeyError as e:
            return f"KeyError: The key {str(e)} is missing in the API output."

    def get_weather_summary(self, latitude, longitude):
        weather_data = self.get_weather(latitude, longitude)
        return self.generate_weather_summary(weather_data)
        