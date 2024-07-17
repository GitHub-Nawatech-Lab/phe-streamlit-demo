import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
import requests
import streamlit as st

def get_api_dicom(url, downsampling_factor, angle_style, threshold) :
    try :
        print("Run get_api()")
        # Get the API
        parameters = {
            "downsampling_factor" : downsampling_factor,
            "angle_style" : angle_style,
            "threshold" : threshold,
        }
        headers = {"api-key" : "0PfSuTqMuPrKPrJLs9IblYvzslI4u9GsgcayLVSaD4reu79gq1DFv1rRuw7GXqF2i5rsWS25oGJcmS7tJjPk39qSDA2NEcesVmkktPMH0cj5Y9Pl22gb3IFXyrAlxcgn"}
        response = requests.get(url, params=parameters, headers=headers)
        if response.status_code == 200 :
            data = response.json()
            return data["data"]
        else :
            print("Error: ", response.status_code)
    except Exception as e :
        print("get_api() function get error :", e)

def visualize_series(data) :
    try :
        print("Run visualize_series()")
        # Create a figure and a 3D subplot
        fig= plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the points
        ax.scatter(data["x"], data["y"], data["z"], c=data["z"], cmap='viridis', marker='.')

        # Set labels and show the plot
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        st.pyplot(fig)
    except Exception as e :
        print("visualize_series() function get error :", e)

def show_dicom(url, min_threshold, max_threshold, mid_threshold=None) :
    try :
        # Sidebar controls
        if mid_threshold is None :
            mid_threshold = (min_threshold + max_threshold) // 2
        threshold = st.slider("Threshold", min_value=min_threshold, max_value=max_threshold, value=mid_threshold)
        downsampling_factor = st.slider("Downsampling Factor", min_value=1, max_value=10, value=10)
        angle_style = st.slider("Angle", min_value=0, max_value=5, value=0)

        # Process DICOM Series
        response = get_api_dicom(url, downsampling_factor, angle_style, threshold)
        if response is not None :
            visualize_series(response)
    except Exception as e :
        print("show_dicom() function get error :", e)

def st_dicom() :
    try :
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.title("DICOM Image Visualization")
        st.markdown("### ✅ DICOM Visualization Nawatech - PHE")

        ddr_url = "http://127.0.0.1:8000/process_dicom/ddr/"
        lung_url = "http://127.0.0.1:8000/process_dicom/lung/"
        mri_url = "http://127.0.0.1:8000/process_dicom/mri/"

        selected_option = st.selectbox("Select a DICOM Series", ["DDR", "Lung", "MRI"])
        if selected_option == "DDR" :
            show_dicom(ddr_url, 1985, 53970, 5177)
        elif selected_option == "Lung" :
            show_dicom(lung_url, -1024, 3071, 500)
        elif selected_option == "MRI" :
            show_dicom(mri_url, 0, 8847, 800)
    except Exception as e :
        print("st_dicom() function get error :", e)