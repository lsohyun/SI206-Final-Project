from env import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import pandas as pd
import sqlite3


# key of spotipy api
cid = spcid
secret = spsecret

client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)

# define spotipy module
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# get data from playlist_id
def get_play_track(playlist_id):
    # get data from api
    d = sp.playlist(playlist_id)

    # to DataFrame
    z = pd.DataFrame(list(pd.DataFrame(d['tracks']['items'])['track']))

    # get singer name
    z['player'] = pd.DataFrame(list(z.artists.str[0]))['name']

    # final filtter
    final_df = z[['duration_ms', 'id', 'popularity', 'player', 'name']]
    return final_df


# update to DB
def dbUpdate(df):

    # connect db
    conn = sqlite3.connect('twit.sqlite')
    cur = conn.cursor()

    # create table
    cur.execute(
        'CREATE TABLE IF NOT EXISTS track(id TEXT UNIQUE, duration TEXT, popularity INTEGER, player TEXT, name STRING)')

    # insert data to table
    for value in df.values:
        id = value[1]
        duration = value[0]
        popularity = value[2]
        player = value[3]
        name = value[4]

        cur.execute('INSERT OR IGNORE INTO track(id, duration, popularity, player, name) VALUES (?,?,?,?,?)',
                    (id, duration, popularity, player, name))
        conn.commit()

    visualization(df)

def visualization(df):
    import matplotlib.pyplot as plt

    # data frame
    df.columns = ['duration', 'id', 'popularity', 'p', 'n']

    # draw plot
    plt.scatter(df['popularity'], df['duration'].astype('int'))
    plt.xlabel('popularity')
    plt.ylabel('duration')
    plt.xlim(75, 100)
    plt.title("duration_popularity")
    plt.savefig("duration_popularity.png")
    plt.show()

    plt.hist(df['popularity'])
    plt.xlabel('popularity')
    plt.ylabel('counts')
    plt.title('popularity -counts')
    plt.savefig("counts_popularity.png")
    plt.show()
    # The Calculations are Below and added into a new database


# main function
if __name__ == "__main__":

    df = get_play_track('37i9dQZF1DXcBWIGoYBM5M')
    df.to_csv('test.csv')
    dbUpdate(df)
