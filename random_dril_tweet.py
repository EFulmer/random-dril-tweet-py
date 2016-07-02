# -*- coding: utf-8 -*-

"""
which programming language should I learn if I want to transform myself
into an enormous 3d wireframe head that spits out flashing cubes
"""

from __future__ import print_function

import calendar
import csv
import os.path
import random
import subprocess
import sys
import time

from pymongo import MongoClient


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
    with open(tweet_file, 'r') as tweet_file_handle:
        reader = csv.reader(tweet_file_handle, delimiter='|')
        tweets = [line[-1] for line in reader if "http://" not in line[-1]]
    random.shuffle(tweets)
    return tweets[0]


def add_tweets_to_mongodb(tweet_file):
    """
    'Nuffs aid.  Need I say more? Nuff said. Need I say more?
    Nuff said.  Need i say more?  Nuff said.  Need I say more?
    Nuff said.  Need I say'
    """
    client = MongoClient()
    tweets_col = client.dril_tweets.tweets
    with open(tweet_file, 'r') as tweets:
        for tweet in tweets:
            try:
                post_id, timestamp, post = tweet.strip().split('|', 2)

            # there are several lines, apparently from old tweets, that
            # are just fragments of a tweet. I think Twitter changed
            # how newlines are represented in tweets and that has to
            # do with it?
            # anyway they cause ValueErrors when trying to unpack
            # via str.split() above
            except ValueError:
                pass # TODO better logging
            in_db = tweets_col.find({'post_id': post_id})

            if in_db.count() == 0:
                result = tweets_col.insert_one({'post_id': post_id,
                                               'timestamp': timestamp,
                                               'post': post})
                if not result.acknowledged:
                    pass # TODO better logging
            else:
                break # we've found all the new tweets

    client.close()


def random_dril_tweet_from_mongodb():
    """
    'polease cut all art programs so we can instead focus on teaching
    our children the importance of being Respectful towards influencers'
    """
    client = MongoClient()
    tweets = client.dril_tweets.tweets

    tweet_count = tweets.count() - 1
    which_tweet = random.randint(0, tweet_count)

    cursor = tweets.find()
    tweet = cursor.skip(which_tweet).next()
    client.close()
    return tweet['post']


def main():
    """
    'most of my material is never recorded or heard by human ears'
    """
    if 'mongo' in sys.argv:
        add_tweets_to_mongodb(TWEET_FILE_NAME)
        print(random_dril_tweet_from_mongodb())
    else:
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
