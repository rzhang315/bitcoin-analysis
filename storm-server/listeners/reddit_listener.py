"""
Reddit listener class.

"""
import praw
from kafka import KafkaProducer
import json
import os
import time

def main():

    print('Reddit is listening...')

    # Load config file
    abs_path = os.path.dirname(os.path.abspath(__file__))
    with open('{}/../config.json'.format(abs_path)) as json_data_file:
        config = json.load(json_data_file)

    # Load Kafka configuration and initialize Kafka producer
    servers = config['kafka']['servers']
    topic = config['kafka']['topic']['reddit']
    kafka_producer = KafkaProducer(bootstrap_servers=servers)

    # Load NEWS access credentials
    client_id = config['reddit']['client_id']
    client_secret = config['reddit']['client_secret']
    keywords = config['reddit']['keywords']

    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='storm bitcoin listener praw')
   
	
    while True:	
      for k, submission in enumerate(reddit.subreddit(keywords[0]).top(limit=10)):
        submission.comments.replace_more(limit=0)
        submission.comment_sort = 'top'
        submission_dict = {'rank': k,'title': submission.title,	'comments': [top_level_comment.body for top_level_comment in submission.comments][:10]}
         			
        kafka_producer.send(topic, json.dumps(submission_dict))

        print submission_dict
		
        time.sleep(10)
    

if __name__ == '__main__':
    main()
