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
    adress = st.text_input("Address")
    whatsapp_number = st.text_input("Whatsapp Number")
    email = st.text_input("Email")
    payment_preferences = st.selectbox("Payment Preferences", ["Credit Card", "Bank Transfer", "Cash on Arrival"])

    payment_date = datetime.date.today().isoformat()

    if st.button("Order"):
        # Ensure that the column names match exactly what is in your payments table.
        query = """
        INSERT INTO payments ("  customer_full_name", username, quantity, " amount", adress, whatsapp_number, email, payment_preferences, payment_date, status, note, tree_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        status = "Pending"
        note = ""
        try:
            execute_query(query, (
                customer_full_name,
                username,
                str(quantity),
                str(total_price),
                adress,
                whatsapp_number,
                email,
                payment_preferences,
                payment_date,
                status,
                note,
                tree_name
            ))
            st.success("Order placed successfully!")
            st.session_state.purchase_mode = False
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.warning("Automatic page refresh is unavailable. Please refresh the page manually.")
        except Exception as e:
            st.error(f"Error placing order: {e}")

    if st.button("Back to Home"):
        st.session_state.purchase_mode = False
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.warning("Automatic page refresh is unavailable. Please refresh the page manually.")
