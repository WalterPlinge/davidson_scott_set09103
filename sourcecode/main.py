import ConfigParser
import logging
import os
import sqlite3

from flask import abort, flash, Flask, g, redirect, render_template, request, session, url_for
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = os.urandom(64)

db_location = 'var/test.db'

@app.route('/')
def index():
	this_route = url_for('.index')
	app.logger.info('Logging a test message from ' + this_route)
	return render_template('index.html')

@app.route('/album/')
@app.route('/album/<album>')
def album(album=None):
	if album == None:
		return 'Albums:'
	return 'album = ' + album

@app.route('/artist/')
@app.route('/artist/<artist>')
def artist(artist=None):
	if artist == None:
		return 'Artists:'
	return 'artist = ' + artist

@app.route('/genre/')
@app.route('/genre/<genre>')
def genre(genre=None):
	if genre == None:
		return 'Genres:'
	return 'genre = ' + genre

@app.route('/track/')
@app.route('/track/<track>')
def track(track=None):
	if track == None:
		return 'Tracks:'
	return 'track = ' + track

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

@app.route('/bootstrap/')
def bootstrap():
	return render_template('bootstrap.html')

@app.route('/ttt/')
@app.route('/ttt/<path>')
def ttt(path=None):
	return render_template('sketch.html', sketch = '/static/js/ttt.js')

@app.errorhandler(404)
def page_not_found(error):
	return 'Cannot find the page you requested.', 404

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
