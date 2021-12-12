import time
import datetime
import tweepy
import pandas as pd
from env import *
import sqlite3
import matplotlib.pyplot as plt


# define twitter data
auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
auth.set_access_token(twitter_access_token, twitter_access_secret)

api = tweepy.API(auth)


# get data from spotify table
def get_data_from_db():
    con = sqlite3.connect("spotify.sqlite")
    cursor = con.cursor()

    # get all data
    cursor.execute("select * from track")
    rows = cursor.fetchall()

    # to dataframe
    df = pd.DataFrame(rows)
    df.columns = ['id', 'duration', 'pop', 'name', 'title']
    cursor.close()
    con.close()

    return df


# twiter data get by api
def get_data(df):
    conn = sqlite3.connect('twit.sqlite')
    cur = conn.cursor()

    # create twit table
    cur.execute(
        'CREATE TABLE IF NOT EXISTS twit(id TEXT UNIQUE, main TEXT, time TEXT,keyword TEXT)')

    # get data and insert from each sing
    for value in df[['name', 'title']].values:

        # define keyword
        data = str(value[0])+' '+str(value[1])

        # remove retweets
        keyword = f'{data} -filter:retweets'
        result = []

        # only get 10 data because Limit of api
        tweets = api.search(q=keyword, lang='en', count=10)

        # fillter data
        for tweet in tweets:
            result.append([tweet.id_str, tweet.text,
                           tweet.created_at, tweet.user._json['location']])

        # to dataframe
        df = pd.DataFrame(result)
        df.columns = ['id', 'main', 'time', 'nation']

        # insert
        for dfv in df.values:
            id = str(dfv[0])
            main = str(dfv[1])
            time = str(dfv[2])

            cur.execute('INSERT OR IGNORE INTO twit(id, main, time,keyword) VALUES (?,?,?,?)',
                        (id, main, time, data))
            conn.commit()


# visualization
def visualization():

    # get data from twit
    con = sqlite3.connect("twit.sqlite")
    cursor = con.cursor()

    cursor.execute("select * from twit")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows)

    # calculate time delta
    df.columns = ['id', 'main', 'time', 'keyword']
    df['time'] = pd.to_datetime(df['time'])
    t = (df.groupby(['keyword']).max()['time'] -
         df.groupby(['keyword']).min()['time']).to_frame().reset_index()

    # second to hours
    t['hoursdelta'] = t['time'].dt.seconds/3600

    # get data from spotifyDB
    con2 = sqlite3.connect("spotify.sqlite")
    cursor = con2.cursor()
    cursor.execute("select * from track")
    rows = cursor.fetchall()

    df = pd.DataFrame(rows)
    df.columns = ['id', 'duration', 'popurarity', 'name', 'title']
    df['keyword'] = df['name'].astype('str') + ' '+df['title'].astype('str')

    # merge 2 dataframe
    m = pd.merge(df[['popurarity', 'keyword']], t)

    # draw
    plt.scatter(m.popurarity, m.hoursdelta)
    plt.xlabel('popurarity')
    plt.ylabel('twitter timedelta (hours)')
    plt.xlim(75, 100)
    plt.title("popularity_twiter_timedelay")
    plt.savefig("image.png")
    plt.show()

    plt.hist(m.hoursdelta)
    plt.xlabel('delta hist')
    plt.ylabel('counts')
    plt.title("delta hist")
    plt.savefig("delta_hist.png")
    plt.show()


if __name__ == "__main__":

    df = get_data_from_db()
    get_data(df)
    visualization()
