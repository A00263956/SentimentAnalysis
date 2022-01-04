from twitter_auth import *
from common_functions import clean_tweet
import tweepy as tp
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


def get_tb_tweets(query):
    auth = tp.OAuthHandler(API_KEY,API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tp.API(auth)
    tweets = {}
    tweets_from_api = api.search_tweets(q=query)
    id = 0

    for tweet in tweets_from_api:
        tweets[id] = {
            'id':id,
            'username':tweet.user.name,
            'text': clean_tweet(tweet.text),
            'sentiment': TextBlob(tweet.text).sentiment.polarity
        }
        id+=1

    df = pd.DataFrame.from_dict(tweets, orient='index')

    df.set_index('id', inplace=True)

    df.to_csv('output.csv')

    return df
