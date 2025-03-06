import streamlit as st
import pandas as pd
from handle1 import run_query

def set_purchase(row):
    # Update session state with purchase details.
    st.session_state.purchase_tree = row['common_name']
    st.session_state.available_quantity = row['quantity_in_stock']
    st.session_state.unit_price = row['price']
    st.session_state.purchase_mode = True
    st.experimental_rerun()

def home_page():
    # If purchase mode is active, do not render the home page.
    if st.session_state.get("purchase_mode", False):
        return

    st.markdown("<h1>Welcome to the Home Page</h1>", unsafe_allow_html=True)
    
    # Dropdown for Tree Name.
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    
    # Packaging Type dropdown based on selected tree.
    if selected_tree != "All":
        query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        packaging_types = [row["packaging_type"] for row in run_query(query_packaging, (selected_tree,)) or []]
    else:
        query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
        packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)
        
    # Dynamic Height Range Dashboard.
    if selected_tree != "All":
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        height_range = run_query(height_range_query, (selected_tree,))
    else:
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory;"
        height_range = run_query(height_range_query)
    
    if height_range and height_range[0]['min_val'] is not None and height_range[0]['max_val'] is not None:
        slider_min = float(height_range[0]['min_val'])
        slider_max = float(height_range[0]['max_val'])
        selected_height_range = st.slider("Select Height Range (cm)", min_value=slider_min, max_value=slider_max, value=(slider_min, slid
