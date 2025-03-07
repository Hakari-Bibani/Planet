import streamlit as st
import pandas as pd
from handle1 import run_query

def status_page():
    # Apply custom CSS for better styling
    st.markdown("""
    <style>
        .status-header {
            color: #2c3e50;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #f0f2f6;
            text-align: center;
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
            border-radius: 6px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .search-button:hover {
            background-color: #2980b9;
        }
        .order-table {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            border-radius: 10px;
            overflow: hidden;
        }
        .order-table thead tr {
            background-color: #3498db;
            color: white;
            text-align: left;
            font-weight: bold;
        }
        .order-table th, .order-table td {
            padding: 12px 15px;
        }
        .order-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .order-table tbody tr:nth-of-type(even) {
            background-color: #f8f9fa;
        }
        .order-table tbody tr:last-of-type {
            border-bottom: 2px solid #3498db;
        }
        .status-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            text-align: center;
        }
        .status-pending {
            background-color: #f39c12;
            color: white;
        }
        .status-delivered {
            background-color: #27ae60;
            color: white;
        }
        .status-cancelled {
            background-color: #e74c3c;
            color: white;
        }
        .status-processing {
            background-color: #3498db;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 class='status-header'>Order Status & History</h1>", unsafe_allow_html=True)
    
    # Search container
    st.markdown("<div class='search-container'>", unsafe_allow_html=True)
    
    # Info message
    st.info("Enter your username or email to view your order history and current status.")
    
    # Create a clean form layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        identifier = st.text_input("Username or Email", 
                                  placeholder="Enter your username or email address",
                                  help="Please enter the username or email you used when placing your order")
    
    with col2:
        search_clicked = st.button("View Orders", 
                                 use_container_width=True,
                                 help="Click to search for your orders")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process search
    if search_clicked:
        if identifier:
            # Display loading message
            with st.spinner("Searching for your orders..."):
                query = """
                SELECT tree_name, customer_full_name, quantity, amount, address, status, note,
                       payment_date, payment_preference
                FROM payments
                WHERE username = %s OR email = %s
                ORDER BY payment_date DESC;
                """
                results = run_query(query, (identifier, identifier))
            
            if results:
                # Convert to DataFrame
                df = pd.DataFrame(results)
                
                # Display a summary card
                st.success(f"Found {len(results)} orders for {identifier}")
                
                # Create a custom table with HTML/CSS for better styling
                table_html = """
                <table class="order-table">
                    <thead>
                        <tr>
                            <th>Tree</th>
                            <th>Customer</th>
                            <th>Quantity</th>
                            <th>Amount</th>
                            <th>Address</th>
                            <th>Date</th>
                            <th>Payment</th>
                            <th>Status</th>
                            <th>Notes</th>
                        </tr>
                    </thead>
                    <tbody>
                """
                
                # Add rows to the table
                for _, row in df.iterrows():
                    # Determine status badge class
                    status_class = "status-pending"
                    if row["status"].lower() == "delivered":
                        status_class = "status-delivered"
                    elif row["status"].lower() == "cancelled":
                        status_class = "status-cancelled"
                    elif row["status"].lower() == "processing":
                        status_class = "status-processing"
                    
                    # Format payment date
                    try:
                        payment_date = pd.to_datetime(row["payment_date"]).strftime("%b %d, %Y")
                    except:
                        payment_date = row["payment_date"]
                    
                    # Add row to table
                    table_html += f"""
                    <tr>
                        <td>{row["tree_name"]}</td>
                        <td>{row["customer_full_name"]}</td>
                        <td>{row["quantity"]}</td>
                        <td>{row["amount"]} IQD</td>
                        <td>{row["address"]}</td>
                        <td>{payment_date}</td>
                        <td>{row["payment_preference"]}</td>
                        <td><span class="status-badge {status_class}">{row["status"]}</span></td>
                        <td>{row["note"]}</td>
                    </tr>
                    """
                
                # Close the table
                table_html += """
                    </tbody>
                </table>
                """
                
                # Display the custom table
                st.markdown(table_html, unsafe_allow_html=True)
                
                # Display helpful note
                st.info("For any questions about your order, please contact our customer service at +1-234-567-8910 or support@treenursery.com.")
                
            else:
                st.warning("No orders found for the given username or email. Please check your information and try again.")
        else:
            st.error("Please enter a username or email to search for your orders.")

if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Order Status | Tree Nursery",
        page_icon="🌳",
        layout="wide"
    )
    status_page()
