#! python
# -*- coding: utf8 -*-
import re
from collections import Counter
import tweepy


# Get Twitter access : https://apps.twitter.com/app/new
nunber_tweets = 200 # Number of tweet analyze
twitter_account = "TWITTER ACCOUNT NAME OR ID TO EXTRACT HASHTAG"
consumer_key = "YOUR CONSUMER KEY"
consumer_secret = "YOUR CONSUMER SECRET"
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR ACCESS TOKEN SECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def get_last_tweets(user, nb=nunber_tweets, max_id=None, last_tweets=None):
    if last_tweets is None:
        last_tweets = []

    tweets = api.user_timeline(user, count=200, max_id=max_id)

    last_tweets.extend(tweets)

    if len(last_tweets) >= nb or len(tweets) == 0:
        return last_tweets[:nb]

    return get_last_tweets(user, nb, max_id=last_tweets[-1].id - 1, last_tweets=last_tweets)


def get_words(text):
    regex_word = r'(#\w\w+)'
    text = text.lower()
    words = re.findall(regex_word, text)
    return words


def getKey(item):
    return item[1]


last_tweets = get_last_tweets(twitter_account)
text_tweets = [t.text for t in last_tweets]
words_tweets = sum([get_words(text) for text in text_tweets], [])
words_tweets_count = Counter(words_tweets)

with open("hashtag_from_"+twitter_account+".txt", "a") as log:
    c = words_tweets_count.items()
    c.sort(reverse=True, key=getKey)
    for hashtag in c:
        log.write("%s %s\n" % (hashtag[0], hashtag[1]))
