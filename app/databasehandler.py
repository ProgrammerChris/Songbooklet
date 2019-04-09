from app import mongo  # MongoDB client

# Using artist as _id to keep unique and not having more documents for the same artist.


""" DatabaseHandler
    All queries and manipulations to the connected mongodb database is handled in this file
"""


class DatabaseHandler:

    def __init__(self):
        """ Init the target collection in the mongoDB. In this case called 'Artists'
            Use the 'Development' collection while developing and testing.
        """
        self.collection = mongo.db.Development  # Development DB (Should be changing acc to .flaskenv FLASK_ENV)
        #self.collection = mongo.db.Artists  # Production DB

    def get_artists(self):
        """Gets all '_id' fields from all documents. Returns a list"""
        return self.collection.find().distinct('_id')

    def get_all_songs(self):
        """Gets all 'songs' fields from all documents containing that field. Returns a list"""
        return self.collection.find().distinct('songs')

    def get_all_songs_from_artist(self, artist):
        """Finds artist by '_id' in the mongoDB collection. All _ids in this collection is artistnames."""
        songs = []

        for doc in self.collection.find({'_id': artist}):
            songs = doc.get('songs')

        return songs

    def get_artist_by_song(self, songname):
        """Search all documents in the collection for a specific song, return the _id(artistname) of the document"""
        return [doc.get('_id') for doc in self.collection.find({'songs': songname})]

    def add_artist_with_songs(self, artist, songs):
        """Add artist to DB. set '_id == artistname', need to supply a list of songs or an empty list"""

        if isinstance(songs, str):
            songs = songs.lower().split(',')
        else:
            [song.lower() for song in songs]

        self.collection.insert({'_id': artist.lower(), 'songs': songs})

    def add_song_to_artist(self, artist, song):
        self.collection.update({'_id': artist.lower()}, {'$addToSet': {'songs': song}})

    def add_songs_to_artist(self, artist, songs):
        """Adds a song to an artist in the DB, if artist not in the database, add artist and song to DB"""
        # TODO: Check if artist in DB, if not, add artist and song.
        self.collection.update({'_id': artist.lower()}, {'$addToSet': {'songs': {'$each': songs}}})

    def delete_song(self, artist, song):
        """Delete specific song from specific artist DB"""
        self.collection.update({'_id': artist.lower()}, {'$pull': {'songs': song}})

    def delete_songs(self, artist, songs):
        """Delete all songs from specific artist in DB"""
        self.collection.update({'_id': artist}, {'$pullAll': {'songs': songs}})

    def delete_artist(self, artist):
        """Delete specific artist from DB"""
        self.collection.remove({'_id': artist})

    def delete_all(self):
        """Delete ALL documents from chosen collection! USE WITH CARE!"""
        self.collection.remove({ })
