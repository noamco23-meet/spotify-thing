import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session as login_session
#initial app setup

#this is stuff that i got from spotify. kinda like how you open an app in firebase, you can open an app in spotify and this is the config
client_id ="2f3ddb10f2a048e9a4a1cb89ff64697a"
client_secret ="48962f9a9d254800a949de8d2180734b"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                    client_secret=client_secret,
                                                    redirect_uri='http://example.com', 
                                                    scope="user-modify-playback-state user-read-currently-playing")) #these are the scopes needed. basically what things we're allowed to do. in this case, modify the playback state (add to queue, skip song) and read playback state (find current song info)

#class setup

blacklisted_students = []
SONG_SKIP_REQUIREMENT = 1 #this is how many votes you need to skip a song
skip_votes = 0 #

def addStudentToBlacklist(student_name):
    blacklisted_students.append(student_name)

def findCurrentSongInfo():
    current = spotify.currently_playing() #if you want you can print this out. it's a massive dictionary of literally everything it's so hard to read
    if current==None:
        return {"name": "Nothing"}
    current_song = current['item']['name']
    num_of_artists = len(current['item']['artists'])
    print(num_of_artists)
    artists = []
    for i in range(num_of_artists):
        artists.append(current['item']['artists'][i]['name'])
    song_info = {"name": current_song, "artists": artists} #maybe we can add the votes here idk
    print(artists)
    return(song_info)

def addNewSongToQueue(uri):
    if(login_session['name'] not in blacklisted_students):
        added = spotify.add_to_queue(uri) #a uri is basically spotify's link to a song. you can find the url by pressing ctrl while clicking on the share button on a spotify track
        return f"added {added}"
    else:
        return "You've been blacklisted :(\nNext time don't be annoying"

def voteToSkip(): #ok this function is wacko. the skip_votes variable is unaccessible in functions ??? maybe we can make the votes part of the song info
    global skip_votes
    skip_votes+=1
    if (skip_votes == SONG_SKIP_REQUIREMENT):
        skipSong(skip_votes)
    else:
        return f"You need {SONG_SKIP_REQUIREMENT-skip_votes} more votes to skip this song."

def skipSong(skip_votes): #see for some reason the skip_votes isn't accessible :(
    spotify.next_track()
    skip_votes = 0
