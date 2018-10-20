import ConfigParser
import logging
import os
import random
import sqlite3

from flask import abort, flash, Flask, g, json, redirect, render_template, request, session, url_for
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = os.urandom(64)

json_albums = json.load(open("data/album.json"))['albums']
json_artists = json.load(open("data/artist.json"))['artists']
json_genres = json.load(open("data/genre.json"))['genres']
json_tracks = json.load(open("data/tracks.json"))['tracks']

@app.route('/')
def index():
	this_route = url_for('.index')
	app.logger.info('Logging a test message from ' + this_route)

	genre = random.choice(json_genres)['title']
	artist = random.choice(json_artists)['title']
	album = random.choice(json_albums)['title']
	track = random.choice(json_tracks)['title']

	return render_template('index.html', pagetitle='Musix', genre=genre, artist=artist, album=album, track=track)

@app.route('/album/')
@app.route('/album/<urlalbum>')
def album(urlalbum=None):
	this_route = url_for('.album')
	app.logger.info('Logging a request from ' + this_route)

	if urlalbum == None:
		albums = []
		for track in json_tracks:
			for album in track['albums']:
				albums.append(album)

		return render_template('album.html', albums=list(set(albums)))

	else:
		for album in json_albums:
			if album['title'].lower() == urlalbum.lower():
				genres = []
				tracks = []
				for track in json_tracks:
					for a in track['albums']:
						if a.lower() == urlalbum.lower():
							tracks.append(track['title'])
							for genre in track['genres']:
								genres.append(genre)

				return render_template('album.html', album=album, genres=list(set(genres)), tracks=list(set(tracks)))

	abort(404)

@app.route('/artist/')
@app.route('/artist/<urlartist>')
def artist(urlartist=None):
	this_route = url_for('.artist')
	app.logger.info('Logging a request from ' + this_route)

	if urlartist == None:
		artists = []
		for track in json_tracks:
			artists.append(track['artist'])

		return render_template('artist.html', artists=list(set(artists)))

	else:
		for artist in json_artists:
			if artist['title'].lower() == urlartist.lower():
				genres = []
				albums = []
				tracks = []
				for track in json_tracks:
					if track['artist'].lower() == urlartist.lower():
						tracks.append(track['title'])
						for album in track['albums']:
							albums.append(album)

						for genre in track['genres']:
							genres.append(genre)

				return render_template('artist.html', artist=artist, albums=list(set(albums)), genres=list(set(genres)), tracks=list(set(tracks)))

	abort(404)

@app.route('/genre/')
@app.route('/genre/<urlgenre>')
def genre(urlgenre=None):
	this_route = url_for('.genre')
	app.logger.info('Logging a request from ' + this_route)

	if urlgenre == None:
		genres = []
		for track in json_tracks:
			for genre in track['genres']:
				genres.append(genre)

		return render_template('genre.html', genres=list(set(genres)))
	else:
		for genre in json_genres:
			if genre['title'].lower() == urlgenre.lower():
				albums = []
				artists = []
				tracks = []
				for track in json_tracks:
					for g in track['genres']:
						if g.lower() == urlgenre.lower():
							artists.append(track['artist'])
							tracks.append(track['title'])
							for a in track['albums']:
								albums.append(a)

				return render_template('genre.html', genre=genre, albums=list(set(albums)), artists=list(set(artists)), tracks=list(set(tracks)))

	abort(404)

@app.route('/track/')
@app.route('/track/<urltrack>')
def track(urltrack=None):
	this_route = url_for('.track')
	app.logger.info('Logging a request from ' + this_route)

	if urltrack == None:
		tracks = []
		for track in json_tracks:
			tracks.append(track['title'])

		return render_template('track.html', tracks=list(set(tracks)))

	else:
		for track in json_tracks:
			if track['title'].lower() == urltrack.lower():
				return render_template('track.html', track=track)

	abort(404)

@app.route('/drseuss/')
def drseuss():
	with open('static/drseuss.txt', 'r') as drseuss:
		return drseuss.read().replace('\n', '<br>')

@app.route('/login/')
@app.route('/login/<message>')
def login(message=None):
	if message != None:
		flash(message)
	else:
		flash(u'A default message')
	return redirect(url_for('index'))

@app.route('/account/', methods=['GET', 'POST'])
def account():
	if request.method == 'POST':
		print request.form
		name = request.form['name']
		return 'Hello %s' % name
	else:
		return render_template('form.html')

@app.route('/session/write/<name>/')
def write(name=None):
	session['name'] = name
	return 'Wrote %s into \'name\' key of session' % name
@app.route('/session/read/')
def read():
	try:
		if (session['name']):
			return str(session['name'])
	except KeyError:
		pass
	return 'No session variable set for \'name\' key'
@app.route('/session/remove/')
def remove():
	session.pop('name', None)
	return 'removed key \'name\' from session'

@app.route('/ttt/')
@app.route('/ttt/<path>')
def ttt(path=None):
	return render_template('sketch.html', sketch='/static/js/ttt.js')

@app.route('/chess/')
@app.route('/chess/<path>')
def chess(path=None):
	return render_template('sketch.html', sketch='/static/js/chess.js')

@app.errorhandler(404)
def page_not_found(error):
	return render_template('error.html')

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
