from flask import Flask, render_template, request
from textblob_functions import get_clean_tweets
from vader_functions import get_polarity
import tweepy as tp

from twitter_auth import *

auth = tp.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tp.API(auth)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/textblob', methods=['GET'])
def textblobpage():
    title = 'Data Vis Project 2021'
    desc = 'A chart to viualise sentiment'
    df = get_clean_tweets('bitcoin')

    pos, neg, nue = get_polarity(df)

    labels = ['positive', 'negative', 'neutral']
    values = [pos, neg, nue]

    data = zip(labels, values)

    list_of_data = []

    for label, value in data:
        list_of_data.append({'name': label, 'y': value})

    return render_template('textblob.html', title=title, description_text=desc, chart_name='Pie', data=list_of_data)


@app.route('/vader', methods=['GET'])
def vaderpage():
    #     text = 'oneplus'

    # analyser = SentimentIntensityAnalyzer()
    # blob = TextBlob(text)

    # print('Textblob output', blob.sentiment.polarity)

    # def sentiment_analyser_score(data):
    #     score = analyser.polarity_scores(data)
    #     print("{:-<40} {}".format(data, str(score)))

    # sentiment_analyser_score(text)
    return render_template('vader.html')

@app.route('/tweets', methods=['POST'])
def tweetspage():  # put application's code here

    if request.method == 'POST':
        query = request.form['query']
        tweets = api.search(query)

        return render_template('results.html', query = tweets)

    return render_template('404.html')




if __name__ == '__main__':
    app.run()
