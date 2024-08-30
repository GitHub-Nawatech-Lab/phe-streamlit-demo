import requests
import streamlit as st
from PIL import Image
import io
import base64

def get_api_seismic(slice_type):
    try:
        print("Run get_api_seismic()")
        # Get the API with the selected slice_type
        response = requests.get(f"http://20.6.74.118:8000/prediction-result/?slice_type={slice_type}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Error: ", response.status_code)
            return None
    except Exception as e:
        print("get_api_seismic() function get error:", e)
        return None

def visualize_seismic(data, slice_type):
    try:
        # Decode the image from the base64 data
        image = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image))
        
        # Display the image in Streamlit
        st.image(image, caption=f"Prediction Result - {slice_type.upper()}")
    except Exception as e:
        print("visualize_seismic() function get error:", e)

def st_seismic():
    try:
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.title("Seismic Visualization")
        st.markdown("### ✅ Seismic Visualization Nawatech - PHE")

        # Sidebar controls to select slice type
        slice_type = st.selectbox(
            "Pilih Slice Type:",
            ("tline", "iline", "xline")
        )

        # Run prediction when the button is clicked
        if st.button("Run Prediction"):
            response = get_api_seismic(slice_type)
            if response is not None:
                visualize_seismic(response, slice_type)
                print("Seismic Visualization Done!")
            else:
                st.error("Failed to get prediction data.")
    except Exception as e:
        print("st_seismic() function get error:", e)
