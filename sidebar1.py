import streamlit as st

def sidebar_menu():
    st.sidebar.markdown("<h2>Menu</h2>", unsafe_allow_html=True)
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    if st.sidebar.button("Home"):
        st.session_state.selected_page = "Home"
    if st.sidebar.button("Status"):
        st.session_state.selected_page = "Status"
    return st.session_state.selected_page
