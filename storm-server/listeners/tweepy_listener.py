"""
Tweepy listener class.

Listens to tweets filtered by a keyword,
then publishes the entire tweet data serialized as a string
to a Kafka queue.
"""
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json

# Listener that publishes data to Kafka queue
class KafkaListener(StreamListener):

    def __init__(self, topic, kafka_producer):
        """
        KafkaListener object.

        Args:
            topic (string) : name of topic for Kafka queue
            kafka_producer (KafkaProducer) : producer object to publish data
        """
        self.topic = topic
        self.kafka_producer = kafka_producer

    def on_data(self, data):
        """
        Publish data to Kafka queue.

        Args:
            data (dict) : dictionary item to publish
        """
        self.kafka_producer.send(self.topic, json.dumps(data))
        return True

    def on_error(self, status):
        print(status)

def main():

    print('Tweepy is listening...')

    # Load config file
    with open('../config.json') as json_data_file:
        config = json.load(json_data_file)

    # Load Kafka configuration and initialize Kafka producer
    servers = config['kafka']['servers']
    topic = config['kafka']['topic']
    kafka_producer = KafkaProducer(bootstrap_servers=servers)

    # Load Twitter access credentials
    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']
    consumer_key = config['twitter']['consumer_key']
    consumer_secret = config['twitter']['consumer_secret']

    # Authenticate to Twitter and create stream with KafkaListener as handler
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener=KafkaListener(topic, kafka_producer))

    # Filter stream by keywords
    stream.filter(track=['football'])

if __name__ == '__main__':
    main()
