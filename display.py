import streamlit as st
from google.cloud import firestore

# Set up Firestore client
db = firestore.Client.from_service_account_json("C:\\Users\\Admin\\Downloads\\tatkal-c7f59-firebase-adminsdk-dqdga-69d1ec6c55.json")

# Function to fetch data from Firestore
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