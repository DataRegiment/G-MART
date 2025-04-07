import streamlit as st
from duckdb_utils import *


st.header("Electronics Store")
con = connect_duckdb()
# create_tables(con)
load_extentions_and_secrets(con)
unique_filename = get_unique_filename()
# con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
con.execute(f"copy (select '/products' as page_name,CURRENT_TIMESTAMP as visit_ts) to 's3://tgt-southdms/g-mart/page_visits/{unique_filename}'  (FORMAT parquet);")
    
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

with st.form("cart", clear_on_submit=True):    
    item_to_buy = st.selectbox("Select an item to buy", ["Macbook Air", "PS5", "Vintage Camera"])
    quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
    mobile_number = st.number_input("Please enter your mobile number", min_value=9000000000, max_value=9999999999)
    delivery_location = st.selectbox("Delivery Location", ["Office", "Home", "Other"])
    promo_code = st.text_input("Promo Code(Optional)")
    total_price = calculate_total_price(item_to_buy, quantity, promo_code)
    st.write("Total Price: $", total_price)
    payment_option = st.radio("Please select Payment Option", ["Credit Card", "Debit Card", "UPI", "Net Banking"])
    submit_button = st.form_submit_button("Buy Now")



    if submit_button:
        unique_filename = get_unique_filename()
        # con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
        query= (f"""copy (
                        select uuid() as order_id,
                        '{item_to_buy}' as product,
                        {quantity} as quantity,
                        {mobile_number} as mobile_number,
                        '{delivery_location}' as delivery_location,
                        '{promo_code}' as promo_code,
                        {total_price} as total_price,
                        '{payment_option}' as payment_option,
                        CURRENT_TIMESTAMP as created_at
                        ) to 's3://tgt-southdms/g-mart/orders/{unique_filename}'  (FORMAT parquet);
                        """)
        print(query)
        con.execute(query)
        st.write("Payment Successful")
        st.write("Thank you for shopping with us!")
