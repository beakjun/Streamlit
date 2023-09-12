import plotly.graph_objects as go

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
        ))
    
# fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "sun"])])
    return fig