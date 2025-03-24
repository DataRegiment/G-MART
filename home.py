import streamlit as st
import duckdb

st.header("Welcome to G-MART")
# user_name = st.text_input("Please enter your name")

con = duckdb.connect(database=':memory:', read_only=False)
