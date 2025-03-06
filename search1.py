import streamlit as st
import pandas as pd
from handle1 import run_query

def search_page():
    st.markdown("<h1 style='text-align: center;'>Search Inventory</h1>", unsafe_allow_html=True)
    
    # Dropdown for Tree Name
    query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
    tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]
    
    col1, col2 = st.columns(2)
    with col1:
        selected_tree = st.selectbox("Select Tree Name", ["All"] + tree_names)
    
    # Packaging Type dropdown depends on selected tree name
    if selected_tree != "All":
        query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        packaging_types = [row["packaging_type"] for row in run_query(query_packaging, (selected_tree,)) or []]
    else:
        query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
        packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
    
    with col2:
        selected_packaging = st.selectbox("Select Packaging Type", ["All"] + packaging_types)
    
    # Dynamic Height Range based on available data for the selected tree
    if selected_tree != "All":
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        height_range = run_query(height_range_query, (selected_tree,))
    else:
        height_range_query = "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val FROM Nursery_Tree_Inventory;"
        height_range = run_query(height_range_query)
        
    if height_range and height_range[0]['min_val'] is not None and height_range[0]['max_val'] is not None:
        slider_min = float(height_range[0]['min_val'])
        slider_max = float(height_range[0]['max_val'])
        selected_height_range = st.slider("Select Height Range (cm)", min_value=slider_min, max_value=slider_max, value=(slider_min, slider_max))
    else:
        selected_height_range = None

    if st.button("Search Inventory", use_container_width=True):
        conditions = []
        params = []
        if selected_tree != "All":
            conditions.append("nti.tree_common_name = %s")
            params.append(selected_tree)
        if selected_packaging != "All":
            conditions.append("nti.packaging_type = %s")
            params.append(selected_packaging)
        if selected_height_range:
            conditions.append("nti.max_height >= %s AND nti.min_height <= %s")
            params.extend([selected_height_range[0], selected_height_range[1]])
        
        if conditions:
            where_clause = " AND ".join(conditions)
            query = f"""
            SELECT nti.quantity_in_stock, nti.price, nti.min_height, nti.max_height,
                   t.growth_rate, nti.tree_common_name as common_name, t.shape, t.watering_demand, 
                   t.main_photo_url, t.origin, t.soil_type, t.root_type, t.leafl_type, 
                   n.address
            FROM Nursery_Tree_Inventory nti
            JOIN Trees t ON nti.tree_common_name = t.common_name
            JOIN Nurseries n ON nti.nursery_name = n.nursery_name
            WHERE {where_clause};
            """
            results = run_query(query, tuple(params))
            if results:
                for row in results:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
                        <h3>{row['common_name']}</h3>
                        <p>Growth Rate: {row['growth_rate']} cm/yr</p>
                        <p>Quantity in Stock: {row['quantity_in_stock']}</p>
                        <p>Price: {row['price']} IQD</p>
                        <p>Height Range: {row['min_height']} cm to {row['max_height']} cm</p>
                        <p>Shape: {row['shape']}</p>
                        <p>Watering Demand: {row['watering_demand']}</p>
                        <p>Origin: {row['origin']}</p>
                        <p>Soil Type: {row['soil_type']}</p>
                        <p>Root Type: {row['root_type']}</p>
                        <p>Leaf Type: {row['leafl_type']}</p>
                        <p>Address: {row['address']}</p>
                    """, unsafe_allow_html=True)
                    if st.button("Add Purchase", key=row['common_name']):
                        st.session_state.selected_purchase = row
                        st.success("Tree selected for purchase. Please go to the Purchase page.")
            else:
                st.write("No results found.")
        else:
            st.write("Please select at least one filter.")
