import dash
import dash_core_components as dcc
from dash.dependencies import Output, Event
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import requests
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

app = dash.Dash()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

# Load config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# Connect to DynamoDB
access_key = config['aws']['access_key']
secret_key = config['aws']['secret_key']
region = config['aws']['region']
dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region)

# connect the 


tweet_sentiment = dynamodb.Table('tweet_sentiment')
news_sentiment = dynamodb.Table('news_sentiment')
reddit_sentiment = dynamodb.Table('reddit_sentiment')

bitcoin_analysis = dynamodb.Table('bitcoin_analysis')
bitcoin_price = dynamodb.Table('bitcoin_price')
bitcoin_price_prediction = dynamodb.Table('bitcoin_price_prediction')




app.layout = html.Div([ 
    html.Div('Bitcoin Analysis', style={'color': 'black', 'fontSize': 30}),
    dcc.Graph(id='live-update-graph-scatter'),   
    dcc.Graph(id='live-update-sentiment-scatter'), 
    dcc.Interval(
            id='interval-component',
            interval=1*60000 # in milliseconds 60 secs in this app
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

    def _get_bitcoin_price_data():
        response = bitcoin_price.scan(
            Key('timestamp')
        )
        items = response['Items']
        db_time = []
        db_price = []
        for item in items:
            db_time.append(item["timestamp"])
            db_price.append(float(item["price"]))
        # might sorted with dynamo db api
        return [list(x) for x in zip(*sorted(zip(db_time, db_price), key=lambda pair: pair[0]))]


    def _get_bitcoin_prediction_data():
        response = bitcoin_price_prediction.scan(
            Key('timestamp')
        )
        items = response['Items']
        db_time = []
        db_price = []
        for item in items:
            db_time.append(item["timestamp"])
            db_price.append(float(item["price"]))
        # might sorted with dynamo db api
        return [list(x) for x in zip(*sorted(zip(db_time, db_price), key=lambda pair: pair[0]))]

    traces = list()
    name = ['real', 'predict']
    real_time, real_price= _get_bitcoin_price_data()
    predict_time, predict_price= _get_bitcoin_prediction_data()
    time = [real_time, predict_time]
    price = [real_price, predict_price]
    xtitle = 'time:' + str(real_time[-1]) c+ ', price:' + str(real_price[-1])
    for t in range(2):
        traces.append(go.Scatter(
            x=time[t],
            y=price[t],
            name=name[t],
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
    app.run_server(host='127.0.0.1',port=80,debug=True)
