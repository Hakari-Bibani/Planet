import streamlit as st
from handle1 import run_query

def status_page():
    st.markdown("<h1 style='text-align: center;'>Order Status</h1>", unsafe_allow_html=True)
    search_input = st.text_input("Enter your Email or Username to check order status")
    
    if st.button("Check Status"):
        query = """
        SELECT tree_name, customer_full_name, username, quantity, amount, adress, status, note
        FROM payments
        WHERE email = %s OR username = %s;
        """
        results = run_query(query, (search_input, search_input))
        if results:
            for row in results:
                st.markdown(f"""
                **Tree Name:** {row['tree_name']}  
                **Customer Full Name:** {row['customer_full_name']}  
                **Quantity:** {row['quantity']}  
                **Price:** {row['amount']} IQD  
                **Address:** {row['adress']}  
                **Status:** {row['status']}  
                **Note:** {row['note']}  
                """)
        else:
            st.write("No orders found.")
