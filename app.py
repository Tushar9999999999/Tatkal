import streamlit as st
from google.cloud import firestore
from display import display
from add_data import add_data 

def main():
    st.set_page_config(
        page_title="Tatkal Excel",
        page_icon="💉",
    )
    st.title("Tatkal Excel")

    menu = ["Display", "Add data"]
    choice = st.sidebar.selectbox("Nav", menu)

    if choice == "Display":
        display()
        
    elif choice == "Add data":
        add_data()

if __name__ == '__main__':
    main()
