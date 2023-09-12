import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go

import candlechart


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
                   make_searchlist(),
                   index = 1)

placeholder = st.empty()
@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from airflow.stock_market_tbl where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)
df['basDt'] = pd.to_datetime(df['basDt'], format='%Y%m%d')
df['fltRt']=df['fltRt'].astype(float)
df = df.astype({'clpr':int,'vs':int,'mkp':int,'hipr':int,'lopr':int,'trqu':int,'trPrc':int,'clpr':int,'lstgStCnt':int,'mrktTotAmt':int,})

st.plotly_chart(candlechart.plot_candlestick(df, title = '주식 캔들 차트'))

st.dataframe(df)

placeholder.title(f'{option}')


