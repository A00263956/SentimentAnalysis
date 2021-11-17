import pandas as pd
from matplotlib import pyplot as plt

def get_polarity(tweets):
    return (tweets['sentiment']> .25).sum(), (tweets['sentiment']< -.25).sum(), (tweets['sentiment'].between(-.25, .25)).sum()

def display_graph(p, n , neu):
    labels = ['postitive', 'negative', 'neutral']
    values = [p,n,neu]

    plt.title('Sentiment Analysis')

    plt.pie(values, labels=labels, autopct='%1.1f%%')

    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('output.csv')

    df.set_index('id', inplace=True)

    postitive, negative, neutral = get_polarity(df)

    display_graph(postitive, negative, neutral)

