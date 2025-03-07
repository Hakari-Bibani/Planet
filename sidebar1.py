import streamlit as st

def sidebar_menu():
    # Apply custom CSS for the sidebar
    st.markdown("""
    <style>
        .sidebar-header {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #f0f2f6;
            text-align: center;
        }
        
        .sidebar-menu-item {
            background-color: white;
            color: #2c3e50;
            border: 1px solid #e6e9ed;
            border-radius: 6px;
            padding: 10px 15px;
            margin-bottom: 10px;
            text-align: left;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            width: 100%;
        }
        
        .sidebar-menu-item:hover {
            background-color: #f8f9fa;
            border-color: #cbd3da;
            box-shadow: 0 4px 8px rgba(0,0,0,0.08);
            transform: translateY(-2px);
        }
        
        .sidebar-menu-item-active {
            background-color: #3498db;
            color: white;
            border: 1px solid #2980b9;
        }
        
        .sidebar-menu-item-active:hover {
            background-color: #2980b9;
            color: white;
        }
        
        .sidebar-logo {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .sidebar-divider {
            margin: 20px 0;
            border: none;
            height: 1px;
            background-color: #e6e9ed;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create logo and header
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <span style="font-size: 2rem; color: #27ae60;">🌳</span>
    </div>
    <h2 class="sidebar-header">Tree Nursery</h2>
    """, unsafe_allow_html=True)
    
    # Initialize session state if not exists
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    # Create menu items with active state
    home_active = "sidebar-menu-item-active" if st.session_state.selected_page == "Home" else ""
    status_active = "sidebar-menu-item-active" if st.session_state.selected_page == "Status" else ""
    
    # Home button
    if st.sidebar.button("Home", key="home_button", 
                        help="Go to the homepage to search tree inventory",
                        use_container_width=True):
        st.session_state.selected_page = "Home"
        st.session_state.purchase_mode = False  # ensure purchase mode is off
    
    # Add CSS class to button based on active state
    st.sidebar.markdown(f"""
    <script>
        const homeButton = document.querySelector('[data-testid="stButton"] button:contains("Home")');
        if (homeButton) {{
            homeButton.className += " sidebar-menu-item {home_active}";
        }}
    </script>
    """, unsafe_allow_html=True)
    
    # Status button
    if st.sidebar.button("Status", key="status_button", 
                        help="View purchase status and history",
                        use_container_width=True):
        st.session_state.selected_page = "Status"
        st.session_state.purchase_mode = False
    
    # Add CSS class to button based on active state
    st.sidebar.markdown(f"""
    <script>
        const statusButton = document.querySelector('[data-testid="stButton"] button:contains("Status")');
        if (statusButton) {{
            statusButton.className += " sidebar-menu-item {status_active}";
        }}
    </script>
    """, unsafe_allow_html=True)
    
    # Add divider
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Display current page indicator
    st.sidebar.markdown(f"""
    <div style="padding: 10px; background-color: #f8f9fa; border-radius: 6px; text-align: center;">
        <p style="margin: 0; color: #2c3e50; font-weight: 500;">Current Page: <span style="color: #3498db; font-weight: 600;">{st.session_state.selected_page}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some useful info at the bottom of sidebar
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.info("Need help? Contact the nursery at support@treenursery.com or call +1-234-567-8910")
    
    return st.session_state.selected_page
