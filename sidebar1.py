import streamlit as st

def sidebar_menu():
    # Apply custom CSS styling for the sidebar
    st.sidebar.markdown("""
    <style>
        .sidebar-title {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #f0f2f6;
            text-align: center;
        }
        
        .sidebar-menu-button {
            background-color: white;
            color: #2c3e50;
            border: 1px solid #e6e9ed;
            border-radius: 8px;
            padding: 10px 15px;
            margin-bottom: 10px;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
            width: 100%;
            display: flex;
            align-items: center;
        }
        
        .sidebar-menu-button:hover {
            background-color: #f8f9fa;
            border-color: #cbd5e0;
            transform: translateX(5px);
        }
        
        .sidebar-menu-button.active {
            background-color: #3498db;
            color: white;
            border-color: #2980b9;
        }
        
        .sidebar-icon {
            margin-right: 10px;
            width: 20px;
            text-align: center;
        }
        
        .sidebar-divider {
            margin: 20px 0;
            border: none;
            border-top: 1px solid #e6e9ed;
        }
        
        .sidebar-footer {
            font-size: 0.8rem;
            color: #7f8c8d;
            text-align: center;
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar header
    st.sidebar.markdown("<h2 class='sidebar-title'>🌳 Tree Nursery</h2>", unsafe_allow_html=True)
    
    # Initialize session state for selected page if not exists
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    # Menu buttons with active state styling
    home_active = "active" if st.session_state.selected_page == "Home" else ""
    status_active = "active" if st.session_state.selected_page == "Status" else ""
    
    # Home button
    if st.sidebar.markdown(f"""
    <button class="sidebar-menu-button {home_active}">
        <span class="sidebar-icon">🏠</span> Home
    </button>
    """, unsafe_allow_html=True):
        st.session_state.selected_page = "Home"
        st.session_state.purchase_mode = False  # ensure purchase mode is off
        # Only call experimental_rerun if it exists
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
    
    # Status button
    if st.sidebar.markdown(f"""
    <button class="sidebar-menu-button {status_active}">
        <span class="sidebar-icon">📊</span> Status
    </button>
    """, unsafe_allow_html=True):
        st.session_state.selected_page = "Status"
        st.session_state.purchase_mode = False
        # Only call experimental_rerun if it exists
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
    
    # Add a divider
    st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    
    # Handle actual button clicks since the HTML buttons are just for show
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Home", key="home_btn", use_container_width=True):
            st.session_state.selected_page = "Home"
            st.session_state.purchase_mode = False
    
    with col2:
        if st.button("Status", key="status_btn", use_container_width=True):
            st.session_state.selected_page = "Status"
            st.session_state.purchase_mode = False
    
    # Add user information section if logged in
    if 'user_logged_in' in st.session_state and st.session_state.user_logged_in:
        st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
        st.sidebar.subheader("User Profile")
        st.sidebar.info(f"Logged in as: {st.session_state.get('username', 'User')}")
        
        if st.sidebar.button("Logout", key="logout_btn", use_container_width=True):
            st.session_state.user_logged_in = False
            # Add any other logout logic here
    
    # Add footer
    st.sidebar.markdown("""
    <div class='sidebar-footer'>
        Tree Nursery Management System<br>
        © 2025 All Rights Reserved
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.selected_page
