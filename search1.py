import streamlit as st
import pandas as pd
from handle1 import run_query

def set_purchase(row):
    # Update session state with purchase details
    st.session_state.purchase_tree = row["common_name"]
    st.session_state.available_quantity = row["quantity_in_stock"]
    st.session_state.unit_price = row["price"]
    st.session_state.purchase_mode = True
    # Only call experimental_rerun if it exists
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("Automatic page refresh is unavailable. Please refresh the page manually.")

def home_page():
    # If purchase mode is active, do not render the home page
    if st.session_state.get("purchase_mode", False):
        return

    # Apply custom CSS for better styling
    st.markdown("""
    <style>
        .main-header {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
            padding-bottom: 1rem;
            border-bottom: 2px solid #f0f2f6;
        }
        .tree-card {
            border: 1px solid #e6e9ed;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .tree-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.12);
        }
        .tree-image {
            width: 140px;
            height: 140px;
            border-radius: 8px;
            object-fit: cover;
            margin-right: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        .tree-title {
            margin: 0;
            color: #2c3e50;
            font-size: 1.4rem;
            font-weight: 600;
        }
        .tree-subtitle {
            margin: 5px 0;
            color: #576574;
            font-size: 1rem;
        }
        .tree-details {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .detail-item {
            margin: 0;
            font-size: 0.9rem;
        }
        .detail-label {
            font-weight: 600;
            color: #2d3436;
        }
        .detail-value {
            color: #576574;
        }
        .search-button {
            background-color: #27ae60;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .search-button:hover {
            background-color: #219653;
        }
        .purchase-button {
            background-color: #3498db;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .purchase-button:hover {
            background-color: #2980b9;
        }
        .filters-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        .divider {
            border: none;
            border-top: 1px solid #e6e9ed;
            margin: 15px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main header
    st.markdown("<h1 class='main-header'>Tree Nursery Inventory</h1>", unsafe_allow_html=True)

    # Filters container
    with st.container():
        st.markdown("<div class='filters-container'>", unsafe_allow_html=True)
        st.subheader("Search Filters")

        # Dropdown for Tree Name
        query_tree_names = "SELECT DISTINCT tree_common_name FROM Nursery_Tree_Inventory;"
        tree_names = [row["tree_common_name"] for row in run_query(query_tree_names) or []]

        col1, col2 = st.columns(2)
        with col1:
            selected_tree = st.selectbox("Tree Species", ["All"] + tree_names, help="Filter by tree species")
        
        # Packaging Type dropdown based on selected tree
        if selected_tree != "All":
            query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory WHERE tree_common_name = %s;"
            packaging_types = [row["packaging_type"] for row in run_query(query_packaging, (selected_tree,)) or []]
        else:
            query_packaging = "SELECT DISTINCT packaging_type FROM Nursery_Tree_Inventory;"
            packaging_types = [row["packaging_type"] for row in run_query(query_packaging) or []]
        
        with col2:
            selected_packaging = st.selectbox("Packaging Type", ["All"] + packaging_types, help="Filter by packaging type")
            
        # Dynamic Height Range Dashboard
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
                "Height Range (cm)",
                min_value=slider_min,
                max_value=slider_max,
                value=(slider_min, slider_max),
                help="Filter trees by height range"
            )
        else:
            selected_height_range = None

        # Search button with improved styling
        search_clicked = st.button("Search Inventory", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Process search when button is clicked
    if search_clicked:
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
            WHERE {where_clause}
            ORDER BY nti.quantity_in_stock DESC;
            """
            results = run_query(query, tuple(params))
            
            if results:
                st.success(f"Found {len(results)} trees matching your criteria")
                
                for idx, row in enumerate(results):
                    # Create a stylish card for each tree
                    st.markdown(f"""
                    <div class="tree-card">
                        <div style="display: flex; align-items: center;">
                            <img src="{row['main_photo_url']}" alt="{row['common_name']}" class="tree-image">
                            <div>
                                <h3 class="tree-title">{row['common_name']}</h3>
                                <p class="tree-subtitle">Growth Rate: {row['growth_rate']} cm/yr</p>
                                <p class="tree-subtitle">Price: <strong>{row['price']} IQD</strong> | Stock: <strong>{row['quantity_in_stock']}</strong></p>
                            </div>
                        </div>
                        <hr class="divider">
                        <div class="tree-details">
                            <p class="detail-item"><span class="detail-label">Height:</span> <span class="detail-value">{row['min_height']} - {row['max_height']} cm</span></p>
                            <p class="detail-item"><span class="detail-label">Shape:</span> <span class="detail-value">{row['shape']}</span></p>
                            <p class="detail-item"><span class="detail-label">Watering:</span> <span class="detail-value">{row['watering_demand']}</span></p>
                            <p class="detail-item"><span class="detail-label">Origin:</span> <span class="detail-value">{row['origin']}</span></p>
                            <p class="detail-item"><span class="detail-label">Soil Type:</span> <span class="detail-value">{row['soil_type']}</span></p>
                            <p class="detail-item"><span class="detail-label">Root Type:</span> <span class="detail-value">{row['root_type']}</span></p>
                            <p class="detail-item"><span class="detail-label">Leaf Type:</span> <span class="detail-value">{row['leafl_type']}</span></p>
                            <p class="detail-item"><span class="detail-label">Available at:</span> <span class="detail-value">{row['address']}</span></p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Purchase button with unique key
                    unique_key = f"purchase_button_{idx}_{row['common_name']}"
                    if st.button(
                        f"Purchase {row['common_name']}",
                        key=unique_key,
                        on_click=set_purchase,
                        args=(row,),
                        use_container_width=True
                    ):
                        pass
            else:
                st.warning("No trees found matching your criteria. Please adjust your filters and try again.")
        else:
            st.info("Please select at least one filter to search the inventory.")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Tree Nursery Inventory",
        page_icon="🌳",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state if not exists
    if "purchase_mode" not in st.session_state:
        st.session_state.purchase_mode = False
        
    home_page()
