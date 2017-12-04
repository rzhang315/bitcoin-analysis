from datetime import date
import time
import datetime
import boto3
import json
import storm
import os
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

overall_sentiment = [0.0]

class DynamoInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]

        # Analyze data
        if data['source'] == 'twitter':
            weight = .995
            sentiment = data['data']['sentiment']
            overall_sentiment[0] = overall_sentiment[0] * weight + sentiment * (1 - weight)
        elif data['source'] == 'reddit':
            weight = .85
            sentiment = data['data']['sentiment']
            overall_sentiment[0] = overall_sentiment[0] * weight + sentiment * (1 - weight)
        elif data['source'] == 'news':
            weight = .85
            sentiment = data['data']['sentiment']
            overall_sentiment[0] = overall_sentiment[0] * weight + sentiment * (1 - weight)
 
        # Get today's date
        today = date.today()

        # Store analyzed results in DynamoDB
        table = dynamodb.Table(config['dynamodb']['analysis'])
        table.put_item(
            Item = {
                'date': str(today),
                'timestamp': str(time.time()),
                'sentiment': Decimal(str(overall_sentiment[0]))
            }
        )
        # Emit for downstream bolts
        storm.emit([data])

DynamoInsertBolt().run()


