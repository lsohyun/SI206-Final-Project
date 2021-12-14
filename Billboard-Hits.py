from matplotlib import artist
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3


#gathers the ranks, artists, and song from the site -- returns a list of tuples with rank, artist, song data
def collect_data():
    
    start_url = 'https://www.billboard.com/charts/hot-100/'
    
    r = requests.get(start_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup)
    #print(r.status_code)




    #BELOW FOR SONGS
    #===============================================SONG NAME================================================
    song_list = []
    #soup2 = soup.find_all('h3', id='title-of-a-story')
    songs = soup.find_all('h3', class_="c-title")
    #del soup2['id']

    #</h3>, <h3 class="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only" id="title-of-a-story">
    #Rockin' Around The Christmas Tree
    #</h3>, <h3 class="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only" id="title-of-a-story">
    #Jingle Bell Rock
    #</h3>, <h3 class="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only" id="title-of-a-story">
    #Industry Baby
    #</h3>, <h3 class="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only" id="title-of-a-story">
    #A Holly Jolly Christmas

    desired_list = songs[:104] 
    #actual_list = desired_list[5:]


    for x in range(len(desired_list)):
        if x > 3:
    #while (x > 5) & (x < len(desired_list)):
            #['song1', 'song2', 'song3', 'song4'...]
            song_list.append(songs[x].get_text().strip())

    #print(len(song_list))
    #print(song_list)# change to go into tuple or w.e is needed !!!!!!!!!!!!!!!!
    #======================================================================================ABOVE FOR SONGS




    #=============================================ARTIST NAME BELOW FOR ==========================
    artist_list = []
    #print(songs[4].get_text())  WHAT HELPED ME FIGURE OUT THE ACTUAL LIST OF SONGS

    artists = soup.find_all('span', class_="c-label")
    #artist_list.append(artists[0].get_text().strip())

    desired_list = artists[:835] 
    #print(len(artists))

    for x in range(len(desired_list)):
        if x > 3:   
            artist_list.append(artists[x].get_text().strip()) 

    #new_dict = dict.fromkeys(artist_list)
    keys_to_remove = [ 
    'RE-\nENTRY' ,'NEW', '1', '8', '2', '21', '3', '12',
    '47', '4', '14', '41', '5', '20', '38', '6', '19', '7', '27', '22', '46',
    '9', '10', '25', '11', '30', '23', '13', '15', '40', '16', '-', '17', 
    '18', '28', '24', '51', '26', '29', '31', '32', '33', '34', '35', '36',
    '37', '39', '42', '43', '44', '45', '48', '49', '50', '52', '53', '54', 
    '55', '63', '56', '57', '58', '59', '60', '61', '67', '62', '64', '65', 
    '66', '69', '68', '85', '70', '71', '72', '73', '74', '75', '76', '77', 
    '78', '79', '80', '81', '82', '83', '84', '86', '87', '91', '88', '89', 
    '90', '92', '93', '94', '95', '96', '98', '97', '99', '100']
    #print(artist_list)

    x=0
    while x < 30:
        artist_list.remove("RE-\nENTRY")
        x= x+1
    #print(artist_list)

    #y=0
    #while y < 8:
    artist_list.remove("NEW")  # hardcoding? 
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    artist_list.remove("NEW")
    #print(range(len(artist_list)))
        #y= x+1
    complete_artist_list = artist_list[::8]
    #len(complete_list)
    #print(complete_artist_list)
    #==========================================ARTIST NAME ABOVE==================================




    #=========================================WEEKS ON CHART BELOW================================

    rank_list = []
    #print(songs[4].get_text())  WHAT HELPED ME FIGURE OUT THE ACTUAL LIST OF SONGS

    ranks = soup.find_all('span', class_="c-label")
    #artist_list.append(artists[0].get_text().strip())

    desired_list = ranks[:843] 
    #print(len(artists))

    for x in range(len(desired_list)):
        if x > 6:   
            rank_list.append(ranks[x].get_text().strip()) 

    #print(rank_list)

    x=0
    while x < 30:
        rank_list.remove("RE-\nENTRY")
        x= x+1
    #print(rank_list)

    rank_list.remove("NEW")  # hardcoding? 
    rank_list.remove("NEW")
    rank_list.remove("NEW")
    rank_list.remove("NEW")
    rank_list.remove("NEW")
    rank_list.remove("NEW")
    rank_list.remove("NEW")
    rank_list.remove("NEW")

    #print(rank_list)

    weeks_listed = rank_list[::8]
    #print("==============================")
    #print(weeks_listed)
    #print(len(complete_list))

    #=========================================WEEKS ON CHART BELOW================================



    #=========================================INTO TUPLE======================================
    complete_list_set_w_tuple = []

    for a in range(len(complete_artist_list)):
        name = complete_artist_list[a]  #iterates for index _ and gets the name of artist
        title = song_list[a]            #iterates for index _ and gets the title of song
        weeks = weeks_listed[a]         #iterates for index _ and gets the weeks on chart
        
        ordering = (name, title, weeks)
        complete_list_set_w_tuple.append(ordering)
    #print(complete_list_set_w_tuple)
    return complete_list_set_w_tuple



