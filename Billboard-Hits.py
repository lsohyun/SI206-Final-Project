from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


#gathers the ranks, artists, and song from the site -- returns a list of tuples with rank, artist, song data
def collect_data():
    #start url for billboard 100
    start_url = 'https://www.billboard.com/charts/hot-100'
    
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #empty list to store tuples w/ info in 
    main_collection = []
    
    #supposed to get the 1st match for ranks/artists/songs in soup, then 2nd, then 3rd as it loops until end
    #for each entry, it puts it into a tuple and then organized into a main collection
    for entry in soup:  # for 1st match in soup(all of billboard 100), put it into specified label
        rank_artist_song_tuple = () # tuple that will hold (rank, artist, and song)
        
        ranks = entry.find_all('span', class_ = 'chart-element__rank__number').get_text()
        rank_artist_song_tuple = rank_artist_song_tuple + ranks
        
        artists = entry.find_all('span', class_ = 'chart-element__information__artist text--truncate color--secondary').get_text()
        rank_artist_song_tuple = rank_artist_song_tuple + artists

        songs = entry.find_all('span', class_= 'chart-element__information__song text--truncate color--primary').get_text()
        rank_artist_song_tuple = rank_artist_song_tuple + songs
        #collects info in a tuple per line and inserts it into main collection
        main_collection.append(rank_artist_song_tuple)

    #print(main_collection)

    #EXAMPLE OF EXPECTED LIST:
    #[(rank_num, artist_name, song_name), (rank, artist, song)...]
    return main_collection


#creates table Billboard-100 that will have rank, artist, and song name 
def create_table(cur, conn):
    #creates table "Billboard-100" with labels: Rank, Artist, Song
    cur.execute('CREATE TABLE IF NOT EXISTS Billboard-100 (Rank INTEGER PRIMARY KEY, Artist TEXT, Song TEXT)')
    conn.commit()


def main_collection_to_table(cur, conn, db_name):
    
    #EXAMPLE OF EXPECTED LIST:
    #[(rank_num, artist_name, song_name), (rank, artist, song)...]
    billboard_list = collect_data()

    cur, conn = set_up_db('billboard.sqlite')
    create_table(cur, conn)

    #print(billboard_list)

    #limit = 25

    for row in billboard_list:

        #gets rank, artist, and song per row 
        rank = billboard_list[row][0]
        artist = billboard_list[row][1]
        song = billboard_list[row][2]

        #expected to insert the desired data (rank, artist , song) to each row in table
        cur.execute("INSERT INTO Billboard-100(rank, artist, song) VALUES (?, ?, ?)", (rank, artist, song))
        conn.commit()


   
   


# put into visualization document, import, and call function once database is filled in
'''
def bar_visualizations():

    return None
'''



'''
def main():






    
if __name__ == "__main__":
    main()

'''