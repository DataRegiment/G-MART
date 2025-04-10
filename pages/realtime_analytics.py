import streamlit as st
from duckdb_utils import *

con = connect_duckdb()
load_extentions_and_secrets(con)
ANALYTICS_S3 = st.secrets["ANALYTICS_S3"]
visit_data = con.execute(f"select page_name as Page,count(*) as Visits from delta_scan('{ANALYTICS_S3}/visits/') group by all").fetchdf()
st.write("# Page Visits")
st.bar_chart(visit_data, x="Page", y="Visits", use_container_width=True,horizontal=True)

try:
    sum_sales = con.execute(f"select coalesce(sum(total_price),0) from delta_scan('{ANALYTICS_S3}/orders/')").fetchdf()
    sales_data = sum_sales.iloc[0, 0] if sum_sales is not None else 0
    
except Exception as e:
    sales_data = 0
    
st.write("### Total Sales: $", sales_data if sales_data is not None else 0)