import streamlit as st
import pandas as pd
from handle1 import run_query

def set_purchase(row):
    # Update session state with purchase details.
    st.session_state.purchase_tree = row["common_name"]
    st.session_state.available_quantity = row["quantity_in_stock"]
    st.session_state.unit_price = row["price"]
    st.session_state.purchase_mode = True
    try:
        st.experimental_rerun()
    except AttributeError:
        st.warning("Automatic page refresh is unavailable. Please refresh the page manually to proceed.")

def home_page():
    # Skip rendering home page if purchase mode is active.
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
        height_range_query = (
            "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val "
            "FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
        )
        height_range = run_query(height_range_query, (selected_tree,))
    else:
        height_range_query = (
            "SELECT MIN(min_height) as min_val, MAX(max_height) as max_val "
            "FROM Nursery_Tree_Inventory;"
        )
        height_range = run_query(height_range_query)
    
    if height_range and height_range[0]["min_val"] is not None and height_range[0]["max_val"] is not None:
        slider_min = float(height_range[0]["min_val"])
        slider_max = float(height_range[0]["max_val"])
        selected_height_range = st.slider(
            "Select Height Range (cm)",
            min_value=slider_min,
            max_value=slider_max,
            value=(slider_min, slider_max)
        )
    else:
        selected_height_range = None

    if st.button("Search Inventory"):
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
                for idx, row in enumerate(results):
                    st.markdown(f"""
                    <div style="border: 1px solid #dee2e6; border-radius: 8px; padding: 15px;
                                margin-bottom: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <div style="display: flex; align-items: center;">
                            <img src="{row['main_photo_url']}" alt="Tree Photo"
                                 style="width:120px; height:120px; border-radius:8px;
                                        object-fit:cover; margin-right:15px;">
                            <div>
                                <h3 style="margin:0; color:#2c3e50;">{row['common_name']}</h3>
                                <p style="margin:0; color:#495057;">
                                    Growth Rate: {row['growth_rate']} cm/yr
                                </p>
                            </div>
                        </div>
                        <hr style="border:none; border-top:1px solid #dee2e6; margin:10px 0;">
                        <p><strong>Quantity in Stock:</strong> {row['quantity_in_stock']}</p>
                        <p><strong>Price:</strong> {row['price']} IQD</p>
                        <p><strong>Height Range:</strong> {row['min_height']} cm to {row['max_height']} cm</p>
                        <p><strong>Shape:</strong> {row['shape']}</p>
                        <p><strong>Watering Demand:</strong> {row['watering_demand']}</p>
                        <p><strong>Origin:</strong> {row['origin']}</p>
                        <p><strong>Soil Type:</strong> {row['soil_type']}</p>
                        <p><strong>Root Type:</strong> {row['root_type']}</p>
                        <p><strong>Leaf Type:</strong> {row['leafl_type']}</p>
                        <p><strong>Address:</strong> {row['address']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    unique_key = f"purchase_button_{idx}_{row['common_name']}"
                    st.button(
                        f"Add Purchase - {row['common_name']}",
                        key=unique_key,
                        on_click=set_purchase,
                        args=(row,)
                    )
            else:
                st.write("No results found.")
        else:
            st.write("Please select at least one filter.")

if __name__ == "__main__":
    home_page()
