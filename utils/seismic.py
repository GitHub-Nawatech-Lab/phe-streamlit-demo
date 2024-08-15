import requests
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def get_api_seismic() :
    try :
        print("Run get_api()")
        # Get the API
        response = requests.post("http://localhost:8000/predict")
        if response.status_code == 200 :
            return response.json()
        else :
            print("Error: ", response.status_code)
    except Exception as e :
        print("get_api() function get error :", e)

def visualize_seismic(data) :
    try :
        tline = np.array(data["tline"])
        iline = np.array(data["iline"])
        xline = np.array(data["xline"])

        fig, ax = plt.subplots(3, 1, figsize=(10, 30))
        ax[0].imshow(tline)
        ax[0].set_title("T-Line Prediction")
        ax[1].imshow(iline)
        ax[1].set_title("I-Line Prediction")
        ax[2].imshow(xline)
        ax[2].set_title("X-Line Prediction")
        st.pyplot(fig)
    except Exception as e :
        print("visualize_seismic() function get error :", e)

def st_seismic() :
    try :
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.title("Seismic Visualization")
        st.markdown("### ✅ Seismic Visualization Nawatech - PHE")
        # Sidebar controls
        if st.button("Run Prediction"):
            response = get_api_seismic()
            if response is not None :
                visualize_seismic(response)
                print("Seismic Visualization Done!")
    except Exception as e :
        print("st_seismic() function get error :", e)