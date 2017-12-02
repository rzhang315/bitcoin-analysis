from flask import Flask
import datetime
import time
import random
import json
from collections import deque
app = Flask(__name__)

q = deque([])
t = [0]
@app.route('/bitcoin')
def bitcoin():
    if not q:
        for i in range(10):
            d = {}
            d['time_stamp'] = datetime.datetime.now().time().isoformat()
            #d['time_stamp'] = t[0]
            d['price'] = 1000 * random.random()
            q.append(d)
    else:
        q.popleft()
        d = {}
        d['time_stamp'] = datetime.datetime.now().time().isoformat()
        d['price'] = 1000 * random.random()
        q.append(d)
    t[0] += 1
    return json.dumps(list(q))

@app.route('/')
def home_page():

    return "hello world"

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)