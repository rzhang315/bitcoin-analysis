from datetime import date
import time
import datetime
import boto3
import json
import storm
import os
from sentiment import compute_sentiment
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

def _get_sentiment_score(title, comments):
    
    sentiment_score = 0
    sentiment_score += TextBlob(title).sentiment.polarity
    sentiment_score += sum(TextBlob(c).sentiment.polarity for c in comments)
    return sentiment_score	

class RedditInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
    	data = json.loads(json.loads(data))

        # Get today's date
        today = date.today()

        # Store analyzed results in DynamoDB
        table = dynamodb.Table("reddit_sentiment")
		
        for sub in data:
          sentiment = get_sentiment_score(sub['rank'], sub['comments'])
		
          table.put_item(
            Item = {
                'date': str(today),
                'timestamp': str(data['timestamp_ms']),
                'text': data['text'],
                'sentiment': Decimal(sentiment)
            }
          )
        # Emit for downstream bolts
        storm.emit([data])

RedditInsertBolt().run()


