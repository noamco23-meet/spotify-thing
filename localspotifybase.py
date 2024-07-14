import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyOAuth
import pyrebase
import time
import json

firebaseConfig = {
  "apiKey": "AIzaSyCRj8D8wEQ7wf4u2QHMxtQ12cJZSBx0yZI",
  "authDomain": "spotify-thing-3d02e.firebaseapp.com",
  "databaseURL": "https://spotify-thing-3d02e-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "spotify-thing-3d02e",
  "storageBucket": "spotify-thing-3d02e.appspot.com",
  "messagingSenderId": "1072909622967",
  "appId": "1:1072909622967:web:0daa7d2c3ce1795da87732",
  "measurementId": "G-H1XGBRX5TV",
  "databaseURL": "https://spotify-thing-3d02e-default-rtdb.europe-west1.firebasedatabase.app/"
}


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()



CLIENT_ID ="2f3ddb10f2a048e9a4a1cb89ff64697a"
CLIENT_SECRET ="48962f9a9d254800a949de8d2180734b"
REDIRECT_URI = "http://example.com"

scope = "user-modify-playback-state user-read-currently-playing user-read-playback-state" 
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = REDIRECT_URI,
        scope=scope))

def dictsToSets(d):
    return frozenset(d.items())

def dictListsToSets(lst):
    return {dictsToSets(d) for d in lst}

def find_difference(list1, list2):
    set1 = dictListsToSets(list1)
    set2 = dictListsToSets(list2)
    
    difference = set1.difference(set2)
    
    return [s for s in difference]

def updateCurrent():
  current = sp.currently_playing() #if you want you can print this out. it's a massive dictionary of literally everything it's so hard to read
  if current==None:
      print("no song")
      return
  current_uri = current['item']['uri']
  db_info = json.loads(json.dumps(db.child("current").get().val()))
  prev_info = json.loads(json.dumps(db.child("previous").get().val()))
  if prev_info != None:
     prev_uri = next(iter(prev_info))
  else:
     prev_uri = ""
  if db_info == None:
     print("None")
     db.child("current").child("spotify:track:1Pai6r7aZUkrP57WoGNVtp").set({"timestamp": {".sv": "timestamp"}, "votes": 0})
  else:
    db_uri = next(iter(db_info))
    if db_uri == None or current_uri != db_uri: #if database current is different from spotify current
      print(f"db and current differ. db {db_uri} current {current_uri}")
      first = db.child("queue").order_by_child("timestamp").limit_to_first(1).get().val()
      first = json.loads(json.dumps(first))
      if first != None:
        first_uri = next(iter(first))
        print("current song " + current_uri)
        print("first in queue" + first_uri + " " + sp.track(first_uri)['name'])
      if first==current_uri: #if first in queue is the one that is playing
        print("first in line is playing")
        db.child("current").child(current_uri).set(first)
        db.child("queue").child(current_uri).remove()
      elif prev_uri == current_uri:
         print("a song has been voted out. skipping...")
         sp.next_track()
      else:
        print("other song is playing")
        db.child("current").remove()
        db.child("current").child(current_uri).set({"timestamp": {".sv": "timestamp"}, "votes": 0})
    else: 
      print("same song")


def updateQueue():
  queue = sp.queue()
  spotify_uris = []
  for track in queue['queue']:
    spotify_uris.append(track['uri'])
  db_queue = db.child("queue").get().val()
  if db_queue != None:
    db_queue = json.loads(json.dumps(db_queue))
    db_uris = []
    for song in db_queue:
      db_uris.append(song)
    print(f" firebase queue : {db_uris}")
    print(f"spotify queue {len(spotify_uris)}")
    not_in_queue = list(set(db_uris).difference(spotify_uris))
    print(f"not in queue: {not_in_queue}")
    for track in not_in_queue:
      sp.add_to_queue(track)

def checkFull():
  queue = sp.queue()
  queue = sp.queue()
  spotify_uris = []
  for track in queue['queue']:
    spotify_uris.append(sp.track(track['uri'])['name'])
  print(spotify_uris)
  # print(f"length of queue: {len(spotify_uris)}")
  return len(spotify_uris) >=20


while True:
  updateCurrent()
  updateQueue()
  if checkFull() == True:
     db.update({"isFull": 1})
  else:
     db.update({"isFull": 0})
  time.sleep(15)