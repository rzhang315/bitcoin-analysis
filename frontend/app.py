import dash
import dash_core_components as dcc
from dash.dependencies import Output, Event
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import requests
import json



# current price 

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')
URL = 'http://127.0.0.1:5000'




app.layout = html.Div([ 
    html.Div('Bitcoin Analysis', style={'color': 'black', 'fontSize': 30}),
    dcc.Graph(id='live-update-graph-scatter'),   
    dcc.Graph(id='live-update-sentiment-scatter'), 
    dcc.Interval(
            id='interval-component',
            interval=1*2000 # in milliseconds
    )
])


@app.callback(Output('live-update-sentiment-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_sentiment_scatter():
    # def _get_bitcoin_data():
    #     resp = requests.get('http://127.0.0.1:5000')
    #     json_list = json.loads(resp.text)
    #     x = [data['time_stamp'] for data in json_list]
    #     y = [data['price'] for data in json_list]
    #     print(x)
    #     print(y)
    #     return x, y
    df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')
    figure={
        'data': [
            go.Scatter(
                x=df[df['continent'] == i]['gdp per capita'],
                y=df[df['continent'] == i]['life expectancy'],
                text=df[df['continent'] == i]['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ) for i in df.continent.unique()
        ],
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }
    return figure





@app.callback(Output('live-update-graph-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_scatter():
    def _get_bitcoin_data():
        resp = requests.get(URL + '/bitcoin')
        json_list = json.loads(resp.text)
        x = [data['time_stamp'] for data in json_list]
        y = [data['price'] for data in json_list]
        print(x)
        print(y)
        return x, y
    traces = list()
    x, y = _get_bitcoin_data()
    xtitle = 'time:' + str(x[-1]) + ', price:' + str(y[-1])
    for t in range(1):
        traces.append(go.Scatter(
            x=x,
            y=y,
            name='Scatter {}'.format(t),
            mode= 'lines+markers'
            ))
    layout = go.Layout(
        title='Bitcoin',
        xaxis=dict(
                #range = [x[0], x[-1]],
            title= xtitle,
            titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
        yaxis=dict(
                title='Price (USD)',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
    )
    return {'data': traces, 'layout' : layout}


if __name__ == '__main__':
    app.run_server(debug=True)
