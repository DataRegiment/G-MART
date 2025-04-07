import streamlit as st
from duckdb_utils import *

con = connect_duckdb()
load_extentions_and_secrets(con)

visit_data = con.execute("select page_name as Page,count(*) as Visits from read_parquet('s3://tgt-southdms/g-mart/page_visits/*.parquet') group by all").fetchdf()
st.write("# Page Visits")
st.bar_chart(visit_data, x="Page", y="Visits", use_container_width=True,horizontal=True)

sales_data = con.execute("select sum(total_price) from read_parquet('s3://tgt-southdms/g-mart/orders/*.parquet')").fetchdf()
# st.write(sales_data)
st.write("### Total Sales: $", sales_data.iloc[0, 0])