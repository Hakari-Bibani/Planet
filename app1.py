import streamlit as st
from sidebar1 import sidebar_menu

# Get selected page from sidebar
selected_page = sidebar_menu()

if selected_page == "Home":
    import search1
    search1.home_page()
elif selected_page == "Status":
    import status1
    status1.status_page()
