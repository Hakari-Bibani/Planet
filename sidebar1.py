import streamlit as st

def sidebar_menu():
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Search"

    st.sidebar.title("Menu")
    if st.sidebar.button("Search"):
        st.session_state.selected_page = "Search"
    if st.sidebar.button("Purchase"):
        st.session_state.selected_page = "Purchase"
    if st.sidebar.button("Status"):
        st.session_state.selected_page = "Status"

    return st.session_state.selected_page
