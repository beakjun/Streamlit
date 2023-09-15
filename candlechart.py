import plotly.graph_objects as go
import streamlit as st

def plot_candlestick(data,title=""):
    fig = go.Figure(data=[go.Candlestick(
        x = data['basDt'],
        open=data['mkp'],
        high=data['hipr'],
        low=data['lopr'],
        close=data['clpr']
    )])
    data['MA5'] = data['clpr'].rolling(window=5).mean()
    data['MA20'] = data['clpr'].rolling(window=20).mean()
    data['MA60'] = data['clpr'].rolling(window=60).mean()
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA5'], mode='lines', name='MA-5', line=dict(color='#9d11d0', width=0.7)))
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA20'], mode='lines', name='MA-20', line=dict(color='#dcad04', width=0.7)))
    fig.add_trace(go.Scatter(x=data['basDt'], y=data['MA60'], mode='lines', name='MA-60', line=dict(color='#11d067', width=0.7)))
    fig.update_layout(
        title = '일별 주가',
        title_font_family="맑은고딕",
        title_font_size = 18,
        hoverlabel=dict(
            bgcolor='black',
            font_size=15,
        ),
        hovermode="x unified", 
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
        ),
        width=1200,
        autosize=True)
    
# fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat","mon"])])
    return fig