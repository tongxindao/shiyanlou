#-*- coding:utf-8 -*-
from flask import Flask, request, session, redirect, url_for, render_template
from flask_pymongo import PyMongo
from requests_oauthlib import OAuth2Session
import datetime, time
import os

app = Flask(__name__)
mongo = PyMongo(app)
app.config["MONGO_HOST"] = "127.0.0.1"
app.config["MONGO_PORT"] = 27017
app.config["MONGO_DBNAME"] = "github_cafe"

client_id = "b5dbe561e3dbbc4c35d8"
client_secret = "77d6bf70fdf18c890c6e68f9680fa0024a981589"
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"

@app.route('/', methods=["GET", "POST"])
@app.route('/page/<int:page>', methods=["GET", "POST"])
def index(page = 1):
    if request.method == "POST":
        session["geek_wisdom"] = request.form["geek_wisdom"]
        try:
            githuber_say()
        except:
            github = OAuth2Session(client_id)
            authorization_url, state = github.authorization_url(authorization_base_url)
            session["oauth_state"] = state
            return redirect(authorization_url)

    wisdom_list = get_githuber_wisdom(page=page)
    return render_template("index.html", wisdom_list=wisdom_list, page=page, page_count=get_page_count())


@app.route('/callback', methods=["GET"])
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)
    session['oauth_token'] = token
    githuber_say()
    return redirect(url_for("index"))

def githuber_say():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    profile = github.get('https://api.github.com/user').json()

    wisdom_dict = {
        "username": profile["name"],
        "avatar_url": profile["avatar_url"],
        "html_url": profile["html_url"],
        "geek_wisdom": session["geek_wisdom"],
        "datetime" : datetime.datetime.today().strftime("%Y/%-m/%d %H:%M"),
        "timestamp" : time.time()
    }

    del session["geek_wisdom"]
    mongo.db.wisdom.insert(wisdom_dict)

def get_githuber_wisdom(count=10, page=1):
    return mongo.db.wisdom.find({}).sort([('timestamp', -1)]).skip(count * (page-1)).limit(count)

def get_page_count(count=10):
    # python3 ?? / ?? //
    return mongo.db.wisdom.find({}).count() / count + 1

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, ssl_context=("ssl.crt", "ssl.key"), threaded=True)

