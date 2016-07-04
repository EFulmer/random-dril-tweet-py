# -*- coding: utf-8 -*-

"""
'which programming language should I learn if I want to transform myself
into an enormous 3d wireframe head that spits out flashing cubes'
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
from redis import StrictRedis


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
    tweets = []
    with open(tweet_file, 'r') as tweet_file_handle:
        reader = csv.reader(tweet_file_handle, delimiter='|')
        tweets = [line[-1] for line in reader if "http://" not in line[-1]]
    random.shuffle(tweets)
    tweet = tweets[0].replace('dril.txt grep.php lock', '').replace('&amp;', '&')
    return tweet


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
                post = tweet.strip().split('|', 2)[2]

            # there are several lines, apparently from old tweets, that
            # are just fragments of a tweet. I think Twitter changed
            # how newlines are represented in tweets and that has to
            # do with it?
            # anyway they cause ValueErrors when trying to unpack
            # via str.split() above
            except IndexError:
                continue
            in_db = tweets_col.find({'post': post})

            if in_db.count() == 0:
                result = tweets_col.insert_one({'post': post})
                if not result.acknowledged:
                    print('error adding tweet "{}" to MongoDB'.format(post))
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


def add_tweets_to_redis(tweet_file):
    """
    'DVD: FBI WARNING Me: oh boy here we go DVD: The board advises you
    to have lots of fun watching this Hollywood movie Me: Ah.. It's a
    nice one'
    """
    redis_client = StrictRedis(host='localhost', port=6379, db=0)
    with open(tweet_file, 'r') as tweets:
        for line in tweets:
            # again, dealing with weird error here
            try:
                tweet = line.strip().split('|', 2)[2]
                # need to investigate whether one-by-one inserting
                # or building a list of tweets and doing a single insert
                # would be more efficient
                if not redis_client.sismember('tweets', tweet):
                    result = redis_client.sadd('tweets', tweet)
                    if not result:
                        print('error occurred while adding tweet: "{}" to redis'
                              .format(tweet))
                else:
                    break # found all new tweets
            except IndexError:
                continue
    redis_client.save()


def random_dril_tweet_from_redis():
    """
    to counter-act the terrible "ISIS", im starting my own group called
    "NICEis". what we do is give retweets & faves to the
    hopelessly decrepit
    """
    redis_client = StrictRedis(host='localhost', port=6379, db=0)
    tweet = redis_client.srandmember('tweets')
    tweet = tweet.decode('UTF-8')
    return tweet


def update_tweet_file(tweet_file_name, tweet_url):
    """
    'ive heard from a reliable source that people arre putting their
    lips on to my girl friends avatars and going "muah muah muah." cut
    it out'
    """
    file_age = os.path.getmtime(tweet_file_name)
    now = calendar.timegm(time.gmtime())
    if now - file_age > (60 * 60 * 48): # two days
        get_dril_tweets(tweet_url, tweet_file_name)


def main():
    """
    'most of my material is never recorded or heard by human ears'
    """
    if not os.path.exists(TWEET_FILE_NAME):
        get_dril_tweets(TWEET_URL_NAME, TWEET_FILE_NAME)
    else:
        update_tweet_file(TWEET_FILE_NAME, TWEET_URL_NAME)
    if 'mongo' in sys.argv:
        add_tweets_to_mongodb(TWEET_FILE_NAME)
        print(random_dril_tweet_from_mongodb())
    elif 'redis' in sys.argv:
        add_tweets_to_redis(TWEET_FILE_NAME)
        print(random_dril_tweet_from_redis())
    else:
        print(random_dril_tweet(TWEET_FILE_NAME))

    sys.exit(0)


if __name__ == '__main__':
    main()
