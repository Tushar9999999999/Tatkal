import streamlit as st
import json
from google.cloud import firestore

# Initialize Firebase Client
firebase_service_account = st.secrets["firebase"]["service_account_json"]
db = firestore.Client.from_service_account_info(json.loads(firebase_service_account))

# Function to get all consumer names
def get_consumer_names():
    try:
        data_ref = db.collection("data")
        docs = data_ref.stream()
        consumer_names = [doc.to_dict().get("Consumer Name") for doc in docs]
        return consumer_names
    except Exception as e:
        st.error(f"Error retrieving consumer names: {e}")
        return []

# Function to select a consumer
def select_consumer():
    consumer_names = get_consumer_names()
    selected_consumer = st.selectbox("Select Consumer", consumer_names)
    return selected_consumer

# Function to select a column field
def select_column():
    columns = ["Consumer Name", "Date Of Birth", "Gender", "Income Tax Id Number", "Passport Number", "Passport Issue Date", "Passport Expiry Date", "Voter Id Number", "Driver’s License Number", "Driving License Issue Date", "Driving License Expiry Date", "Ration Card Number", "Universal ID Number", "Additional ID #1", "Additional ID #2", "TelephoneNo.Mobile", "Telephone No.Residence", "Telephone No.Office", "Extension Office", "Telephone No.Other", "Extension Other", "E-Mail ID 1", "E-Mail ID 2", "Address 1", "State Code1", "PIN Code 1", "Address Category1", "Residence Code1", "Address 2", "State Code2", "PIN Code 2", "Address Category2", "Residence Code2", "Current/New Reporting Member Code", "Current/New Member Short Name", "Current/New Account Number", "Unnamed: 36", "Unnamed: 37", "Account Type", "Ownership Indicator", "Date Opened/Disbursed", "Date Of Last Payment", "Date Closed", "Date Reported", "High Credit/Sanctioned Amount", "Current Balance", "Amount Overdue", "Number Of Days Past Due", "Old Reporting Member Code", "Old Member Short Name", "Old Account Number", "Old Account Type", "Old Ownership Indicator", "Suit Filed/Wilful Default", "Credit Facility Status", "Asset Classification", "Value of Collateral", "Type of Collateral", "Credit Limit", "Cash Limit", "Rate Of Interest", "Repayment Tenure", "EMI Amount", "Written-off Amount(Total)", "Written-off Amount(Principal)", "Settlement Amount", "Payment Frequency", "Actual Payment Amount", "Occupation Code", "Income", "Net/Gross Income Indicator", "Monthly/Annual Income Indicator"]
    selected_column = st.selectbox("Select Column", columns)
    return selected_column

# Function to type new data
def enter_data():
    new_data = st.text_input("Enter New Data")
    return new_data

# Function to edit data on button click
def edit_data_helper(selected_consumer, selected_column, new_data):
    try:
        data_ref = db.collection("data")
        query = data_ref.where("`Consumer Name`", "==", selected_consumer).limit(1)
        docs = query.stream()

        for doc in docs:
            doc_ref = data_ref.document(doc.id)
            doc_data = doc.to_dict()
            doc_data[selected_column] = new_data
            doc_ref.set(doc_data)

        st.success(f"Data for {selected_consumer} in {selected_column} column edited successfully.")
    except Exception as e:
        st.error(f"Error editing data: {e}")

# Main Streamlit app
def edit_data():
    st.title("Edit Consumer Data")

    selected_consumer = select_consumer()
    selected_column = select_column()
    new_data = enter_data()

    if st.button("Edit Data"):
        edit_data_helper(selected_consumer, selected_column, new_data)
