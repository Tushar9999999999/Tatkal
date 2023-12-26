import os
import base64
import json
import streamlit as st
from google.cloud import firestore
from google.auth.credentials import AnonymousCredentials
from dotenv import load_dotenv

#load_dotenv()

firebase_credentials_b64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

if firebase_credentials_b64:
    firebase_credentials_json = base64.b64decode(firebase_credentials_b64).decode('utf-8')
    firebase_credentials = json.loads(firebase_credentials_json)
else:
    st.warning("Firebase service account JSON not provided. Check your environment variables.")
    st.stop()

db = firestore.Client.from_service_account_info(firebase_credentials) if firebase_credentials else firestore.Client(credentials=AnonymousCredentials())

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
