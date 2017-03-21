from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
import datetime

app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
# Importing NoResultFound for error handling of query
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, Genre, Song, User


#Connect to Database and create database session
engine = create_engine('sqlite:///music.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#######################################
#
# JSON APIs to view Music Information
#
#######################################
@app.route('/genre/<int:genre_id>/JSON')
def genreJSON(genre_id):
    genre = session.query(Genre).filter_by(id = genre_id).one()
    songs = session.query(Song).filter_by(genre_id = genre_id).all()
    return jsonify(songs = [i.serialize for i in songs])

@app.route('/genre/<int:genre_id>/song/<int:song_id>/JSON')
def songJSON(genre_id, song_id):
    try:
        song = session.query(Song).filter_by(id = song_id, genre_id = genre_id).one()
    # Adding error handling if no result is found.
    except NoResultFound:
        return jsonify({'error' : 'Genre and song do not match!'})

    return jsonify(song.serialize)

@app.route('/genre/JSON')
def allGenreJSON():
    genres = session.query(Genre).all()
    return jsonify(genres = [i.serialize for i in genres])


############################
#
# Template rendering
#
############################
# Show all genres
@app.route('/')
def showGenres():
    songs = session.query(Song).order_by(asc(Song.name))
    genres = session.query(Genre).order_by(asc(Genre.name))
    return render_template('main.html', songs = songs, genres = genres)

@app.route('/genre/<int:genre_id>/')
def showGenreSongs(genre_id):
    genres = session.query(Genre).order_by(asc(Genre.name))
    songs = session.query(Song).filter_by(genre_id = genre_id)
    current_genre = session.query(Genre).filter_by(id = genre_id).one()
    return render_template('public_songs.html', genres = genres, songs = songs, curr_genre = current_genre)

@app.route('/genre/<int:genre_id>/song/<int:song_id>/', methods=['GET', 'POST'])
def editSong(genre_id, song_id):
    editedSong = session.query(Song).filter_by(id = song_id).one()
    genre = session.query(Genre).filter_by(id = genre_id).one()
    genres = session.query(Genre).order_by(asc(Genre.name))

    if request.method == 'POST':
        if request.form['song-name']:
            editedSong.name = request.form['song-name']
        if request.form['artist-name']:
            editedSong.artist_name = request.form['artist-name']
        if request.form['youtube_url']:
            # Decided to be more user friendly and ask users to enter a youtube url. Since the url is consistent and only the query_id changes, I extract the query id from the url
            youtube_id = request.form['youtube_url'].split("v=", 1)[1]
            editedSong.youtube_id = youtube_id
        if request.form['genre_id']:
            editedSong.genre_id = request.form['genre_id']
        session.add(editedSong)
        session.commit()
        flash('Successfully Edited %s - %s' % (editedSong.name, editedSong.artist_name))
        return redirect(url_for('showGenreSongs', genre_id = editedSong.genre_id))
    else:
        return render_template('editsong.html', genre = genre, genres = genres, song = editedSong)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
