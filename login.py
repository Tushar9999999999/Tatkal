import streamlit as st
import json
from google.cloud import firestore

firebase_service_account = st.secrets["firebase"]["service_account_json"]

db = firestore.Client.from_service_account_info(json.loads(firebase_service_account))

def authenticate_user(username, password):
    try:
        auth_ref = db.collection("auth")

        # Query for the user with the provided username
        query = auth_ref.where("username", "==", username).limit(1)
        user_doc = next(query.stream(), None)

        if user_doc:
            # Check if the provided password matches the stored password
            stored_password = user_doc.get("password")
            if stored_password and stored_password == password:
                st.success("Authentication successful!")
                st.session_state.authenticated = True
                return True
            else:
                st.warning("Incorrect password. Please try again.")
        else:
            st.warning("User not found. Please check your username.")
    except Exception as e:
        st.error(f"Error during authentication: {e}")
    
    return False

def login():
    st.header("Login Page")

    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if username and password:
            authenticate_result = authenticate_user(username, password)
            if authenticate_result:
                st.success("Redirecting to the dashboard...")
                st.rerun()
            else:
                st.warning("Authentication failed. Please check your credentials.")
        else:
            st.warning("Please enter both username and password.")