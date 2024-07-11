from flask import Flask, render_template, request, redirect, url_for
import spotifybase #this is the other python file
from flask import session as login_session
import pyrebase
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID ="2f3ddb10f2a048e9a4a1cb89ff64697a"
CLIENT_SECRET ="48962f9a9d254800a949de8d2180734b"
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


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
    if current == None:
        print("EMPTYYYYYYYYYYYYY")
        current = {"name": 0, "votes":0}
    db_info = json.loads(json.dumps(current))
    uri = list(db_info.keys())[0]
    return uri

def fetchFirstQueue():
    first = db.child("queue").order_by_child("timestamp").limit_to_first(1).get().val()
    print("first" + str(first))

def toggleVote():
    print("yas")
    current = json.loads(json.dumps(db.child("current").get().val()))
    print(current[fetchCurrent()])

    # if login_session['voted'] == False:
    #     db.child("current").update({"votes": votes+1})
    # else:
    #     db.child("current").update({"votes":votes-1})

    # login_session['voted'] = not login_session['voted']
    # print(f"loginsessionvoted: {login_session['voted']}")



@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        login_session['name'] = request.form['name']  
        login_session['voted'] = False
        return redirect(url_for('home'))
    else:
        return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song = request.form['song']
        print("USER SONG" + song)
        db.child("queue").child(song).set({"timestamp": {".sv": "timestamp"}, "votes": 0})
        return redirect(url_for('home'))
    else:
        print("yiiis")
        root = db.get().val()
        isFull = json.loads(json.dumps(root))['isFull']
        spotify_info = sp.track(fetchCurrent())
        print(spotify_info['name'])
        print(spotify_info['album']['artists'][0]['name'])
        return render_template("home.html", song=spotify_info['name'], artists=spotify_info['album']['artists'][0]['name'], name=login_session['name'], voted=login_session['voted'],
                               isFull = True if isFull == 1 else False )

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
       toggleVote()
       return redirect(url_for('home'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True , host= '0.0.0.0', port= 5000)

