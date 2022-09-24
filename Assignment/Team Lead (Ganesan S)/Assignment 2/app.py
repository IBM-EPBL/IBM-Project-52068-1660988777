from flask import Flask, url_for, render_template
from markupsafe import escape

app=Flask(__name__)
@app.route("/")
def index():
    return render_template("signup.html")

@app.route("/user/")
def hello(name):
    return render_template("index.html")

@app.route("/users/<username>")
def profile(username):
    return render_template("profile.html", username=username)

