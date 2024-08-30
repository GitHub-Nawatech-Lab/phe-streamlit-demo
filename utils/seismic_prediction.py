import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

st.title("Seismic Data Prediction")

if st.button("Run Prediction"):
    # url = "https://demo-phe-seismic.azurewebsites.net/predict/"
    url = "http://127.0.0.1:8000/predict/"
    headers = {"api-key" : "0PfSuTqMuPrKPrJLs9IblYvzslI4u9GsgcayLVSaD4reu79gq1DFv1rRuw7GXqF2i5rsWS25oGJcmS7tJjPk39qSDA2NEcesVmkktPMH0cj5Y9Pl22gb3IFXyrAlxcgn"}
    response = requests.get(url, headers=headers)
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

