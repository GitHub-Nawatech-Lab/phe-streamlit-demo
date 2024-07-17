import streamlit as st
from utils.dicom import st_dicom
from utils.volve import st_volve
# from utils import seismic_prediction
import logging

logging.

def main() :
    try :
        st.set_page_config(
            page_title="Workshop Nawatech - PHE",
            page_icon="✅",
            layout="centered",
            initial_sidebar_state="expanded",
            menu_items={
                'About': "✅ Workshop Nawatech - PHE",
            }
        )
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)
        st.sidebar.title("Menu")
        selected_option = st.sidebar.selectbox("Select an Option", ["Seismic Holoviz", "DICOM", "Volve Production", "Field Prediction"])

        if selected_option == "Seismic Holoviz":
            st.write("Welcome to the Seismic page!")
            seismic_prediction()
        elif selected_option == "DICOM":
            st_dicom()
        elif selected_option == "Volve Production":
            st_volve()
        elif selected_option == "Field Prediction":
            st.write("Welcome to the Case-5 page!")
    except Exception as e :
        print("main() function get error :", e)

if __name__ == "__main__" :
    main()