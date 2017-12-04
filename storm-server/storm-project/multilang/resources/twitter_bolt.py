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

def get_sentiment_score(text):
    return TextBlob(text).sentiment.polarity

class TwitterInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
        data = json.loads(json.loads(data))

        # Get today's date
        today = date.today()

        # Analyze data
        sentiment = get_sentiment_score(data['text'])

        # Store analyzed results in DynamoDB
        table = dynamodb.Table(config['dynamodb']['twitter'])
        parsed_data = {
            'date': str(today),
            'timestamp': str(data['timestamp_ms']),
            'hashtags': [ht['text'] for ht in data['entities']['hashtags']],
            'text': data['text'],
            'sentiment': Decimal(str(sentiment))
        }
        table.put_item(Item=parsed_data)

        # Emit for downstream bolts
        storm.emit([{'source': 'twitter', 'data': parsed_data}])

TwitterInsertBolt().run()


