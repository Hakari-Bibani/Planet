import streamlit as st
import pandas as pd
from handle1 import run_query

def status_page():
    # Apply custom CSS for the status page
    st.markdown("""
    <style>
        .status-header {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #f0f2f6;
        }
        
        .search-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        
        .search-button {
            background-color: #3498db;
            color: white;
            font-weight: 600;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .search-button:hover {
            background-color: #2980b9;
        }
        
        .order-table {
            border-collapse: separate;
            border-spacing: 0;
            width: 100%;
            border: 1px solid #e6e9ed;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        .order-table th {
            background-color: #f1f3f5;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            color: #2c3e50;
            border-bottom: 1px solid #e6e9ed;
        }
        
        .order-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #e6e9ed;
        }
        
        .order-table tr:last-child td {
            border-bottom: none;
        }
        
        .order-table tr:hover {
            background-color: #f8f9fa;
        }
        
        .status-pending {
            background-color: #ffeaa7;
            color: #b7791f;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.85rem;
        }
        
        .status-completed {
            background-color: #c6f6d5;
            color: #2f855a;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.85rem;
        }
        
        .status-cancelled {
            background-color: #fed7d7;
            color: #c53030;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.85rem;
        }
        
        .status-processing {
            background-color: #bee3f8;
            color: #2b6cb0;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: 500;
            font-size: 0.85rem;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .instructions {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("<h1 class='status-header'>Order Status & History</h1>", unsafe_allow_html=True)
    
    # Instructions box
    st.markdown("""
    <div class="instructions">
        <p><strong>Track Your Orders</strong>: Enter your username or email address below to view all your orders and their current status.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search container
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        identifier = st.text_input(
            "Username or Email",
            placeholder="Enter your username or email",
            help="Enter the username or email you used when placing your order"
        )
    
    with col2:
        search_clicked = st.button(
            "View Orders",
            use_container_width=True,
            help="Click to view your order history"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process search when button is clicked
    if search_clicked:
        if identifier:
            with st.spinner("Searching for your orders..."):
                query = """
                SELECT 
                    tree_name, 
                    customer_full_name, 
                    quantity, 
                    amount, 
                    address, 
                    status, 
                    note
                FROM payments
                WHERE username = %s OR email = %s
                ORDER BY status, tree_name;
                """
                results = run_query(query, (identifier, identifier))
                
            if results:
                # Convert results to DataFrame
                df = pd.DataFrame(results)
                
                # Show summary statistics
                total_orders = len(df)
                total_amount = df['amount'].sum()
                total_trees = df['quantity'].sum()
                
                # Create summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Orders", f"{total_orders}")
                with col2:
                    st.metric("Total Spent", f"{total_amount:,.2f} IQD")
                with col3:
                    st.metric("Trees Purchased", f"{total_trees}")
                
                # Custom render the orders table with better styling
                st.markdown("<h3>Your Orders</h3>", unsafe_allow_html=True)
                
                # Custom HTML table with better styling
                table_html = """
                <table class="order-table">
                    <thead>
                        <tr>
                            <th>Tree</th>
                            <th>Customer</th>
                            <th>Quantity</th>
                            <th>Amount (IQD)</th>
                            <th>Delivery Address</th>
                            <th>Status</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                for _, row in df.iterrows():
                    # Determine status class for styling
                    status_class = "status-processing"
                    status = row['status'].lower() if isinstance(row['status'], str) else ""
                    
                    if "complete" in status or "delivered" in status:
                        status_class = "status-completed"
                    elif "cancel" in status:
                        status_class = "status-cancelled"
                    elif "pending" in status or "wait" in status:
                        status_class = "status-pending"
                    
                    # Format the amount with commas
                    amount = f"{row['amount']:,.2f}" if pd.notna(row['amount']) else ""
                    
                    table_html += f"""
                    <tr>
                        <td>{row['tree_name']}</td>
                        <td>{row['customer_full_name']}</td>
                        <td>{row['quantity']}</td>
                        <td>{amount}</td>
                        <td>{row['address']}</td>
                        <td><span class="{status_class}">{row['status']}</span></td>
                        <td>{row['note'] if pd.notna(row['note']) else ""}</td>
                    </tr>
                    """
                
                table_html += """
                    </tbody>
                </table>
                """
                
                st.markdown(table_html, unsafe_allow_html=True)
                
                # Add export options
                st.download_button(
                    label="Export to CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f"tree_orders_{identifier}.csv",
                    mime="text/csv"
                )
                
            else:
                # No results found - show empty state
                st.markdown("""
                <div class="empty-state">
                    <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" width="100" height="100" alt="No orders found">
                    <h3>No Orders Found</h3>
                    <p>We couldn't find any orders associated with the provided username or email.</p>
                    <p>If you've recently placed an order, please check the spelling or try using a different identifier.</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # No identifier entered
            st.warning("Please enter a username or email to view your orders.")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Order Status - Tree Nursery",
        page_icon="🌳",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    status_page()
