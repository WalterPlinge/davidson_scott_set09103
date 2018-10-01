from flask import abort, Flask, redirect, request, url_for
app = Flask(__name__)


@app.route("/")
def root():
	return "The default, 'root' route"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name = None):
	if name == None:
		return "Hello Napier!!! :D"
	else:
		return "Hello %s" % name

@app.route("/goodbye/")
def goodbye():
	return "Goodbye cruel world :("

@app.route("/drseuss/")
def drseuss():
	with open(url_for("static", filename = "drseuss.txt"), "r") as drseuss:
		return drseuss.read().replace("\n", "<br>")

@app.route("/private/")
def private():
	return redirect(url_for("login"))

@app.route("/login/")
def login():
	return "Now we would get username & password"

@app.route('/static-example/img/')
def static_example_img():
	start = '<img src="'
	url = url_for('static', filename='vmask.jpg')
	end = '">'
	return start + url + end

@app.route("/account/", methods=["GET", "POST"])
def account():
	if request.method == "POST":
		print request.form
		name = request.form["name"]
		return "Hello %s" % name
	else:
		return """
		<!doctype html>
		<html>
			<body>
				<form action="" method="post" name="form">
					<label for="name">Name:</label>
					<input type"text" name="name" id="name"/>
					<input type="submit" name="submit" id="submit"/>
				</form>
			</body>
		</html>
		"""

@app.route("/ttt/")
@app.route("/ttt/<path>")
def ttt(path=None):
	if path == None:
		with open(redirect(url_for("static", filename="ttt/index.html"))) as file:
			return file.read()
	else:
		filename = "/static/ttt/" + path
		with open(filename, "r") as file:
			return file.read()

@app.route("/force404/")
def force404():
	abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return "%d: Cannot find the page you requested." % 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
