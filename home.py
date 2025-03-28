import streamlit as st
from duckdb_utils import *


st.header("Welcome to G-MART")
con = connect_duckdb()
create_tables(con)
load_extentions_and_secrets(con)
unique_filename = get_unique_filename()
# con.execute("insert into page_visits values('/products', CURRENT_TIMESTAMP);")
con.execute(f"copy (select '/home' as page_name,CURRENT_TIMESTAMP as visit_ts) to 's3://tgt-southdms/g-mart/page_visits/{unique_filename}'  (FORMAT parquet);")
# user_name = st.text_input("Please enter your name")

# con = duckdb.connect(database=':memory:', read_only=False)
