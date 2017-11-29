"""
News listener class.

"""
import requests
from kafka import KafkaProducer
import json
import os
import datetime
import time

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

    url = "https://newsapi.org/v2/top-headlines?q="+keywords[0]+"&apiKey="+key
	
    while True:
	
        resp = requests.get(url)
        #print resp
        output = resp.json()['articles']		
 
        output = sorted(output, key=lambda k: (k['publishedAt']), reverse=True)		
        datas = []
		
        #print output
        
        for article in output[0:10]:
            data = {}
            data['source'] = article['source'] 
            data['author'] = article['author'] 
            data['title'] = article['title'] 
            data['description'] = article['description'] 
            data['publishedAt'] = article['publishedAt'] 
            datas.append(data)
            			
        kafka_producer.send(topic, json.dumps(datas))

        print datas
		
        time.sleep(10)
    

if __name__ == '__main__':
    main()
