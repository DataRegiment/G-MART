import duckdb
import streamlit as st
import uuid

def connect_duckdb():
    if 'conn' not in st.session_state:
        st.session_state.conn = duckdb.connect(database=':memory:', read_only=False)
    return st.session_state.conn

# def create_tables(con):
#     con.execute("create table IF NOT EXISTS page_visits(page_name TEXT, visit_ts datetime);")
#     con.execute("create table IF NOT EXISTS clickstream_events(event_type TEXT, visit_ts datetime);")
    # con.execute("""CREATE TABLE IF NOT EXISTS orders (
    #             id UUID PRIMARY KEY  DEFAULT  uuid(),
    #             product VARCHAR,
    #             quantity INTEGER,
    #             mobile_number INTEGER,
    #             delivery_location VARCHAR,
    #             promo_code VARCHAR,
    #             total_price DECIMAL(10, 2),
    #             payment_option VARCHAR,
    #             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    #             );
    #         """)
    
def load_extentions_and_secrets(con):
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    con.execute(f"""
                CREATE OR REPLACE SECRET (
                TYPE s3,
                KEY_ID '{st.secrets["AWS_ACCESS_KEY_ID"]}',
                SECRET '{st.secrets["AWS_SECRET_ACCESS_KEY"]}',
                REGION '{st.secrets["AWS_REGION"]}'
            );
                """)
    try:
        #Caching
        con.execute("INSTALL cache_httpfs from community;")
        con.execute("LOAD cache_httpfs;")
        #Set cache to memory
        con.execute("SET cache_httpfs_type='in_mem';")
    except:
        pass

def get_unique_filename():
    unique_filename = f"{uuid.uuid4()}.parquet"
    return unique_filename