import streamlit as st
import datetime
from handle1 import run_query, execute_query

def purchase_page():
    st.markdown("<h1 style='text-align: center;'>Purchase Order</h1>", unsafe_allow_html=True)
    if 'selected_purchase' not in st.session_state:
        st.error("No tree selected for purchase. Please go to the Search page and select a tree.")
        return

    selected = st.session_state.selected_purchase
    st.write("**Tree Name:**", selected['common_name'])
    
    available_quantity = selected['quantity_in_stock']
    price_per_unit = selected['price']
    st.write("Available Quantity:", available_quantity)
    
    quantity = st.number_input("Enter Purchase Quantity", min_value=1, max_value=int(available_quantity), value=1)
    computed_price = quantity * float(price_per_unit)
    st.write("Total Price (IQD):", computed_price)
    
    customer_full_name = st.text_input("Customer Full Name")
    username = st.text_input("Username")
    adress = st.text_input("Address")
    whatsapp_number = st.text_input("Whatsapp Number")
    email = st.text_input("Email")
    payment_preferences = st.selectbox("Payment Preferences", ["Credit Card", "Bank Transfer", "Cash on Arrival"])
    
    # Auto-fill payment date with current timestamp
    payment_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if st.button("Order"):
        insert_query = """
        INSERT INTO payments (tree_name, customer_full_name, username, quantity, amount, adress, whatsapp_number, email, payment_preferences, payment_date, status, note)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        status_val = "Pending"
        note_val = ""
        params = (selected['common_name'], customer_full_name, username, str(quantity), str(computed_price), adress, whatsapp_number, email, payment_preferences, payment_date, status_val, note_val)
        try:
            execute_query(insert_query, params)
            st.success("Order placed successfully!")
        except Exception as e:
            st.error("Error placing order. Possibly duplicate username or a database error.")
