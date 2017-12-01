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

class PriceInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple ex:{'timestamp': u'2017-12-01T17:24:00+00:00', 'price': u'10,529.7513'}
        data = tup.values		
    	data = json.loads(json.loads(data))  
        print data
		
        # Store analyzed results in DynamoDB
        table = dynamodb.Table("bitcoin_price")
        table.put_item(
            Item = data
        )
        # Emit for downstream bolts
        storm.emit(data)

PriceInsertBolt().run()


