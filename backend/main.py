"""
This module implements a FastAPI web service for applying style transfer to images.

The service allows users to upload an image and apply a selected style, such as 
'candy', 'mosaic', or 'starry_night', using pre-trained neural network models. 
The processed image is saved to a storage directory, and the file path is returned 
in the response.

Modules used:
    - FastAPI: The web framework used to handle API requests.
    - Uvicorn: ASGI server to serve the FastAPI application.
    - OpenCV (cv2): Used to save the processed image.
    - PIL (Pillow): Used for image handling.
    - Numpy: For image array manipulation.
    - uuid: To generate unique filenames for the processed images.

Endpoints:
    - GET /: Returns a welcome message.
    - POST /{style}: Applies the specified style to an uploaded image and returns 
      the file path of the processed image.

Usage:
    Run this module as the main module to start the FastAPI application.
"""
import uuid
import time
import asyncio
import logging
import cv2
import uvicorn
from fastapi import File, FastAPI, UploadFile
import numpy as np
from PIL import Image
from functools import partial
from concurrent.futures import ProcessPoolExecutor

import config
import inference

app = FastAPI()

logging.basicConfig(level=logging.INFO)

def process_image(models, image, name: str):
    for model in models:
        output, resized = inference.inference(models[model], image)
        name = name.split(".")[0]
        name = f"{name.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(name, output)

async def generate_remaining_models(models, image, name: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, name)
    )

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome from the API"}

@app.post("/{style}")
async def get_image(style: str, file: UploadFile = File(...)):
    """
    Endpoint to apply style transfer to an uploaded image.

    Args:
        style (str): The style to apply, corresponding to a key in config.STYLES.
        file (UploadFile): The uploaded image file.

    Returns:
        dict: The filename of the processed image or an error message.
    """
    if style not in config.STYLES:
        return {"error": f"Style '{style}' not recognized."}

    try:
        logging.info("Processing style: %s", style)
        image = np.array(Image.open(file.file))
        start = time.time()
        model = config.STYLES[style]
        output, resized = inference.inference(model, image)
        name = f"/storage/{str(uuid.uuid4())}.jpg"
        cv2.imwrite(name, output)
        models = config.STYLES.copy()
        del models[style]
        asyncio.create_task(generate_remaining_models(models, image, name))
        logging.info("Image saved as: %s", name)
        return {"name": name, "time": time.time() - start}
    except Exception as e:
        logging.error("Error processing image: %s", e)
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
