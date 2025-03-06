import streamlit as st
from sidebar1 import sidebar_menu

selected_page = sidebar_menu()

if selected_page == "Search":
    import search1
    search1.search_page()
elif selected_page == "Purchase":
    import purchase
    purchase.purchase_page()
elif selected_page == "Status":
    import status
    status.status_page()
