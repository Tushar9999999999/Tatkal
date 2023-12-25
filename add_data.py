import pandas as pd
import streamlit as st
from google.cloud import firestore

db = firestore.Client.from_service_account_json("C:\\Users\\Admin\\Downloads\\tatkal-c7f59-firebase-adminsdk-dqdga-69d1ec6c55.json")

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

