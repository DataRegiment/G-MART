import streamlit as st
from duckdb_utils import connect_duckdb
import pandas as pd
import numpy

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'San Francisco', 'Chicago', 'Boston']
}

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Display the original DataFrame in Streamlit
st.write("Original DataFrame:")
st.dataframe(df)



# con = connect_duckdb()
# df = con.execute("select * from page_visits;").fetch_arrow_table()
# # df = con.execute("show tables")
# st.dataframe(df)