from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from collections import OrderedDict
import json
import datetime
import spotifybase


# config = {
#   "apiKey": "AIzaSyCRj8D8wEQ7wf4u2QHMxtQ12cJZSBx0yZI",
#   "authDomain": "spotify-thing-3d02e.firebaseapp.com",
#   "projectId": "spotify-thing-3d02e",
#   "storageBucket": "spotify-thing-3d02e.appspot.com",
#   "messagingSenderId": "1072909622967",
#   "appId": "1:1072909622967:web:0daa7d2c3ce1795da87732",
#   "measurementId": "G-H1XGBRX5TV"
# }

current = spotifybase.findCurrentSongInfo()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

name = ""
@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('home'))
    else:
        return render_template("signup.html")

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        song = request.form['song']
        spotifybase.addNewSongToQueue(song, name)
    return render_template("home.html", current=current)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
       print(spotifybase.voteToSkip())
    return render_template("home.html", current=current)

if __name__ == '__main__':
    app.run(debug=True)

