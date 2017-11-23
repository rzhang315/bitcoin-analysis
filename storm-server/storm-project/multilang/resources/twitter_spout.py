from storm import Spout, emit, log
from kafka import KafkaConsumer
import os
import json

# Load config file
abs_path = os.path.dirname(os.path.abspath(__file__))
with open('{}/../../../config.json'.format(abs_path)) as json_data_file:
    config = json.load(json_data_file)

# Create Kafka consumer
servers = config['kafka']['servers']
topic = config['kafka']['topic']['twitter']
kafka_consumer = KafkaConsumer(topic, bootstrap_servers=servers)

class TweetSpout(Spout):

    def nextTuple(self):
        # Consume next data from Kafka queue
    	data = consumer.next().value

        # Emit value so bolts down stream can process it
        emit([data])

TweetSpout().run()
