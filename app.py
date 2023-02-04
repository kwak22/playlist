import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(
    'mongodb+srv://spartsyl:U6V10Jk7juI7SMEX@Cluster0.fsdg43e.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.Bibimbapx

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = 'aa4b6b300fdb4797bfe7625e121c99cd'
secret = 'ddbca51759f340e58471ec1b929bad7b'


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)




@app.route('/')
def home():
    return render_template('index.html')


@app.route("/playlist", methods=["POST"])
def playlist_post():
    track_input_receive = request.form.get('track_input')

    track_results = []
    artists_results = []

    track_search = sp.search(q=track_input_receive, limit=10, type='track', market=None)

    for track in track_search['tracks']['items']:

        for artist in track['artists']:
            artists_result = artist['name']
            artists_results.append(artists_result)

        track_result = track['name']
        track_results.append(track_result)

def selected_title():


    date_input_receive = request.form['date_input']
    hour_input_receive = request.form['hour_input']
    count = db.playlist.count()


    doc = {
        'track': track_selected,
        'artists': artists_selected,
        'date': date_input_receive,
        'hour': hour_input_receive,
        'count': count,

    }
    db.playlist.insert_one(doc)


@app.route("/playlist", methods=["GET"])
def playlist_get():
    playlist_list = list(db.playlist.find({}, {'_id': False}))
    return jsonify({'playlist': playlist_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)