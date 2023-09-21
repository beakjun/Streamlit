import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go

import candlechart
from TechnicalIndicators import TechnicalIndicators





### Postgres 연결

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# 검색 셀레트 박스에 들어가는 리스트 생성
def make_searchlist():
    query='select distinct "itmsNm","srtnCd" from airflow.stock_market_tbl order by "srtnCd"'
    df=pd.read_sql_query(query,con=conn)
    df['new']=df['itmsNm']+'  '+df['srtnCd']
    return list(df['new'])



# 검색 셀렉트 박스 & 보조지표 멀티박스
placeholder = st.empty()
col1, col2 = st.columns(2)
with col1 :
    option = st.selectbox('종목을 선택하세요',
                   make_searchlist(),
                   index = 1)


with col2 : 
    st.write("")
    with st.expander("보조 지표 선택"):
        bojo = st.multiselect("보조 지표",["MACD","RSI","모멘텀"])


### 검색 결과 데이터 프레임 생성 
@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_sql_query(query,con=conn)
    return df
query2=f"SELECT * from airflow.stock_market_tbl where \"itmsNm\" = '{option[:-8]}' order by \"basDt\" "
df = run_query(query2)

### class 호출
indicators = TechnicalIndicators(df)
indicators.preprocess_data()
main_df=indicators.df.copy()

indicators.compute_macd()
macd_df=indicators.df

indicators.compute_rsi()
rsi_df=indicators.df

placeholder1 = st.empty()


datelist=sorted(list(main_df['basDt']))

if 'select_slider' not in st.session_state:
    st.session_state.slider_value=(min(datelist),max(datelist))

start_date, end_date = st.select_slider(
    'Select a range of Date',
    options=datelist,
    value=st.session_state.slider_value
)

st.session_state.slider_value = (start_date,end_date)

st.write(st.session_state) ### 공부좀 해야될듯

placeholder1.plotly_chart(candlechart.plot_candlestick(main_df, title = '주식 캔들 차트'))

if 'MACD' in bojo:
    st.write('Show MACD Chart')
if 'RSI' in bojo:
    st.write('Show RSI Chart')

st.dataframe(main_df.sort_values(by='basDt', ascending = False).head(20))


placeholder.title(f'{option}')


