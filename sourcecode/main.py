import ConfigParser
import logging
import os
import random
import sqlite3

from flask import abort, flash, Flask, g, json, redirect, render_template, request, session, url_for
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = os.urandom(64)

# File paths
json_albums = 'data/album.json'
json_artists = 'data/artist.json'
json_genres = 'data/genre.json'
json_tracks = 'data/tracks.json'

# Load files
def loadAlbums():
	return json.load(open(json_albums))['albums']
def loadArtists():
	return json.load(open(json_artists))['artists']
def loadGenres():
	return json.load(open(json_genres))['genres']
def loadTracks():
	return json.load(open(json_tracks))['tracks']

@app.route('/')
def index():
	this_route = url_for('.index')
	app.logger.info('Logging a test message from ' + this_route)

	genre = random.choice(loadGenres())['title']
	artist = random.choice(loadArtists())['title']
	album = random.choice(loadAlbums())['title']
	track = random.choice(loadTracks())['title']

	return render_template('index.html', pagetitle='Musix', genre=genre, artist=artist, album=album, track=track), 200

@app.route('/album/')
@app.route('/album/<urlalbum>')
def album(urlalbum=None):
	this_route = url_for('.album')
	app.logger.info('Logging a request from ' + this_route)
	# Collect all albums
	if urlalbum == None:
		albums = []
		for album in loadAlbums():
			albums.append(album['title'])

		return render_template('album.html', albums=list(set(albums))), 200
	# Collect all album data
	else:
		for album in loadAlbums():
			if album['title'].lower() == urlalbum.lower():
				genres = []
				tracks = []
				# Genre and track data
				for track in loadTracks():
					for a in track['albums']:
						if a.lower() == urlalbum.lower():
							tracks.append(track['title'])
							for genre in track['genres']:
								genres.append(genre)

				return render_template('album.html', album=album, genres=list(set(genres)), tracks=list(set(tracks))), 200

	abort(418)

@app.route('/artist/')
@app.route('/artist/<urlartist>')
def artist(urlartist=None):
	this_route = url_for('.artist')
	app.logger.info('Logging a request from ' + this_route)
	# Collect all artists
	if urlartist == None:
		artists = []
		for artist in loadArtists():
			artists.append(artist['title'])

		return render_template('artist.html', artists=list(set(artists))), 200
	# Collect all artist data
	else:
		for artist in loadArtists():
			if artist['title'].lower() == urlartist.lower():
				genres = []
				albums = []
				tracks = []
				# Collect genres, albums, tracks
				for track in loadTracks():
					if track['artist'].lower() == urlartist.lower():
						tracks.append(track['title'])
						for album in track['albums']:
							albums.append(album)

						for genre in track['genres']:
							genres.append(genre)

				return render_template('artist.html', artist=artist, albums=list(set(albums)), genres=list(set(genres)), tracks=list(set(tracks))), 200

	abort(418)

@app.route('/genre/')
@app.route('/genre/<urlgenre>')
def genre(urlgenre=None):
	this_route = url_for('.genre')
	app.logger.info('Logging a request from ' + this_route)
	# Collect all genres
	if urlgenre == None:
		genres = []
		for genre in loadGenres():
			genres.append(genre['title'])

		return render_template('genre.html', genres=list(set(genres))), 200
	# Collect all genre data
	else:
		for genre in loadGenres():
			if genre['title'].lower() == urlgenre.lower():
				albums = []
				artists = []
				tracks = []
				# Collect albums, artists, tracks
				for track in loadTracks():
					for g in track['genres']:
						if g.lower() == urlgenre.lower():
							artists.append(track['artist'])
							tracks.append(track['title'])
							for a in track['albums']:
								albums.append(a)

				return render_template('genre.html', genre=genre, albums=list(set(albums)), artists=list(set(artists)), tracks=list(set(tracks))), 200

	abort(418)

@app.route('/track/')
@app.route('/track/<urltrack>')
def track(urltrack=None):
	this_route = url_for('.track')
	app.logger.info('Logging a request from ' + this_route)
	# Collect all tracks
	if urltrack == None:
		tracks = []
		for track in loadTracks():
			tracks.append(track['title'])

		return render_template('track.html', tracks=list(set(tracks))), 200
	# Collect all track data
	else:
		for track in loadTracks():
			if track['title'].lower() == urltrack.lower():
				return render_template('track.html', track=track), 200

	abort(418)

