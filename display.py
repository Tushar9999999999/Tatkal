import json
import streamlit as st
from google.cloud import firestore
import pandas as pd

firebase_service_account_json = st.secrets["firebase"]["service_account_json"]
firebase_service_account = json.loads(firebase_service_account_json)

db = firestore.Client.from_service_account_info(firebase_service_account)

def get_firestore_data():
    data_ref = db.collection("data")
    docs = data_ref.stream()

    data_list = []
    for doc in docs:
        column_order = ["Consumer Name", "Date Of Birth", "Gender", "Income Tax Id Number", "Passport Number", "Passport Issue Date", "Passport Expiry Date", "Voter Id Number", "Driver’s License Number", "Driving License Issue Date", "Driving License Expiry Date", "Ration Card Number", "Universal ID Number", "Additional ID #1", "Additional ID #2", "TelephoneNo.Mobile", "Telephone No.Residence", "Telephone No.Office", "Extension Office", "Telephone No.Other", "Extension Other", "E-Mail ID 1", "E-Mail ID 2", "Address 1", "State Code1", "PIN Code 1", "Address Category1", "Residence Code1", "Address 2", "State Code2", "PIN Code 2", "Address Category2", "Residence Code2", "Current/New Reporting Member Code", "Current/New Member Short Name", "Current/New Account Number", "Unnamed: 36", "Unnamed: 37", "Account Type", "Ownership Indicator", "Date Opened/Disbursed", "Date Of Last Payment", "Date Closed", "Date Reported", "High Credit/Sanctioned Amount", "Current Balance", "Amount Overdue", "Number Of Days Past Due", "Old Reporting Member Code", "Old Member Short Name", "Old Account Number", "Old Account Type", "Old Ownership Indicator", "Suit Filed/Wilful Default", "Credit Facility Status", "Asset Classification", "Value of Collateral", "Type of Collateral", "Credit Limit", "Cash Limit", "Rate Of Interest", "Repayment Tenure", "EMI Amount", "Written-off Amount(Total)", "Written-off Amount(Principal)", "Settlement Amount", "Payment Frequency", "Actual Payment Amount", "Occupation Code", "Income", "Net/Gross Income Indicator", "Monthly/Annual Income Indicator"]
        custom_dict = {column: str(doc.to_dict().get(column, None)) for column in column_order}

		# Convert NaN values to None
        custom_dict = {k: None if pd.isna(v) else v for k, v in custom_dict.items()}

        # Append the custom dictionary to the data_list
        data_list.append(custom_dict)

    return data_list

def display():
    st.header("Data Display")

    data = get_firestore_data()

    if not data:
        st.warning("No data found in the Firestore collection 'data'")
    else:
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Display the DataFrame in Streamlit
        st.table(df)

        # Add a button to download the data as an Excel file
        if st.button("Download Data as Excel"):
            # Save the file locally
            excel_file = df.to_excel("data_export.xlsx", index=False)
            
            # Create a download link
            st.download_button(
                label="Download Excel File",
                data=open("data_export.xlsx", "rb").read(),
                key="download_excel",
                file_name="data_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            st.success("Data exported to data_export.xlsx")
