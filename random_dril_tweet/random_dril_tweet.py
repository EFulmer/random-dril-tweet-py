from __future__ import print_function

import calendar
import csv
import os.path
import random
import subprocess
import sys
import time


TWEET_FILE_NAME = 'dril.txt'
TWEET_URL_NAME = 'http://greptweet.com/u/dril/dril.txt'


def get_dril_tweets(url, out_file_name):
    """
    'computer fetch me my Posts'
    """
    with open(out_file_name, 'w') as out_file:
        subprocess.call('curl --compressed -s ' + url,
                        shell=True,
                        stdout=out_file)
    

def random_dril_tweet(tweet_file):
    """
    'FURTHER MORe, any future tweet i make may now randomly be 
    designated as a "Hell Tweet", meaning if you reply to it , you will 
    be blocked,'
    """
    # TODO merging tweets that got split across lines
    tweets = []
    with open(tweet_file, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        tweets = [ line[-1] for line in reader
                   if "http://" not in line[-1] ]
    random.shuffle(tweets)
    return tweets[0]


def main():
    """
    'most of my material is never recorded or heard by human ears'
    """
    if not os.path.exists(TWEET_FILE_NAME):
        get_dril_tweets(TWEET_URL_NAME, TWEET_FILE_NAME)
    else:
        file_age = os.path.getmtime(TWEET_FILE_NAME)
        now = calendar.timegm(time.gmtime())
        if now - file_age > 172800: # two days
            get_dril_tweets(TWEET_URL_NAME, TWEET_FILE_NAME)
    print(random_dril_tweet(TWEET_FILE_NAME))
    sys.exit(0)


if __name__ == '__main__':
	main()
