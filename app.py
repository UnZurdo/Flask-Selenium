from flask import Flask, render_template, url_for, request, json, jsonify, redirect
from datetime import datetime
import requests

from tweepyFunctions import *
import datetime
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import os
import csv
from flask import make_response


#-- WEB SCRAPING --
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#--- Tweepy --
import tweepy
from tweepy.auth import OAuthHandler

CONSUMER_KEY = 'l2EF8otpmNPXVQy8bXp7lSkZH'
CONSUMER_SECRET = 'v1Xr0dEYqLv9pVF985Cg9hf1WIfqOLszjz6npdRJMdimQ911pe'
ACCESS_TOKEN = '2723252692-LpDhLkKBUzx79283gDwA4Jg3uoGGz1ED2K5cIdY'
ACCESS_TOKEN_SECRET = '94qwUPMLK4rbynJaOZgxYQhK1i8LEiw7Po9arTBhhD9iO'
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.getcwd()

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

app = Flask(__name__)

@app.route('/senfile/', methods=['GET', 'POST'])
def sendFile():
    webscraping = jsonify(request.form['file'])
    webscraping.headers['Content-Disposition'] = 'attachment;filename=webscraping.json'
    return webscraping

@app.route('/download/twitter/csv/', methods=['POST'])
def download_csv():

    response = make_response(request.form['csv'])
    cd = 'attachment; filename=tweets.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/csv'

    return response

@app.route('/')
def homepage():
    return render_template("SearchEngine.html")

@app.route('/services/<string:id>/')
def service(id):
    return render_template("home.html", id=id)

@app.route('/new_form/Facebook/<string:id>')
def newFacebook(id):
    return render_template("new_form.html", id=id)

@app.route('/new_form/Google/<string:id>')
def newGooglek(id):
    return render_template("formGoogle.html",id=id)

@app.route('/new_form/Twitter/<string:id>')
def newTwitter(id):
    return render_template("formTwitter.html",id=id)

@app.route('/search/facebook/<string:id>', methods=['POST'])
def get_browserFacebook(id):
    # create a new Firefox session
    # driver = webdriver.Firefox()
    if id == "Firefox":
        driver = webdriver.Firefox(executable_path=BASE_DIR+'\geckodriver.exe')
    elif id == "Chrome":
        driver = webdriver.Chrome(executable_path=BASE_DIR+'\chromedriver.exe')
    else:
        return render_template("SearchEngine.html")

    driver.implicitly_wait(5)
    # driver.maximize_window()
    try:
    # navigate to the application home page
        driver.get('https://www.facebook.com/')

        username = driver.find_element_by_id("email")
        password = driver.find_element_by_id("pass")

        username.send_keys(request.form['user'])
        password.send_keys(request.form['pw'])

        driver.find_element_by_id("loginbutton").click()
        info = driver.find_element_by_tag_name('body').text

        return render_template("output.html", elements="vacia", info = info)

    except requests.exceptions.RequestException as e:
        return render_template("new_form.html")
@app.route('/search/google/<string:id>', methods=['POST'])
def get_browserGoogle(id):
    # create a new Firefox session
    # driver = webdriver.Firefox()
    if id == "Firefox":
        driver = webdriver.Firefox(executable_path=BASE_DIR+'\geckodriver.exe')
    elif id == "Chrome":
        driver = webdriver.Chrome(executable_path=BASE_DIR+'\chromedriver.exe')
    else:
        return render_template("SearchEngine.html")

    driver.implicitly_wait(30)


    # navigate to the application home page
    driver.get("http://www.google.com")

    # get the search textbox
    search_field = driver.find_element_by_id("lst-ib")
    search_field.clear()

    # enter search keyword and submit
    search_field.send_keys(request.form['tokens'])
    search_field.submit()

    # get the list of elements which are displayed after the search
    # currently on result page using find_elements_by_class_name  method
    lists= driver.find_elements_by_class_name("_Rm")

    # get the number of elements found
    elements= ("Found " + str(len(lists)) + " searches:")

    info = driver.find_element_by_tag_name('body').text

    # info = json.loads(info.decode("utf-8"))
    return render_template("output.html", elements = elements, info=info)

@app.route('/search/twitter/<string:id>',methods=['GET', 'POST'])
def get_browserTwitter(id):
    if request.method=='POST':
        if id == "all":
            return render_template("mostrarTweets.html", elements=request.form['num'], tweets=request.form['tweets'])

    n = request.form['num']
    user = request.form['user']

    try:
        stuff = get_stuff(api,user)
        tweets=[]
        tweets2=[]
        tweetsENDL,tweets = get_tweets(stuff, int(n))


        if id=="partial":
            return render_template("mostrarTweets.html", elements=n, tweets=tweetsENDL[:25], all= tweets)
        else:
            return render_template("formTwitter.html",id=id)

    except requests.exceptions.RequestException as e:
        return render_template("formTwiter.html",id=id)


if __name__ == '__main__':
    app.run()
