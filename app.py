import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
st.title('Postgres Connection Test')
### Postgres 연결


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
rows = run_query("SELECT * from airflow.stock_market_tbl limit 50")

for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
#이제 포스트레 테스트 완료
    