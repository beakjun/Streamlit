import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
from streamlit_searchbox import st_searchbox
st.title('Postgres Connection Test')
### Postgres 연결


@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
def make_searchlist():
    query='select distinct "itmsNm","srtnCd" from airflow.stock_market_tbl order by "srtnCd"'
    df=pd.read_sql_query(query,con=conn)
    df['new']=df['itmsNm']+'  '+df['srtnCd']
    return list(df['new'])

option = st.selectbox('종목을 선택하세요',
                   make_searchlist())

@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from airflow.stock_market_tbl where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)
if len(df)>0 :
    st.dataframe(df)
else:
    st.write("해당 키워드는 검색되지 않습니다.")



    