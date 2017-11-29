"""
Price listener class.

"""
import requests
from kafka import KafkaProducer
import json
import os
import datetime
import time

def main():

    print('Price is listening...')

    # Load config file
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open('{}/../config.json'.format(abs_path)) as json_data_file:
        config = json.load(json_data_file)

    # Load Kafka configuration and initialize Kafka producer
    servers = config['kafka']['servers']
    topic = config['kafka']['topic']['price']
    kafka_producer = KafkaProducer(bootstrap_servers=servers)

    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
	
    while True:
	
        resp = requests.get(url)
        #print resp
        price = resp.json()['bpi']['USD']['rate']	
        timestamp = resp.json()['time']['updatedISO']	
 
        data = {}
        data['price'] = price 
        data['timestamp'] = timestamp        
            			
        kafka_producer.send(topic, json.dumps(data))

        print data
		
        time.sleep(10)
    

if __name__ == '__main__':
    main()
