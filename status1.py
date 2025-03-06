import streamlit as st
import pandas as pd
from handle1 import run_query

def status_page():
    st.markdown("<h2>Order Status</h2>", unsafe_allow_html=True)
    identifier = st.text_input("Enter your Username or Email to view your orders")
    if st.button("View Orders"):
        if identifier:
            query = """
            SELECT tree_name, "  customer_full_name", quantity, " amount", adress, status, note
            FROM payments
            WHERE username = %s OR email = %s;
            """
            results = run_query(query, (identifier, identifier))
            if results:
                df = pd.DataFrame(results)
                st.write(df)
            else:
                st.write("No orders found for the given identifier.")
        else:
            st.write("Please enter a Username or Email.")
