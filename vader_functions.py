from twitter_auth import *
import tweepy as tp
import re
from common_functions import clean_tweet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

def get_vader_tweets(query):
    auth = tp.OAuthHandler(API_KEY,API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tp.API(auth)

    tweets = {}

    vdr = SentimentIntensityAnalyzer()

    tweets_from_api = api.search_tweets(q=query)

    id = 0

    for tweet in tweets_from_api:
        tweets[id] = {
            'id':id,
            'username':tweet.user.name,
            'text': clean_tweet(tweet.text),
            'sentiment': vdr.polarity_scores(tweet.text)['compound']
        }
        id+=1

    df = pd.DataFrame.from_dict(tweets, orient='index')

    df.set_index('id', inplace=True)

    df.to_csv('output.csv')

    return df