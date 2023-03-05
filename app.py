from flask import Flask, render_template, request, redirect, url_for, flash
import spotifybase #this is the other python file

current = spotifybase.findCurrentSongInfo()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

name = ""
@app.route("/", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']  #debating on turning this into a login_session because the name isn't saving
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

