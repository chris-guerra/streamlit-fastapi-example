# style-shift-ml

## Overview

This project is a web-based application that allows users to apply artistic style transfer to their images using pre-trained neural network models. The application consists of a frontend built with Streamlit and a backend powered by FastAPI. Users can upload an image, select an artistic style, and receive a stylized version of their image.

## Features

- **Upload Image:** Users can upload an image file from their local device.
- **Select Style:** Choose from a variety of pre-trained artistic styles.
- **Style Transfer:** The selected style is applied to the uploaded image using a deep learning model, and the resulting image is displayed to the user.

## Available Styles

The application currently supports the following styles:

- Candy
- Composition VI
- Feathers
- La Muse
- Mosaic
- Starry Night
- The Scream
- The Wave
- Udnie

## Project Structure

The project is organized into two main components:

### Frontend

- **Framework:** Streamlit
- **Directory:** `frontend/`
- **Entry Point:** `frontend/main.py`
- **Dockerfile:** `frontend/Dockerfile`

### Backend

- **Framework:** FastAPI
- **Directory:** `backend/`
- **Entry Point:** `backend/main.py`
- **Model Inference:** `backend/inference.py`
- **Configuration:** `backend/config.py`
- **Dockerfile:** `backend/Dockerfile`

### Shared Resources

- **Models:** Pre-trained models for style transfer are stored in the `backend/models/` directory.
- **Storage:** The `storage/` directory is shared between the frontend and backend for saving and accessing processed images.

## How to Run

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Step-by-Step Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/chris-guerra/style-shift-ml.git
   cd style-shift-ml
   ```
2. **Download models:**
```bash
sh download_models.sh
```
2. **Build and start the application:**
   ```bash
    docker compose up --build -d
   ```
3. Access the application:

Frontend: Open your browser and go to http://localhost:8501 to interact with the web app.
Backend: The API is accessible at http://localhost:8080.

### Stopping the application
```bash
docker compose down
```

### Credits:

https://www.youtube.com/watch?v=cCsnmxXxWaM