import streamlit as st
from duckdb_utils import *



st.image("assets\G-Mart.png")
st.subheader("Ganitans Shopping Mart")
con = connect_duckdb()
# create_tables(con)
load_extentions_and_secrets(con)
unique_filename = get_unique_filename()
# con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
S3_BUCKET = st.secrets["BASE_S3"]
con.execute(f"copy (select '/home' as page_name,CURRENT_TIMESTAMP as visit_ts) to '{S3_BUCKET}/page_visits/{unique_filename}'  (FORMAT parquet);")
# user_name = st.text_input("Please enter your name")

# con = duckdb.connect(database=':memory:', read_only=False)
