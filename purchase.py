import streamlit as st
import datetime
from handle1 import execute_query

def purchase_page():
    # Page Configuration
    st.set_page_config(
        page_title="Tree Purchase",
        page_icon="🌳",
        layout="centered"
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            margin-bottom: 1rem;
        }
        .order-summary {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .page-title {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .section-header {
            color: #34495e;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page Header
    st.markdown("<h1 class='page-title'>🌳 Tree Purchase Form</h1>", unsafe_allow_html=True)

    if 'purchase_tree' not in st.session_state:
        st.error("⚠️ No tree selected for purchase.")
        return

    tree_name = st.session_state.purchase_tree
    available_quantity = st.session_state.available_quantity
    unit_price = st.session_state.unit_price

    # Order Summary Section
    st.markdown("<div class='section-header'>Order Summary</div>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Selected Tree:** {tree_name}")
            st.markdown(f"**Available Quantity:** {available_quantity}")
        with col2:
            st.markdown(f"**Unit Price:** {unit_price} IQD")
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=int(available_quantity),
                step=1,
                help="Select the number of trees you wish to purchase"
            )
            total_price = quantity * float(unit_price)
            st.markdown(f"**Total Price:** {total_price:,.2f} IQD")

    # Customer Information Section
    st.markdown("<div class='section-header'>Customer Information</div>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            customer_full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name",
                help="Please enter your complete name as it appears on official documents"
            )
            username = st.text_input(
                "Username",
                placeholder="Choose a unique username",
                help="This username must be unique in our system"
            )
            address = st.text_area(
                "Delivery Address",
                placeholder="Enter your complete delivery address",
                help="Please provide a detailed delivery address"
            )
        with col2:
            whatsapp_number = st.text_input(
                "WhatsApp Number",
                placeholder="+964xxxxxxxxxx",
                help="Include country code"
            )
            email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                help="We'll send order confirmation to this email"
            )
            payment_preference = st.selectbox(
                "Payment Method",
                ["Credit Card", "Bank Transfer", "Cash on Arrival"],
                help="Select your preferred payment method"
            )

    # Hidden payment date field
    payment_date = datetime.date.today().isoformat()

    # Action Buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        order_button = st.button(
            "Place Order",
            type="primary",
            use_container_width=True,
            help="Click to confirm your order"
        )
        back_button = st.button(
            "Back to Home",
            use_container_width=True
        )

    if order_button:
        # Validation
        if not all([customer_full_name, username, address, whatsapp_number, email]):
            st.error("⚠️ Please fill in all required fields!")
            return

        # Database insertion
        query = """
        INSERT INTO payments (
            tree_name, customer_full_name, username, quantity, amount, address,
            whatsapp_number, email, payment_preference, payment_date, status, note
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        try:
            execute_query(query, (
                tree_name, customer_full_name, username, str(quantity),
                str(total_price), address, whatsapp_number, email,
                payment_preference, payment_date, "Pending", ""
            ))
            
            # Success message with order summary
            st.success("🎉 Order placed successfully!")
            st.balloons()
            
            # Reset purchase mode
            st.session_state.purchase_mode = False
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
            else:
                st.info("Please refresh the page to continue shopping.")
                
        except Exception as e:
            st.error(f"❌ Error placing order: {str(e)}")

    if back_button:
        st.session_state.purchase_mode = False
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.info("Please refresh the page to return to home.")

if __name__ == "__main__":
    purchase_page()
