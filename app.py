from flask import Flask, render_template, url_for, request, json, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup


#-- WEB SCRAPING --
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

@app.route('/senfile/', methods=['GET', 'POST'])
def sendFile():
    webscraping = jsonify(request.form['file'])
    webscraping.headers['Content-Disposition'] = 'attachment;filename=webscraping.json'
    return webscraping

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
    return render_template("formTwitter.html")

@app.route('/search/facebook/<string:id>', methods=['POST'])
def get_browserFacebook(id):
    # create a new Firefox session
    # driver = webdriver.Firefox()
    if id == "Firefox":
        driver = webdriver.Firefox(executable_path=r'C:\Users\alber\Projects\flask\geckodriver.exe')
    elif id == "Chrome":
        driver = webdriver.Chrome(executable_path=r'C:\Users\alber\Projects\flask\chromedriver.exe')
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
        driver = webdriver.Firefox(executable_path=r'C:\Users\alber\Projects\flask\geckodriver.exe')
    elif id == "Chrome":
        driver = webdriver.Chrome(executable_path=r'C:\Users\alber\Projects\flask\chromedriver.exe')
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

@app.route('/search/twitter/<string:id>', methods=['POST'])
def get_browserTwitter(id):
    # create a new Firefox session
    # driver = webdriver.Firefox()
    if id == "Firefox":
        driver = webdriver.Firefox(executable_path=r'C:\Users\alber\Projects\flask\geckodriver.exe')
    elif id == "Chrome":
        driver = webdriver.Chrome(executable_path=r'C:\Users\alber\Projects\flask\chromedriver.exe')
    else:
        return render_template("SearchEngine.html")

    driver.implicitly_wait(30)
    # driver.maximize_window()
    try:
    # navigate to the application home page
        driver.get('https://twitter.com/login')

        username_field = driver.find_element_by_class_name("js-username-field")
        password_field = driver.find_element_by_class_name("js-password-field")

        username_field.send_keys(request.form['user'])
        driver.implicitly_wait(1)

        password_field.send_keys(request.form['pw'])
        driver.implicitly_wait(1)

        driver.find_element_by_class_name("EdgeButtom--medium").click()

        return render_template("output.html")

    except requests.exceptions.RequestException as e:
        return render_template("new_form.html", elements = elements)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
