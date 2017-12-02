import subprocess
from multiprocessing import Process

def listener_process(filename):
    subprocess.call(['python', filename])

def main():
    listeners = [
        'tweepy_listener.py',
        'reddit_listener.py',
        'price_listener.py',
        'news_listener.py'
    ]
    processes = [Process(target=listener_process, args=(fname,)) for fname in listeners]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
