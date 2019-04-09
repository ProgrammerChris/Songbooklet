from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from collections import defaultdict, OrderedDict
from flask import render_template, request, send_file, session
import os

from .databasehandler import DatabaseHandler
from .bookeltfactory import merge_pdfs


collection = DatabaseHandler()

songs_from_db = collection.get_all_songs()
artists_from_db = collection.get_artists()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/<artist>', methods=['GET', 'POST'])
def artist(artist):
    """After clicking an artist in browser, display the artists songs in a list and artistname in URL"""
    songs = []
    for song in collection.get_all_songs_from_artist(artist):
        songs.append(song.title())

    if artist in collection.get_artists():
        return render_template('artist.html', artist=artist, songs=songs)
    else:
        return render_template('404.html')


@app.route('/artists', methods=['GET', 'POST'])
def artists():
    """Show list of artists after 'artists'-button clicked in browser"""
    artists = []
    for artist in artists_from_db:
        artists.append(artist)

    artists.sort()

    return render_template('artists.html', artists=artists)


@app.route('/songs', methods=['GET', 'POST'])
def songs():
    """Show all songs after 'songs'-button clicked in browser"""

    return render_template('songs.html', artists=get_all_songs())


@app.route('/results', methods=['GET', 'POST'])
def results():
    """Get results from DB and render to browser"""

    # Getting searchtext from the browser text input.
    searchtext = request.args.get('searchbar')

    if searchtext.strip() == '':
        return render_template('results.html', searchtext=searchtext, artists=artists_from_db, songs=songs_from_db, songline=get_all_songs())

    artists.sort()
    results = []  #set()

    for artistname in artists_from_db:  #Loop artists
        if artistname.lower().find(searchtext.lower()) != -1:  # If match or close match, add to result.
            for song in collection.get_all_songs_from_artist(artistname):  # TODO: Implement binarysearch?
                results.append(song)
    
    for song in songs_from_db:  #Loop songs
        if song not in results:  # Skip if song aleady in the results.
            if song.lower().find(searchtext.lower()) != -1:  # If match or close match, add to result.
                results.append(song)

    # Assemble a dict to be used to create HTML element in browser when rendering.
    songline = defaultdict(list)  # To get a dict of list to be able to store duplicate keys.
    for song in results:
        songline[''.join(collection.get_artist_by_song(song))].append(song)

    return render_template('results.html', searchtext=searchtext, artists=artists, songs=songs, songline=songline)


@app.route('/download', methods=['GET', 'POST'])
def download():
    # Empty booklet folder every time /download reached. To stop folder from taking up space on server.
    booklets_dir = app.root_path + '/static/booklets/'  # Booklet folder on server
    for booklet in os.listdir(booklets_dir):
        file_path = os.path.join(booklets_dir, booklet)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Send file to client for download.
    if request.method == 'POST':
        json = request.get_json()
        booklet = merge_pdfs(json)
        session['booklet'] = booklet

    return render_template('download.html')


@app.route('/download/<filename>', methods=['GET', 'POST'])
def booklet(filename):
    return send_file(session['booklet'], as_attachment=True, mimetype='application/pdf')


@app.errorhandler(404)
def error_page_404(e):
    return render_template('404.html'), 404


def get_all_songs():
    """Creating a dict with artists and songs, using OrderedDict to be able to have duplicate keys for artists"""
    artists = {}

    for artist in artists_from_db:
        artists[artist] = []
        songs = collection.get_all_songs_from_artist(artist)
        for song in songs:
            if song != '':
                artists[artist].append(song)
    return OrderedDict(sorted(artists.items()))


if __name__ == "__main__":
    app.run()

