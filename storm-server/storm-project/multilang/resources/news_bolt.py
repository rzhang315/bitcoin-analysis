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

def analyzeData(data):
    """
    Analyze Twitter data.

    Args:
        data (dict) : Twitter data dictionary

    Returns:
        analyzed data
    """
    return compute_sentiment(data)

class NewsInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
    	data = json.loads(json.loads(data))

        # Get today's date
        today = date.today()

        # Analyze data
        sentiment = analyzeData(data)

        # Store analyzed results in DynamoDB
        table = dynamodb.Table("news_sentiment")
        table.put_item(
            Item = {
                'date': str(today),
                'timestamp': str(data['publishedAt']),
                'text': data['title'],
                'sentiment': Decimal(sentiment)
            }
        )
        # Emit for downstream bolts
        storm.emit([data])

NewsInsertBolt().run()


