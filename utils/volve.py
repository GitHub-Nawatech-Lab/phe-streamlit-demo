import requests
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def get_api_volve(data) :
    try :
        test_sample = json.dumps(data)
        test_sample = bytes(test_sample,encoding = 'utf8')

        # If (key) auth is enabled, don't forget to add key to the HTTP header.
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer ' + "RFj8Ki3vRGfCJzg7rlIhoQTTePF7uHwf"}
        endpoint = "http://20.239.234.167:80/api/v1/service/volve-service-aks/score"
        resp = requests.post(endpoint, test_sample, headers=headers)
        if resp.status_code == 200 :
            data = resp.json()
            return data
        else :
            print("Error: ", resp.status_code)
    except Exception as e :
        print("get_api_volve() function get error :", e)

def upload_volve_files() :
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None :
        try :
            st.write("You selected the file :", uploaded_file.name)
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e :
            st.error("Invalid CSV format. Please upload a valid CSV file.")

def process_volve(df) :
    try :
        test_df = df.drop(["DATEPRD","BORE_OIL_VOL(t)"], axis=1)
        test = {"data": test_df.values.tolist()}
        response = get_api_volve(test)
        df["Actual"] = df["BORE_OIL_VOL(t)"]
        df["Prediction"] = response["result"]
        df["DATEPRD"] = pd.to_datetime(df["DATEPRD"])
        return df
    except Exception as e :
        print("process_volve() function get error :", e)

def visualize_volve(df) :
    try :        
        # Create a line plot
        plt.figure(figsize=(8, 6))
        plt.plot(df['DATEPRD'], df['Actual'], label='Actual')
        plt.plot(df['DATEPRD'], df['Prediction'], label='Prediction')
        plt.xlabel('DATEPRD')
        plt.ylabel('Values')
        plt.xticks(rotation=90)
        plt.title('Actual vs. Prediction')
        plt.legend()
        st.pyplot(plt)
    except Exception as e :
        print("visualize_volve() function get error :", e)

def st_volve() :
    try :
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.title("Volve Production Rate Prediction")
        st.markdown("### ✅ Volve Production Nawatech - PHE")

        data = upload_volve_files()
        if data is not None :
            df = process_volve(data)
            df.drop("BORE_OIL_VOL(t)", axis=1, inplace=True)
            if df is not None :
                # Add a slider for selecting date range
                start_date = st.date_input("Select start date", min(df['DATEPRD']))
                end_date = st.date_input("Select end date", max(df['DATEPRD']))
                # Convert selected dates to datetime64[ns]
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                # Filter data based on selected date range
                filtered_df = df[(df['DATEPRD'] >= start_date) & (df['DATEPRD'] <= end_date)]
                visualize_volve(filtered_df)
                st.dataframe(filtered_df)
    except Exception as e :
        print("st_volve() function get error :", e)
