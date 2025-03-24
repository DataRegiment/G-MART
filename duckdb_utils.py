import duckdb
import streamlit as st

def connect_duckdb():
    if 'conn' not in st.session_state:
        st.session_state.conn = duckdb.connect(database='my_database.db', read_only=False)
    return st.session_state.conn

def create_tables(con):
    con.execute("create table IF NOT EXISTS page_visits(page_name TEXT, visit_ts datetime);")