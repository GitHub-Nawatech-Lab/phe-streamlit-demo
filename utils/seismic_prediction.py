import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

st.title("Seismic Data Prediction")

if st.button("Run Prediction"):
    response = requests.post("http://localhost:8000/predict")
    if response.status_code == 200:
        result = response.json()
        tline = np.array(result["tline"])
        iline = np.array(result["iline"])
        xline = np.array(result["xline"])

        fig, ax = plt.subplots(3, 1, figsize=(10, 30))
        ax[0].imshow(tline)
        ax[0].set_title("T-Line Prediction")
        ax[1].imshow(iline)
        ax[1].set_title("I-Line Prediction")
        ax[2].imshow(xline)
        ax[2].set_title("X-Line Prediction")
        st.pyplot(fig)
    else:
        st.error("Prediction failed")

st.write("Click the button to run the prediction on seismic data")

