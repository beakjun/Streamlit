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
cursor=conn.cursor()
title = st.text_input('주식명', '삼성전자')


@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query=f"SELECT * from airflow.stock_market_tbl where \"itmsNm\" like '%{title}%'"
df = run_query(query)
st.dataframe(df)
    