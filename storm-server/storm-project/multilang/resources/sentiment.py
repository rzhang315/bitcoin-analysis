import json
import re

# Load sentiment dictionary
TERMS={}
with open('AFINN-111.txt') as file:
    sent_lines = file.readlines()
for line in sent_lines:
    s = line.split("\t")
    TERMS[s[0]] = s[1]

def compute_sentiment(tweet):
    """
    Compute sentiment of tweet.

    Args:
        tweet (string) : Tweet text

    Returns:
        sentiment as floating point number
    """
    sentiment=0.0
    if 'text' in tweet:
        text = tweet['text']
        text=re.sub('[!@#$)(*<>=+/:;&^%#|\{},.?~`]', '', text)
        splitTweet=text.split()

        for word in splitTweet:
            if TERMS.has_key(word):
                sentiment = sentiment+ float(TERMS[word])

    return sentiment


