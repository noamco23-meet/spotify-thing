from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID ="2f3ddb10f2a048e9a4a1cb89ff64697a"
CLIENT_SECRET ="48962f9a9d254800a949de8d2180734b"
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

SONG_SKIP_REQUIREMENT=1


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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def fetchCurrent():
    current = db.child("current").get().val()
    db_info = json.loads(json.dumps(current))
    if db_info == None:
        print("EMPTYYYYYYYYYYYYY")
        uri = {"name": 0, "votes":0}
        return uri
    
    uri = next(iter(db_info))
    return uri
  

def toggleVote():
    print("toggling vote")
    current = json.loads(json.dumps(db.child("current").get().val()))
    current_uri = fetchCurrent()
    votes = current[current_uri]['votes']
    print(votes)

    if login_session['voted'] == False:
        votes += 1
    else:
        votes -= 1
    
    db.child("current").child(current_uri).update({"votes": votes})
    login_session['voted'] = not login_session['voted']
    return votes
    

def fetchFirstQueue():
    db_info = db.child("queue").order_by_child("timestamp").limit_to_first(1).get().val()
    song_formatted = json.loads(json.dumps(db_info)) 
    print(f"songformatted {song_formatted}")   
    if song_formatted != None:
        print(f"firstin line: {next(iter(song_formatted))}")
    else:
        song_formatted = None
    return song_formatted

def skipTrack():
    first = fetchFirstQueue()
    prev = db.child("current").get().val()
    if first != None:
        db.child("previous").remove()
        db.child("previous").set(prev)
        db.child("current").set(first)
        db.child("queue").child(next(iter(first))).remove()
    else:
        print("No other songs to skip to")


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song = request.form['song']
        if song.startswith("spotify:track:") == False:
            flash("Wrong kind of input! Make sure you submit a spotify URI (it should start with spotify:track:)")
            return redirect(url_for('home'))
        else:
            print(f"New song added to queue: {song}")
            track = sp.track(song)
            db.child("queue").child(song).set({"timestamp": {".sv": "timestamp"}, "votes": 0, "url": track['album']['images'][0]['url'], "name": track['name'], "artist": track['album']['artists'][0]['name']})
            return redirect(url_for('home'))
    else:
        if "voted" not in login_session:
            login_session['voted'] = False
            print("initialised login_session['voted]")
        root = db.get().val()
        isFull = json.loads(json.dumps(root))['isFull']
        uri=fetchCurrent()
        song = json.loads((json.dumps(db.child("current").get().val())))[uri]
        return render_template("home.html", song=song, voted=login_session['voted'],
                               isFull = True if isFull == 1 else False, totalSkips=SONG_SKIP_REQUIREMENT)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
       votes = toggleVote()
       print(f" votes: {votes}, song skip requirement {SONG_SKIP_REQUIREMENT}")
       if votes >= SONG_SKIP_REQUIREMENT:
           print("skipping...")
           skipTrack()
           login_session['voted'] = False
       return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/tutorial')
def tutorial():
    return render_template("tutorial.html")

@app.route('/howto')
def howto():
    return render_template("howto.html")


if __name__ == '__main__':
    app.run(debug=True , host= '0.0.0.0', port= 5004)

