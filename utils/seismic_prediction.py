import streamlit as st
import requests
from PIL import Image
import io
import base64


st.title("Seismic Data Prediction")

slice_type = st.selectbox(
    "Choose Slice Type:",
    ("tline", "iline", "xline")
)

if st.button("Run Prediction"):
    response = requests.get(f"http://20.6.74.118:8000/prediction-result/?slice_type={slice_type}")
    
    if response.status_code == 200:
        data = response.json()
        image = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image))
        st.image(image, caption=f"Prediction Result - {slice_type.upper()}")
    else:
        st.error("Prediction failed")

st.write("Click the button to run the prediction on seismic data")
