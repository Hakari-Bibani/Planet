import streamlit as st

# Initialize purchase_mode flag if not present
if "purchase_mode" not in st.session_state:
    st.session_state.purchase_mode = False

# If purchase_mode is active, skip the sidebar and show purchase page.
if st.session_state.purchase_mode:
    import purchase
    purchase.purchase_page()
else:
    from sidebar1 import sidebar_menu
    selected_page = sidebar_menu()
    
    if selected_page == "Home":
        import search1
        search1.home_page()
    elif selected_page == "Status":
        import status1
        status1.status_page()
