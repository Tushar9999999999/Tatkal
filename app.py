import streamlit as st
from display import display
from add_data import add_data 
from login import login
from edit_data import edit_data

# Initialize authentication state in session_state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def main():
    st.set_page_config(
        page_title="Tatkal",
        page_icon="📋",
    )
    st.title("Tatkal")
    
    if not st.session_state.authenticated:
        login()  # Display login page
    else:
        # Display other pages only if authenticated
        menu = ["Display", "Add data", "Edit data"]
        choice = st.sidebar.selectbox("Nav", menu)

        if choice == "Display":
            display()
        elif choice == "Add data":
            add_data()
        elif choice == "Edit data":
            edit_data()

if __name__ == '__main__':
    main()
