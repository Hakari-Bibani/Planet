import streamlit as st
import datetime
from handle1 import execute_query

def purchase_page():
    st.markdown("<h2>Purchase Page</h2>", unsafe_allow_html=True)
    
    if 'purchase_tree' not in st.session_state:
        st.error("No tree selected for purchase.")
        return
    
    tree_name = st.session_state.purchase_tree
    available_quantity = st.session_state.available_quantity
    unit_price = st.session_state.unit_price
    
    st.write(f"**Tree Name:** {tree_name}")
    st.write(f"**Available Quantity:** {available_quantity}")
    
    quantity = st.number_input("Enter Quantity", min_value=1, max_value=int(available_quantity), step=1)
    total_price = quantity * float(unit_price)
    st.write(f"**Total Price:** {total_price} IQD")
    
    customer_full_name = st.text_input("Customer Full Name")
    username = st.text_input("Username (must be unique)")
    address = st.text_input("Address")
    whatsapp_number = st.text_input("Whatsapp Number")
    email = st.text_input("Email")
    payment_preference = st.selectbox("Payment Preference", ["Credit Card", "Bank Transfer", "Cash on Arrival"])
    
    # Auto-fill the payment date as today's date.
    payment_date = datetime.date.today().isoformat()
    
    if st.button("Order"):
        # The INSERT query now matches the table schema:
        # (tree_name, customer_full_name, username, quantity, amount, address,
        #  whatsapp_number, email, payment_preference, payment_date, status, note)
        query = """
        INSERT INTO payments (tree_name, customer_full_name, username, quantity, amount, address, whatsapp_number, email, payment_preference, payment_date, status, note)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        status = "Pending"
        note = ""
        try:
            execute_query(query, (
                tree_name,
                customer_full_name,
                username,
                str(quantity),
                str(total_price),
                address,
                whatsapp_number,
                email,
                payment_preference,
                payment_date,
                status,
                note
            ))
            st.success("Order placed successfully!")
            st.session_state.purchase_mode = False
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.info("Please refresh the page manually.")
        except Exception as e:
            st.error(f"Error placing order: {e}")
    
    if st.button("Back to Home"):
        st.session_state.purchase_mode = False
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.info("Please refresh the page manually.")

if __name__ == "__main__":
    purchase_page()