@app.route('/search/', methods=['GET', 'POST'])
def search():
	# Search for term
	if request.method == 'POST':
		term = request.form['search']
		# Lists
		albums = []
		artists = []
		genres = []
		tracks = []
		# Search albums
		for album in loadAlbums():
			if album['title'].lower().find(term.lower()) != -1 or album['artist'].lower().find(term.lower()) != -1 or album['date'].lower().find(term.lower()) != -1:
				albums.append(album['title'])
				continue
			for info in album['info']:
				if info.lower().find(term.lower()) != -1:
					albums.append(album['title'])
					break
		# Search artists
		for artist in loadArtists():
			if artist['title'].lower().find(term.lower()) != -1 or artist['date'].lower().find(term.lower()) != -1:
				artists.append(artist['title'])
				continue
			for info in artist['info']:
				if info.lower().find(term.lower()) != -1:
					artists.append(artist['title'])
					break
		# Search genres
		for genre in loadGenres():
			if genre['title'].lower().find(term.lower()) != -1:
				genres.append(genre['title'])
				continue
			for info in genre['info']:
				if info.lower().find(term.lower()) != -1:
					genres.append(genre['title'])
					break
		# Search tracks
		for track in loadTracks():
			# If title matches
			if track['title'].lower().find(term.lower()) != -1:
				tracks.append(track['title'])
				continue
			# If artist matches
			if track['artist'].lower().find(term.lower()) != -1:
				tracks.append(track['title'])
				continue
			# If date matches
			if track['date'].lower().find(term.lower()) != -1:
				tracks.append(track['title'])
				continue
			# If length matches
			if track['length'].lower().find(term.lower()) != -1:
				tracks.append(track['title'])
				continue
			# If album matches
			for album in track['albums']:
				if album.lower().find(term.lower()) != -1:
					tracks.append(track['title'])
					break
			# If genre matches
			for genre in track['genres']:
				if genre.lower().find(term.lower()) != -1:
					tracks.append(track['title'])
					break
			for info in track['info']:
				if info.lower().find(term.lower()) != -1:
					tracks.append(track['title'])
					break

		return render_template('search.html', term=term, albums=list(set(albums)), artists=list(set(artists)), genres=list(set(genres)), tracks=list(set(tracks))), 200
	else:
		return redirect(url_for('.index')), 200

@app.route('/drseuss/')
def drseuss():
	with open('static/drseuss.txt', 'r') as drseuss:
		return drseuss.read().replace('\n', '<br>'), 200

@app.route('/ttt/')
@app.route('/ttt/<path>')
def ttt(path=None):
	return render_template('sketch.html', sketch='/static/js/ttt.js'), 200

@app.route('/chess/')
@app.route('/chess/<path>')
def chess(path=None):
	return render_template('sketch.html', sketch='/static/js/chess.js'), 200

@app.route('/error/<int:status>')
def error(status=404):
	message = ""
	if status == 404:
		message = "Sorry, the page you requested is not available."
	if status == 418:
		message = "Sorry, this page has not been added yet."
	return render_template('error.html', message=message)

@app.errorhandler(404)
def error404(error):
	return redirect(url_for('.error', status=404))

@app.errorhandler(418)
def error418(error):
	return redirect(url_for('.error', status=418))

def init(app):
	config = ConfigParser.ConfigParser()
	try:
		config_location = 'etc/defaults.cfg'
		config.read(config_location)

		app.config['DEBUG'] = config.get('config', 'debug')
		app.config['ip_address'] = config.get('config', 'ip_address')
		app.config['port'] = config.get('config', 'port')
		app.config['url'] = config.get('config', 'url')

		app.config['log_file'] = config.get('logging', 'name')
		app.config['log_location'] = config.get('logging', 'location')
		app.config['log_level'] = config.get('logging', 'level')
	except:
		print 'Could not read configs from ', config_location

def logs(app):
	log_pathname = app.config['log_location'] + app.config['log_file']
	file_handler = RotatingFileHandler(log_pathname, maxBytes=1024 * 1024 * 10, backupCount=1024)
	file_handler.setLevel(app.config['log_level'])
	formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.setLevel(app.config['log_level'])
	app.logger.handlers.append(file_handler)

if __name__ == '__main__':
	init(app)
	logs(app)
	app.run(
		host=app.config['ip_address'],
		port=int(app.config['port'])
	)
