from PlaceName import generate_location_summary
from WeatherForcaster import WeatherForcaster
import requests
import os

REPORT_TEMPLATE = """
**1. Crop Identification:**
    - Plant Species, sub-species and variety
    - Age of Plant
    - General information about the plant sppecies and variety
---
** Are there any serious abnormalitiesw in the crop or plant. 
    - Does the plant appears to be infected by any disease or pest?
    - What could be the cause of these abnormalities?
---
**2 Discuss the general Health of the crop basaed on the following factors:**
    - appearance
    - Soil Conditions
    - Watering and Nutrient Conditions
    - Pest and Disease Conditions
    - Any other factors
---
**3. Recommendations:**
    - If the plant is unhealthy, what can be done to improve its health?
    - If the plant is healthy, what can be done to maintain its health?
"""

class PlantDoctor:

    def __init__(self, latitude, longitude, image, lang = 'English'):
        API_KEY = os.environ.get("API_KEY")

        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={API_KEY}"
        self.translate_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

        self.headers = {
            "Content-Type": "application/json"
        }

        self.address_data = generate_location_summary(latitude, longitude)
        
        weatherAgent = WeatherForcaster()
        self.weather_data = weatherAgent.get_weather_summary(latitude, longitude)
        self.plant_image = image
        self.lang = lang

    def get_consultation(self):

        prompt = f"""
        Lets say you are a expert botanistor and like a doctor for plants. A farmer has asked you to inspect his crops.
        You know the following details about a plant:

        1. **The location of the plant**
        {self.address_data}

        2. **The current and future weather conditions at this location**
        {self.weather_data}

        3. **An image of the plant attached**

        You need to diagnose this plant based on this information. and prepare a report for the farmer.
        You can use the below template to prepare the report.
        ```
        {REPORT_TEMPLATE}
        ```
        ***If you do not have any information regarding any of the above topucs, you can skip it altogether.***
        """

        report = self.generateText(prompt, self.plant_image)
        if self.lang != 'en':
            report = self.translate(self.lang, report)

        return report

    def translate(self, language, text):

        prompt = f"""
        Translate the text below into {language} verbatim. The response must include only the translation.

        Text to translate:
        {text}

        ..................................
        Output:
        """
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
        }

        response = requests.post(self.translate_url , json=data, headers=self.headers)
        #print(response.json())
        return response.json()['candidates'][0]['content']['parts'][0]['text']


    def generateText(self, prompt, image):

        data = {
            "contents": {
                "role": "USER",
                "parts": [
                    {
                        "text": prompt
                    },
                    {
                        "inline_data": {
                            "data": image,
                            "mime_type": "image/jpeg"
                        }
                    }
                ]
            }
        }

        response = requests.post(self.gemini_url, json=data, headers=self.headers)
        return response.json()['candidates'][0]['content']['parts'][0]['text']





