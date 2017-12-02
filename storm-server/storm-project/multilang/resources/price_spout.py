from storm import Spout, emit, log
from kafka import KafkaConsumer
import os
import json

# Load config file
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# Create Kafka consumer
servers = config['kafka']['servers']
topic = config['kafka']['topic']['price']
kafka_consumer = KafkaConsumer(topic, bootstrap_servers=servers)

class PriceSpout(Spout):

    def nextTuple(self):
        # Consume next data from Kafka queue
        data = kafka_consumer.next().value

        # Emit value so bolts down stream can process it
        emit([data])

PriceSpout().run()
