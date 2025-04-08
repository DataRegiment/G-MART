import streamlit as st
from duckdb_utils import *

st.header("Electronics Store")
con = connect_duckdb()
# create_tables(con)
load_extentions_and_secrets(con)
unique_filename = get_unique_filename()
S3_BUCKET = st.secrets["BASE_S3"]
# con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
if 'total_price' not in st.session_state:
    st.session_state.total_price = 0

con.execute(f"copy (select '/products' as page_name,CURRENT_TIMESTAMP as visit_ts) to '{S3_BUCKET}/page_visits/{unique_filename}'  (FORMAT parquet);")

# Define product prices
product_prices = {
    "Macbook Air": 999,
    "PS5": 499,
    "iPhone 14": 799
}

# Define promo codes
promo_codes = {
    "SANDEEP": 0.1,  # 10% off
    "SURYA": 0.2,  # 20% off
    "SHIVA": 0.8,  # 80% off
    "HARI": 0.8,  # 80% off
    "ASHOK": 0.8  # 80% off
}
    
def calculate_total_price(item, quantity, promo_code):
    base_price = 0
    base_price = product_prices[item] * quantity
    # Apply discount if valid promo code
    if promo_code in promo_codes:
        discount = base_price * promo_codes[promo_code]
        return round(base_price - discount, 2)
    return base_price

col1, col2, col3 = st.columns(3, border=True)

with col1:
    # st.image("https://picsum.photos/id/0/5000/3333")
    st.image("assets/M1.jpg")
    st.write("Macbook Air")
    st.write("Price: $999")

with col2:
    st.image("assets/PS5.jpg")
    st.write("PS5")
    st.write("Price: $499")
    
with col3:
    st.image("assets/IP14.jpg")
    st.write("iPhone 14")
    st.write("Price: $759")
  
item_to_buy = st.selectbox("Select an item to buy", list(product_prices.keys()))
quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
mobile_number = st.number_input("Please enter your last 4 digits of mobile number", min_value=0000, max_value=9999)
delivery_location = st.selectbox("Delivery Location", ["Office", "Home", "Other"])
promo_code = st.text_input("Promo Code(Optional)")
# st.session_state.total_price = calculate_total_price(item_to_buy, quantity, promo_code)
current_price = calculate_total_price(item_to_buy, quantity, promo_code.upper())
st.write(f"Item Price: ${product_prices[item_to_buy]}")
st.write(f"Total Price: ${current_price}")
payment_option = st.radio("Please select Payment Option", ["Credit Card", "Debit Card", "UPI", "Net Banking"])


if st.button("Buy Now"):
    unique_filename = get_unique_filename()
    # con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
    query= (f"""copy (
                    select uuid() as order_id,
                    '{item_to_buy}' as product,
                    {quantity} as quantity,
                    {mobile_number} as mobile_number,
                    '{delivery_location}' as delivery_location,
                    '{promo_code}' as promo_code,
                    {current_price} as total_price,
                    '{payment_option}' as payment_option,
                    CURRENT_TIMESTAMP as created_at
                    ) to '{S3_BUCKET}/orders/{unique_filename}'  (FORMAT parquet);
                    """)
    print(query)
    con.execute(query)
    st.write("Payment Successful")
    st.write("Thank you for shopping with us!")

