'''
Using the tweepy api to obtain twitter data. (Since our account is a free
account, there are limits on how many requests we have per months and how many
data we can obtain.)
'''

import os
import tweepy as tw
import pandas as pd
import csv
import datetime

consumer_key = 'RO3nHei9oHbPH5reh2pUDxsnv'
consumer_secret = '9Yzw2JMJS0UQRSvVSiHvgneAj2QzAh6C6a87SoeePgx1Qv3cdR'
access_token = '1230947381992206343-S0ncT5Uk8lfRXbqCMQH2OWcsTTn6Y8'
access_token_secret = 'tQrxTsMnzn6q6Ubgng62EdHg4K5f1aiUaX36Ez6SF5Mu8'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

def search_tweets(search_words):
    '''
    Using the search word to find tweets from Twitter and write them in a csv 
    file.

    Inputs: 
    search_words: the keyword that we want the tweets to contain
    '''

    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       ).items()
    with open('metoo.csv', mode='w') as metoo_tweets:
        tweets_writer = csv.writer(
        metoo_tweets, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tweets_writer.writerow(
            ["search_words: " + str(search_words)])
        tweets_writer.writerow(
            ['Created_at', 'Tweet_Content'])
        for tweet in tweets:
            tweets_writer.writerow(
                [tweet.created_at, tweet.text])
        print("SEARCH COMPLETED")

    return None
