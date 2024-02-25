from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import base64
import os
import requests
from plant_doctor import PlantDoctor

app = FastAPI()

# lang_dict = {
#     'en':'English',
#     'hi':'Hindi',
#     'ma':'Marathi',
#     'gu':'Gujarati',
#     'ta':'Tamil',
#     'te':'Telugu',
# }

class InputData(BaseModel):
    image: str
    latitude: str
    longitude: str
    lang: str = "en"

@app.get("/")
async def print_input(input: str):
    print(f"Input received: {input}")
    return {"message": "Input received successfully"}

@app.post("/process_image/")
async def process_image(data: InputData):

    latitude = data.latitude
    longitude = data.longitude
    lang = data.lang
    #lang_dict.get(data.lang, 'Hindi')
    
    image_data = data.image.replace('data:image/jpeg;base64,','')
    #print(f"Image data: {image_data}")
    
    doctor = PlantDoctor(latitude, longitude, image_data, lang = lang)
    report = doctor.get_consultation()
    print(report)
    return {"report": report}
