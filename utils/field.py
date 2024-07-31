import requests
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import ast

def get_api_field(data) :
    try :
        test_sample = json.dumps(data)
        test_sample = bytes(test_sample,encoding = 'utf8')

        # If (key) auth is enabled, don't forget to add key to the HTTP header.
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer ' + "wgiE9yysAHSoSddHP94aZ8ET4GSEK8zB"}
        endpoint = "http://20.239.234.167:80/api/v1/service/field-classification/score"
        resp = requests.post(endpoint, test_sample, headers=headers)
        if resp.status_code == 200 :
            data = resp.json()
            return data
        else :
            print("Error: ", resp.status_code)
    except Exception as e :
        print("get_api_field() function get error :", e)

def upload_field_files() :
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None :
        try :
            st.write("You selected the file :", uploaded_file.name)
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e :
            st.error("Invalid CSV format. Please upload a valid CSV file.")

def process_field(df) :
    try :
        test_df = df.drop("Onshore/Offshore", axis=1)
        test = {"data": test_df.values.tolist()}
        response = get_api_field(test)
        df["Actual"] = df["Onshore/Offshore"]
        df["Prediction"] = ast.literal_eval(response)
        return df
    except Exception as e :
        print("process_field() function get error :", e)

def plot_confusion_matrix(y_true, y_pred, class_names=None):
    try :
        cm = confusion_matrix(y_true, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax, xticklabels=class_names, yticklabels=class_names)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('Confusion Matrix')
        st.pyplot(fig)
    except Exception as e :
        print("plot_confusion_matrix() function get error :", e)

def plot_class_distribution(y_true, y_pred):
    try:
        df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
        
        # Get the value counts for actual and predicted
        actual_counts = df['Actual'].value_counts().sort_index()
        predicted_counts = df['Predicted'].value_counts().sort_index()
        
        # Create a DataFrame to align the counts
        counts_df = pd.DataFrame({'Actual': actual_counts, 'Predicted': predicted_counts}).fillna(0)
        
        fig, ax = plt.subplots()
        
        # Define the width of the bars
        bar_width = 0.35
        
        # Get the positions for the bars
        index = counts_df.index
        actual_positions = range(len(index))
        predicted_positions = [p + bar_width for p in actual_positions]
        
        # Plot the bars
        ax.bar(actual_positions, counts_df['Actual'], width=bar_width, alpha=0.5, color='blue', label='Actual')
        ax.bar(predicted_positions, counts_df['Predicted'], width=bar_width, alpha=0.5, color='red', label='Predicted')
        
        # Set the labels and title
        ax.set_xlabel('Class')
        ax.set_ylabel('Count')
        ax.set_title('Class Distribution')
        ax.set_xticks([p + bar_width / 2 for p in actual_positions])
        ax.set_xticklabels(index)
        ax.legend()
        
        st.pyplot(fig)
    except Exception as e:
        print("plot_class_distribution() function get error:", e)

def st_field() :
    try :
        st.markdown("""
            <style>
                .stDeployButton {display:none;}
            </style>
        """, unsafe_allow_html=True)

        st.title("Field Prediction")
        st.markdown("### ✅ Volve Prediction Nawatech - PHE")

        data = upload_field_files()
        if data is not None :
            df = process_field(data)
            df.drop("Onshore/Offshore", axis=1, inplace=True)
            if df is not None :
                class_names = df['Actual'].unique().tolist()
                plot_confusion_matrix(df["Actual"], df["Prediction"], class_names)
                plot_class_distribution(df["Actual"], df["Prediction"])
                st.dataframe(df)
    except Exception as e :
        print("st_field() function get error :", e)