import logging
import requests
import time
import streamlit as st
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)

# Dictionary of available styles and their corresponding model names
STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}

# https://discuss.streamlit.io/t/version-0-64-0-deprecation-warning-for-st-file-uploader-decoding/4465
# st.set_option("deprecation.showfileUploaderEncoding", False)

# Set up the web app title
st.title("Style transfer web app")

# File uploader widget to allow users to upload an image
image = st.file_uploader("Choose an image")

# Dropdown widget to allow users to select a style for the image
style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

# Button to trigger the style transfer process
if st.button("Style Transfer"):
    if image is not None and style is not None:
        logging.info("User selected style: %s", style)
        files = {"file": image.getvalue()}
        try:
            logging.info("Sending POST request to backend...")
            res = requests.post(f"http://backend:8080/{style}", files=files, timeout=100)
            res.raise_for_status()  # Check if the request was successful
            logging.info("Received response from backend")
            img_path = res.json()
            image = Image.open(img_path.get("name"))
            st.image(image, width=500)

            displayed_styles = [style]
            displayed = 1
            total = len(STYLES)

            st.write("Generating other models...")

            while displayed < total:
                for style in STYLES:
                    if style not in displayed_styles:
                        try:
                            path = f"{img_path.get('name').split('.')[0]}_{STYLES[style]}.jpg"
                            image = Image.open(path)
                            st.image(image, width=500)
                            time.sleep(1)
                            displayed += 1
                            displayed_styles.append(style)
                        except:
                            pass
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
            logging.error("HTTP error occurred: %s", http_err)
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"Connection error occurred: {conn_err}")
            logging.error("Connection error occurred: %s", conn_err)
        except requests.exceptions.Timeout as timeout_err:
            st.error(f"Timeout error occurred: {timeout_err}")
            logging.error("Timeout error occurred: %s", timeout_err)
        except requests.exceptions.RequestException as req_err:
            st.error(f"An error occurred: {req_err}")
            logging.error("An error occurred: %s", req_err)
        except ValueError as json_err:
            st.error(f"Failed to parse JSON response: {json_err}")
            logging.error("Failed to parse JSON response: %s", json_err)
            st.write("Response content:", res.text)
    else:
        st.error("Please upload an image and select a style.")
        logging.warning("Image or style not selected by the user")
