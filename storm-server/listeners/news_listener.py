"""
News listener class.

"""
import requests
from kafka import KafkaProducer
import json
import os
import datetime
import time
from operator import itemgetter

def main():

    print('News is listening...')

    # Load config file
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open('{}/../config.json'.format(abs_path)) as json_data_file:
        config = json.load(json_data_file)

    # Load Kafka configuration and initialize Kafka producer
    servers = config['kafka']['servers']
    topic = config['kafka']['topic']['news']
    kafka_producer = KafkaProducer(bootstrap_servers=servers)

    # Load NEWS access credentials
    keywords = config['news']['keywords']
    key = config['news']['key']

    url = 'https://newsapi.org/v2/top-headlines?q={kw}&apiKey={key}'.format(kw=keywords[0],key=key)

    while True:
        resp = requests.get(url)
        output = resp.json()['articles']		
        output = sorted(output, key=itemgetter('publishedAt'), reverse=True)		
        
        for article in output[0:10]:
            data = {
                'source': article['source'],
                'author': article['author'],
                'title': article['title'],
                'description': article['description'],
                'publishedAt': article['publishedAt'],
            }
            kafka_producer.send(topic, json.dumps(data))

        time.sleep(10)

if __name__ == '__main__':
    main()
