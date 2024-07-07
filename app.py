from flask import Flask, render_template, request, redirect, url_for, flash
import spotifybase #this is the other python file
from flask import session as login_session
import spotipy
from spotipy.oauth2 import SpotifyOAuth


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
CLIENT_ID ="2f3ddb10f2a048e9a4a1cb89ff64697a"
CLIENT_SECRET ="48962f9a9d254800a949de8d2180734b"
REDIRECT_URI = "http://example.com"

scope = "user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = REDIRECT_URI,
        scope=scope))

@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        login_session['name'] = request.form['name']  
        return redirect(url_for('home'))
    else:
        return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song = request.form['song']
        print(song)
        sp.add_to_queue(song)
        return redirect(url_for('home'));
    return render_template("home.html", name=login_session['name'], song=spotifybase.findCurrentSongInfo())

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
       print(spotifybase.voteToSkip())
    return render_template("home.html", current=login_session['name'])

if __name__ == '__main__':
    app.run(debug=True)

