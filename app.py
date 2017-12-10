from flask import Flask, render_template, url_for
from datetime import datetime


#-- WEB SCRAPING --
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/new_form/')
def new():
    return render_template("new_form.html")

@app.route('/search/', methods=['POST'])
def get_browser():
    # create a new Firefox session
    # driver = webdriver.Firefox()
    driver = webdriver.Firefox(executable_path=r'C:\Users\alber\Projects\flask\geckodriver.exe')
    driver.implicitly_wait(30)
    driver.maximize_window()

    # navigate to the application home page
    driver.get("http://www.google.com")

    # get the search textbox
    search_field = driver.find_element_by_id("lst-ib")
    search_field.clear()

    # enter search keyword and submit
    search_field.send_keys("Selenium WebDriver Interview questions")
    search_field.submit()

    # get the list of elements which are displayed after the search
    # currently on result page using find_elements_by_class_name  method
    lists= driver.find_elements_by_class_name("_Rm")

    # get the number of elements found
    elements = ("Found " + str(len(lists)) + "searches:")
    return render_template("output.html", elements = elements)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
