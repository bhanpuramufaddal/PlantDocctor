from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import base64
import os
import requests
from plant_doctor import PlantDoctor

app = FastAPI()

class InputData(BaseModel):
    image: str
    latitude: str
    longitude: str

@app.get("/")
async def print_input(input: str):
    print(f"Input received: {input}")
    return {"message": "Input received successfully"}

@app.post("/process_image/")
async def process_image(data: InputData):

    latitude = data.latitude
    longitude = data.longitude
    
    image_data = data.image.replace('data:image/jpeg;base64,','')
    #print(f"Image data: {image_data}")
    
    doctor = PlantDoctor(latitude, longitude, image_data)
    report = doctor.get_consultation()
    print(report)
    return {"report": report}
