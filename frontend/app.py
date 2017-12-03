import dash
import dash_core_components as dcc
from dash.dependencies import Output, Event
import dash_html_components as html
import plotly.graph_objs as go
import json
import boto3
import datetime
from boto3.dynamodb.conditions import Key, Attr
import scipy.linalg as la

app = dash.Dash()

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


tweet_sentiment = dynamodb.Table(
    config['dynamodb']['twitter']
)
news_sentiment = dynamodb.Table(
    config['dynamodb']['news']
)
reddit_sentiment = dynamodb.Table(
    config['dynamodb']['reddit']
)

bitcoin_analysis = dynamodb.Table(
    config['dynamodb']['analysis']
)
bitcoin_price = dynamodb.Table(
    config['dynamodb']['price']
)
bitcoin_price_prediction = dynamodb.Table(
    config['dynamodb']['prediction']
)


app.layout = html.Div([

    html.Div('Bitcoin Analysis', style={'color': 'black', 'fontSize': 30}),
    dcc.Graph(id='live-update-graph-scatter'),
    dcc.Graph(id='live-update-sentiment-scatter'),
    dcc.Interval(
        id='interval-component',
        interval=1 * 2000  # in milliseconds 2 secs in this app
    ),

])



@app.callback(Output('live-update-sentiment-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_sentiment_scatter():

    def _get_bitcoin_analysis_data():
        response = bitcoin_analysis.scan(
            Key('date')
        )
        items = response['Items']
        # 'date': str(today),
        # 'timestamp': str(data['timestamp_ms']),
        # 'hashtags': [ht['text'] for ht in data['entities']['hashtags']],
        # 'text': data['text'],
        # 'sentiment': Decimal(str(sentiment))
        date = []
        timestamp = []
        sentiment = []
        text = []
        for i, item in enumerate(items):
            if i > LIMIT:
                break
            t = datetime.datetime.fromtimestamp(
                round(float(item["timestamp"])))
            date.append(t)
            sentiment.append(float(item["sentiment"]))
            text.append(item["date"])
        # might sorted with dynamo db api
        sentiment =  [number/la.norm(sentiment) for number in sentiment]
        return [list(x) for x in zip(
            *sorted(zip(date, sentiment, text), key=lambda pair: pair[0]))]

    def _get_tweet_sentiment_data():
        response = tweet_sentiment.scan(
            Key('date'),
        )
        items = response['Items']
        # 'date': str(today),
        # 'timestamp': str(data['timestamp_ms']),
        # 'hashtags': [ht['text'] for ht in data['entities']['hashtags']],
        # 'text': data['text'],
        # 'sentiment': Decimal(str(sentiment))
        date = []
        timestamp = []
        hashtags = []
        text = []
        sentiment = []
        for i, item in enumerate(items):
            if i > LIMIT:
                break
            t = datetime.datetime.fromtimestamp(int(item["timestamp"]) / 1e3)
            date.append(t)
            sentiment.append(float(item["sentiment"]))
            text.append(item["text"])
        # might sorted with dynamo db api

        sentiment =  [number/la.norm(sentiment) for number in sentiment]
        return [list(x) for x in zip(
            *sorted(zip(date, sentiment, text), key=lambda pair: pair[0]))]

    def _get_news_sentiment_data():
        response = news_sentiment.scan(
            Key('date')
        )
        items = response['Items']
        # 'date': str(today),
        # 'timestamp': str(data['publishedAt']),
        # 'title': data['title'],
        # 'description': data['description'] if data['description'] != '' else ' ',
        # 'sentiment': Decimal(str(sentiment))
        date = []
        timestamp = []
        title = []
        description = []
        sentiment = []
        for i, item in enumerate(items):
            if i > LIMIT:
                break
            date.append(item["timestamp"])
            sentiment.append(float(item["sentiment"]))
            title.append(item["title"])
        # might sorted with dynamo db api

        sentiment =  [number/la.norm(sentiment) for number in sentiment]
        return [list(x) for x in zip(
            *sorted(zip(date, sentiment, title), key=lambda pair: pair[0]))]

    def _get_reddit_sentiment_data():
        response = reddit_sentiment.scan(
            Key('date')
        )
        items = response['Items']
        # 'date': str(today),
        # 'sentiment': Decimal(str(sentiment)),
        # 'rank': data['rank'],
        # 'title': data['title'],
        # 'comments': data['comments']
        date = []
        sentiment = []
        rank = []
        title = []
        comments = []
        for i, item in enumerate(items):
            if i > LIMIT:
                break
            date.append(item["date"])
            sentiment.append(float(item["sentiment"]))
            title.append(item["title"])
        # might sorted with dynamo db api
        sentiment =  [number/la.norm(sentiment) for number in sentiment]
        return [list(x) for x in zip(
            *sorted(zip(date, sentiment, title), key=lambda pair: pair[0]))]

    LIMIT = 20

    tweet_date, tweet_sentiment_score, tweet_text = _get_tweet_sentiment_data()
    news_date, news_sentiment_score, news_text = _get_news_sentiment_data()
    reddit_date, reddit_sentiment_score, reddit_text = _get_reddit_sentiment_data()
    bitcoin_date, bitcoin_sentiment_score, bitcoin_text = _get_bitcoin_analysis_data()

    name_data = [
        'tweet',
        'news',
        'reddit',
        'bitcoin',
    ]

    sentiment_data = [
        tweet_sentiment_score,
        news_sentiment_score,
        reddit_sentiment_score,
        bitcoin_sentiment_score,
    ]

    date_data = [
        tweet_date,
        news_date,
        reddit_date,
        bitcoin_date,
    ]

    text_data = [
        tweet_text,
        news_text,
        reddit_text,
        bitcoin_text
    ]

    figure = {
        'data': [
            go.Scatter(

                x=date_data[i],
                y=sentiment_data[i],
                text=text_data[i],
                name=name_data[i],

                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
            ) for i in range(len(date_data))
        ],
        'layout': go.Layout(
            xaxis={'title': 'time'},
            yaxis={'title': 'sentiment scode (-1,1)'},
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
        return [list(x) for x in zip(
            *sorted(zip(db_time, db_price), key=lambda pair: pair[0]))]

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
        return [list(x) for x in zip(
            *sorted(zip(db_time, db_price), key=lambda pair: pair[0]))]

    traces = list()
    name = ['real', 'predict']
    real_time, real_price = _get_bitcoin_price_data()
    predict_time, predict_price = _get_bitcoin_prediction_data()
    time = [real_time, predict_time]
    price = [real_price, predict_price]
    xtitle = 'time:' + str(real_time[-1]) + ', price:' + str(real_price[-1])
    for t in range(2):
        traces.append(go.Scatter(
            x=time[t],
            y=price[t],
            name=name[t],
            mode='lines+markers'
        ))
    layout = go.Layout(
        title='Bitcoin',
        xaxis=dict(
            #range = [x[0], x[-1]],
            title=xtitle,
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
    return {'data': traces, 'layout': layout}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80)

