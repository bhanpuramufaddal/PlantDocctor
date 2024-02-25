from PlaceName import generate_location_summary
from WeatherForcaster import WeatherForcaster
import requests
import os

REPORT_TEMPLATE = """**Plant Diagnosis Report**

**Crop:** [Name of the crop]

---

**1. Plant Identification:**
  - **Description:** 
     - **Plant Species:** [Species name]
     - **Variety (if known):** [Variety name]
     - **Age of Plant:** [Age or stage of growth]
     - General information about the plant sppecies and variety
---
** Are there any serious abnormalitiesw in theplant. 
    - Does the plant appears to be infected by any disease or pest?
    - Are there any visible signs of stress or damage?
    - What could be the cause of these abnormalities?
    - What can be done to improve the health of the plant?

**2 Discuss the general Health of the crop basaed on the following factors:**
    - Its appearance
    - Weather Conditions
    - Soil Conditions
    - Watering Conditions
    - Nutrient Conditions
    - Pest and Disease Conditions
    - Does the plant normal grow in this location and under these conditions?
    - Any other factors that may be relevant to the health of the plant.

**3. Recommendations:**
    - If the plant is unhealthy, what can be done to improve its health?
    - If the plant is healthy, what can be done to maintain its health?
"""

class PlantDoctor:

    def __init__(self, latitude, longitude, image):
        API_KEY = os.environ.get("API_KEY")

        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key={API_KEY}"

        self.headers = {
            "Content-Type": "application/json"
        }

        self.address_data = generate_location_summary(latitude, longitude)
        
        weatherAgent = WeatherForcaster()
        self.weather_data = weatherAgent.get_weather_summary(latitude, longitude)
        self.plant_image = image

    def get_consultation(self):

        prompt = """
        Lets say you are a expert botanistor and like a doctor for plants. A farmer has asked you to inspect his crops.
        You know the following details about a plant:

        1. **The location of the plant**
        {self.address_data}

        2. **The current and future weather conditions at this location**
        {self.weather_data}

        3. **An image of the plant attached**

        You need to diagnose this plant based on this information. and prepare a report for the farmer.
        The format of the report must be like this.
        ```
        {REPORT_TEMPLATE}
        ```
        """

        report = self.generateText(prompt, self.plant_image)
        return report

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





