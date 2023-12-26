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

def get_firestore_data():
    data_ref = db.collection("data")
    docs = data_ref.stream()

    data_list = []
    for doc in docs:
        data_list.append(doc.to_dict())

    return data_list

def display():
    st.header("Firestore Data Display")

    data = get_firestore_data()

    if not data:
        st.warning("No data found in the Firestore collection 'data'")
    else:
        st.table(data)