import duckdb
import streamlit as st

def connect_duckdb():
    if 'conn' not in st.session_state:
        st.session_state.conn = duckdb.connect(database='my_database.db', read_only=False)
    return st.session_state.conn

def create_tables(con):
    con.execute("CREATE SEQUENCE IF NOT EXISTS event_id_seq START 1;")
    con.execute("create table IF NOT EXISTS page_visits(page_name TEXT, visit_ts datetime);")
    # Create purchase events table if it doesn't exist
    con.execute("""
        CREATE TABLE IF NOT EXISTS purchase_events (
            event_id INTEGER DEFAULT nextval('event_id_seq'),
            item_name TEXT,
            quantity INTEGER,
            mobile_number TEXT,
            total_amount DECIMAL(10,2),
            delivery_location TEXT,
            payment_option TEXT,
            purchase_timestamp TIMESTAMP,
            status TEXT,
            PRIMARY KEY (event_id)
        );
    """)