import spotipy
from spotipy.oauth2 import SpotifyOAuth

#initial app setup

client_id ="ba4d34b7c5ee41079ca1f4d291009ab9"
client_secret ="c7c8c045fa6640d5a184c3902d6767ea"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                    client_secret=client_secret,
                                                    redirect_uri='http://example.com',
                                                    scope="user-modify-playback-state user-read-playback-state"))

#class setup

blacklisted_students = []
SONG_SKIP_REQUIREMENT = 1
skip_votes = 0

def addStudentToBlacklist(student_name):
    blacklisted_students.append(student_name)

def findCurrentSongInfo():
    current = spotify.currently_playing()
    current_song = current['item']['name']
    num_of_artists = len(current['item']['artists'])
    print(num_of_artists)
    artists = []
    for i in range(num_of_artists):
        artists.append(current['item']['artists'][i]['name'])
    song_info = {"name": current_song, "artists": artists}
    print(artists)
    return(song_info)

def addNewSongToQueue(uri, student_name):
    if(student_name not in blacklisted_students):
        added = spotify.add_to_queue(uri)
        return added
    else:
        return "You've been blacklisted :(\nNext time don't be annoying"

def voteToSkip():
    global skip_votes
    skip_votes+=1
    if (skip_votes == SONG_SKIP_REQUIREMENT):
        skipSong(skip_votes)
    else:
        return f"You need {SONG_SKIP_REQUIREMENT-skip_votes} more votes to skip this song."

def skipSong(skip_votes):
    spotify.next_track()
    skip_votes = 0
