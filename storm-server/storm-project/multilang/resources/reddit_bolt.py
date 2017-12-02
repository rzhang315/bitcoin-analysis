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

def get_sentiment_score(title, comments, rank):
    
    sentiment_score = 0
    sentiment_score += TextBlob(title).sentiment.polarity
    sentiment_score += sum(TextBlob(c).sentiment.polarity for c in comments)
    return sentiment_score * (.95 ** (rank - 1))

class RedditInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
    	data = json.loads(data)

        # Get today's date
        today = date.today()

        # Store analyzed results in DynamoDB
        table = dynamodb.Table(config['dynamodb']['reddit'])
        
        sentiment = get_sentiment_score(data['title'], data['comments'], data['rank'])
        parsed_data = {
            'date': str(today),
            'sentiment': Decimal(str(sentiment)),
            'rank': data['rank'],
            'title': data['title'],
            'comments': data['comments']
        }
        table.put_item(Item=parsed_data)

        # Emit for downstream bolts
        storm.emit([{'source': 'reddit', 'data': parsed_data}])

RedditInsertBolt().run()


