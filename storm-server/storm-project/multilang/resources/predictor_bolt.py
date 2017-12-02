from datetime import date
import time
import datetime
import boto3
import json
import storm
import os
from kafka import KafkaConsumer
import dateutil.parser
from predict import predict
import numpy as np
from collections import deque
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

LOOK_BACK = 15
FUTURE_OFFSET = 5
MODEL = 'model/model_L15_F5_TR429.157226562_TS303.654984229.h5'
past_prices = deque([], maxlen=LOOK_BACK)

def shift_future(timestamp, shift):
    return (dateutil.parser.parse(timestamp) + datetime.timedelta(seconds=60 * shift)).isoformat()

class DynamoInsertBolt(storm.BasicBolt):
    def process(self, tup):
        # Load data from tuple
        data = tup.values[0]
        data = json.loads(data)


        # Initialize if deque is empty
        if len(past_prices) == 0:
            past_prices.extend([float(data['price'].replace(',', ''))] * LOOK_BACK)

        # Append to rolling deque and compute price
        else:
            past_prices.append(float(data['price'].replace(',', '')))

        # Check if enough elements exist
        if len(past_prices) == LOOK_BACK:

            prediction = predict(MODEL, np.array(past_prices).reshape(1, LOOK_BACK))

            # Store predicted results in DynamoDB
            table = dynamodb.Table(config['dynamodb']['prediction'])
            table.put_item(
                Item = {
                    'timestamp': shift_future(data['timestamp'], FUTURE_OFFSET),
                    'price': Decimal(str(prediction)),
                }
            )
        # Emit for downstream bolts
        storm.emit([data])

DynamoInsertBolt().run()

