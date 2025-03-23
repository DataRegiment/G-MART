import streamlit as st

st.header("Electronics Store")

def reset_form():
    st.session_state["text_input"] = ""
    
def calculate_total_price(item, quantity, promo_code):
    price = 0
    if item == "Macbook Air":
        price = 999
    elif item == "PS5":
        price = 499
    elif item == "Vintage Camera":
        price = 199
    total_price = price * quantity
    if promo_code.upper() in ["SANDEEP", "SURYA"]:
        total_price = total_price * 0.5
    elif promo_code.upper() in ["SHIVA", "HARI","ASHOK"]:
        total_price = total_price * 0.2
    return total_price

col1, col2, col3 = st.columns(3, border=True)

with col1:
    st.image("https://picsum.photos/id/0/5000/3333")
    st.write("Macbook Air")
    st.write("Price: $999")

with col2:
    st.image("https://picsum.photos/id/96/4752/3168")
    st.write("PS5")
    st.write("Price: $499")
    
with col3:
    st.image("https://picsum.photos/id/250/4928/3264")
    st.write("Vintage Camera")
    st.write("Price: $199")

with st.form("cart"):    
    item_to_buy = st.selectbox("Select an item to buy", ["Macbook Air", "PS5", "Vintage Camera"])
    quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
    delivery_location = st.selectbox("Delivery Location", ["Office", "Home", "Other"])
    promo_code = st.text_input("Promo Code(Optional)")
    st.write("Total Price: $", calculate_total_price(item_to_buy, quantity, promo_code))
    clear_cart = st.form_submit_button("Clear Cart")
    submit_button = st.form_submit_button("Buy Now")
    payment_option = st.radio("Please select Payment Option", ["Credit Card", "Debit Card", "UPI", "Net Banking"])
    
    if clear_cart:
        reset_form()

    if submit_button:
        st.write("Payment Successful")
        st.write("Thank you for shopping with us!")
