import pandas as pd
import os
import base64
import json
import streamlit as st
from google.cloud import firestore
from google.auth.credentials import AnonymousCredentials
from dotenv import load_dotenv

firebase_service_account_json = st.secrets["firebase"]["service_account_json"]
firebase_service_account = json.loads(firebase_service_account_json)

db = firestore.Client.from_service_account_info(firebase_service_account)

def add_data_to_firestore(data):
    data_ref = db.collection("data")

    data_dict_list = data.to_dict(orient='records')
    for data_dict in data_dict_list:
        data_ref.add(data_dict)

    st.success("Data added to Firestore successfully.")

def add_data():
    st.header("Firestore Data Uploader")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

    if uploaded_file is not None:
        st.write("File Uploaded Successfully!")

        excel_data = pd.read_excel(uploaded_file)

        st.write("Preview of the Data:")
        st.write(excel_data.head())

        if st.button("Add Data to Firestore"):
            add_data_to_firestore(excel_data)

