from datetime import date
import time
import datetime
import boto3
import json
import storm
import os
from kafka import KafkaConsumer
from decimal import Decimal
from textblob import TextBlob

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

def get_sentiment_score(title, description):
    return TextBlob(title).sentiment.polarity + TextBlob(description).sentiment.polarity

class NewsInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
        data = json.loads(data)

        # Get today's date
        today = date.today()

        # Analyze data
        sentiment = get_sentiment_score(data['title'], data['description'])

        # Store analyzed results in DynamoDB
        table = dynamodb.Table(config['dynamodb']['news'])
        parsed_data = {
            'date': str(today),
            'timestamp': str(data['publishedAt']),
            'title': data['title'],
            'description': data['description'] if data['description'] != '' else ' ',
            'sentiment': Decimal(str(sentiment))
        }
        table.put_item(Item=parsed_data)

        # Emit for downstream bolts
        storm.emit([{'source': 'news', 'data': parsed_data}])

NewsInsertBolt().run()


