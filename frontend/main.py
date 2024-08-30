import requests
import streamlit as st
from PIL import Image

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

# st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Style transfer web app")

# displays a file uploader widget
image = st.file_uploader("Choose an image")

# displays the select widget for the styles
style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

# displays a button
if st.button("Style Transfer"):
    if image is not None and style is not None:
        files = {"file": image.getvalue()}
        try:
            res = requests.post(f"http://backend:8080/{style}", files=files, timeout=10)
            res.raise_for_status()  # Check if the request was successful

            # Check if the response is JSON
            if res.headers.get("Content-Type") == "application/json":
                img_path = res.json()
                # Ensure the JSON contains the expected key
                if "name" in img_path:
                    image = Image.open(img_path["name"])
                    st.image(image, width=500)
                else:
                    st.error("The response did not contain the expected 'name' key.")
            else:
                st.error(f"Unexpected content type: {res.headers.get('Content-Type')}")
                st.write("Response content:", res.text)

        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            st.error(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            st.error(f"An error occurred: {req_err}")
        except ValueError as json_err:
            st.error(f"Failed to parse JSON response: {json_err}")
            st.write("Response content:", res.text)
    else:
        st.error("Please upload an image and select a style.")
