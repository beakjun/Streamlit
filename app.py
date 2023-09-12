import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import plotly.graph_objects as go



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
st.dataframe(df)

placeholder.title(f'{option}')

def plot_candlestick(data,title=""):
    fig = go.Figure(data=[go.Candlestick(
        x = data['basDt'],
        open=data['mkp'],
        high=data['hipr'],
        low=data['lopr'],
        close=data['clpr']
    )])
    fig.update_layout(
        title = 'asdf',
    #     title= f'{sig_area} 시군구별 {type_nm} 매매(실거래가)/전월세(보증금) 거래량',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
    #         bgcolor='white',
            bgcolor='black',
            font_size=15,
        ),
        hovermode="x unified",
    #     hovermode="x",    
    #     template='plotly_white', 
        template='plotly_dark',
        xaxis_tickangle=90,
        yaxis_tickformat = ',',
        legend = dict(orientation = 'h', xanchor = "center", x = 0.85, y= 1.1), 
        barmode='group'
    )
        
    fig.update_layout(margin=go.layout.Margin(
            l=10, #left margin
            r=10, #right margin
            b=10, #bottom margin
            t=50  #top margin
        ))
    
# fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "sun"])])
    return fig

st.plotly_chart(plot_candlestick(df, title = '주식 캔들 차트'))
