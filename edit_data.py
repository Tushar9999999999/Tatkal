import streamlit as st
import json
from google.cloud import firestore

firebase_service_account = st.secrets["firebase"]["service_account_json"]

db = firestore.Client.from_service_account_info(json.loads(firebase_service_account))

def get_consumer_names():
    try:
        data_ref = db.collection("data")
        docs = data_ref.stream()
        for doc in docs:
            consumer_names = [doc.to_dict().get("Consumer Name")]
        return consumer_names
    except Exception as e:
        st.error(f"Error retrieving consumer names: {e}")
        return []

def get_data_by_consumer_name(consumer_name):
    try:
        data_ref = db.collection("data")
        query = data_ref.where("Consumer Name", "==", consumer_name).limit(1)
        doc = next(query.stream(), None)
        return doc.to_dict() if doc else None
    except Exception as e:
        st.error(f"Error retrieving data for {consumer_name}: {e}")
        return None

def edit_data():
    st.title("Edit Data")

    consumer_names = get_consumer_names()
    selected_consumer_name = st.selectbox("Select Consumer Name:", consumer_names)

    if st.button("Show Details"):
        if selected_consumer_name:
            data = get_data_by_consumer_name(selected_consumer_name)
            if data:
                st.write(f"Details for {selected_consumer_name}:")
                st.json(data)
            else:
                st.warning("Data not found for the selected consumer name.")
        else:
            st.warning("Please select a consumer name.")