def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    
#creates table Billboard-100 that will have rank, artist, and song name 
def create_table(cur, conn):
    #creates table "Billboard-100" with labels: Rank, Artist, Song
    #cur.execute('CREATE TABLE IF NOT EXISTS Billboard-100 (Rank INTEGER PRIMARY KEY, Artist TEXT, Song TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Billboard100 (Artist TEXT PRIMARY KEY, song TEXT, weeks_in_chart TEXT)') 
    # CHECK IF INTEGER OR STRING^^^^^^^!!!!!!!!!!!!!!!!!!!!!!!!!!

    conn.commit()

'''
def main_collection_to_table(cur, conn, db_name):

    #EXAMPLE OF EXPECTED LIST TO BE ADDED TO TABLE:
    #[ (rank_num, artist_name, song_name), (rank, artist, song) (rank artist, song) ...]
    billboard_list = collect_data()

    cur, conn = set_up_db(db_name)
    create_table(cur, conn)

    #print(billboard_list)

    #limit = 25

    for row in billboard_list:

        #gets rank, artist, and song per row 
        rank = billboard_list[row][0]
        #test
        print(rank)

        artist = billboard_list[row][1]
        song = billboard_list[row][2]

        #expected to insert the desired data (rank, artist , song) to each row in table
        cur.execute("INSERT INTO Billboard-100(rank, artist, song) VALUES (?, ?, ?)", (rank, artist, song))
        conn.commit()

'''
   
   


# put into visualization document, import, and call function once database is filled in
'''
def bar_visualizations():

# X AXIS: song name 
# Y AXOS: weeks on chart

    return None
'''

def main():


     # TEMPPPPPPPPPPP!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    print(complete_artist_list[0])
    print(song_list[0])
    print(complete_rank_list[0])

    print(complete_artist_list[1])
    print(song_list[1])
    print(complete_rank_list[1])
    '''


    cur, conn = set_up_db('complete_table.db')

    create_table(cur, conn)

    complete_data_set = collect_data()

    #print(complete_data_set)
    #print(range(len(complete_data_set)))

    for row in range(len(complete_data_set)): # (0, 100)  # change to get list from collect_data() , use new list

        #gets rank, artist, and song per row 
        artists = complete_data_set[row][0] #works
        songs = complete_data_set[row][1] #works
        weeks_in_charts = complete_data_set[row][2] #works

        #artist = complete_data_set[row] # doesnt work

        #test
        print(artists)
        print(songs)
        print(weeks_in_charts)
        
        cur.execute("INSERT OR IGNORE INTO Billboard100 (artist, song, weeks_in_chart) VALUES (?, ?, ?)", (artists, songs, weeks_in_charts))
        conn.commit()
    



    #CREATE VISUALIZATION
    #WANT ARTIST ON X AXIS 
    #WEEKS ON Y AXIS 
    #BAR CHART
    #shows popularity of artist for weeks 

    artists_collection = []
    weeks_collection = []

    sorted_artist_collection = []
    sorted_weeks_collection =[]
    
    for i in range(len(complete_data_set)):
        artists_collection.append(complete_data_set[i][0]) #works
        weeks_collection.append(complete_data_set[i][2]) #works
    #print(artists_collection)
    #print(weeks_collection)
    

    #create dictionary with VALUES IN ASCENDING ORDER 
    #create dictionary []
    dict_to_be_sorted = {} 
    for key in artists_collection:
        for value in weeks_collection:
            dict_to_be_sorted[key] = int(value)
            weeks_collection.remove(value)
            break
    #print(dict_to_be_sorted)

    #sort dictionary
    
    sorted_dict = sorted(dict_to_be_sorted.items(), key=lambda x: x[1])
    final_list = list(sorted_dict)
    print(final_list)
    print("========")

    for r in range(len(final_list)):
        sorted_artist_collection.append(final_list[r][0])
        sorted_weeks_collection.append(final_list[r][1])
    print(sorted_artist_collection)
    print(sorted_weeks_collection)
    
    #dict1 = dict_to_be_sorted.items()
    #sorted_dict = sorted(dict1)
    print("==============")
    print(sorted_dict)


    plt.bar(sorted_artist_collection, sorted_weeks_collection)

    plt.xticks(sorted_artist_collection, rotation = 90)
    
    plt.xlabel("ARTIST'S NAME")
    plt.ylabel("WEEKS ON THE CHARTS")
    plt.title("Visualization of Artists' Popularity Throughout Time")
   
    plt.show()




    


if __name__ == "__main__":
    main()
