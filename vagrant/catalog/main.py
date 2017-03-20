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
    return render_template('songs.html', genres = genres, songs = songs)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
