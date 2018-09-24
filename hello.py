from flask import Flask, redirect, url_for
app = Flask(__name__)


@app.route("/")
def root():
   return "The default, 'root' route"


@app.route("/hello")
def hello():
   return "Hello Napier!!! :D"

@app.route("/goodbye")
def goodbye():
   return "Goodbye cruel world :("

@app.route("/drseuss")
def drseuss():
   return "One fish, two fish, red fish, blue fish"

@app.route("/private")
def private():
   return redirect(url_for("login"))

@app.route("/login")
def login():
   return "Now we would get username & password"

@app.errorhandler(404)
def page_not_found(error):
   return "Couldn't find the page you requested.", 404

if __name__ == "__main__":
   app.run(host='0.0.0.0', debug=True)
