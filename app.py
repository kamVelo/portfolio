from flask import Flask, render_template,redirect,request, session, url_for
from bs4 import BeautifulSoup
import requests as rq
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import smtplib, ssl
from email.mime.text import MIMEText
app = Flask(__name__)
from keys import Keys
app.secret_key = Keys.get("secretKey")
# TODO: add link to portfolio text in index.html





@app.route("/")
@app.route("/index/")
def home():
    return render_template("index.html")
@app.route("/projects/")
def projects():
    return render_template("projects.html",repos=getProjects())

@app.route('/about/')
def about():
    return render_template("about.html")
def getColours():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = Chrome(chrome_options = chrome_options)
    driver.get("https://coolors.co/generate")
    url = driver.current_url
    while "generate" in url: # waits till page is fully loaded rather than returning faulty url
        url = driver.current_url
    driver.quit()
    colours = url.split('/')[-1].split('-')
    pairs = []
    for colour in colours:
        red = int(colour[0:2], 16)
        green = int(colour[2:4], 16)
        blue = int(colour[4:6], 16)
        font = "edebe9" if (red*0.299 + green*0.587 + blue*0.114) < 186 else "010101"
        icon = "githubSVG.svg" if (red * 0.299 + green * 0.587 + blue * 0.114) < 186 else "githubIconBlack.png"
        pairs.append([colour,font,icon])
    print(pairs)
    return pairs

def getProjects():
    url = "https://github.com/kamVelo?tab=repositories"
    soup = BeautifulSoup(rq.get(url).content, "html.parser")
    list = soup.find("div", {"id": "user-repositories-list"}).findChildren("ul", recursive=False)[0]
    repos = list.findChildren("li", recursive=False)
    repo_dicts = []
    row = 0 # this will count how many rows down each respective project will be.
    i = 0
    colours = getColours()
    for repo in repos:
        if i == 5:
            i = 0
        repo_dict = {}
        info_block = repo.find("div", {"class": "col-10"})
        title = \
        info_block.findChildren("div", recursive=False)[0].findChildren("h3", recursive=False)[0].findChildren("a",recursive=False)[0].text.strip()
        try:
            desc = info_block.findChildren("div", recursive=False)[1].findChildren("p", recursive=False)[0].text.strip()

        except:
            desc = ""
        try:
            language = \
            info_block.findChildren("div", recursive=False)[2].findChildren("span", recursive=False)[0].findChildren("span", recursive=False)[1].text.strip()
        except:
            language = ""
        try:
            updated = info_block.findChildren("div", recursive=False)[2].findChildren("relative-time", recursive=False)[0].text.strip()
        except:
            updated = ""

        repo_dict["title"] = title
        repo_dict["desc"] = desc
        repo_dict["lang"] = language
        repo_dict["updated"] = updated
        repo_dict["side"] = ("right", "left")[row % 2 != 0]
        repo_dict["colour"] = colours[i][0]
        repo_dict["font"] = colours[i][1]
        repo_dict['gitIcon'] = url_for("static",filename=f"img/{colours[i][2]}")
        repo_dicts.append(repo_dict)
        row += 1
        i += 1
    return repo_dicts
if __name__ == "__main__":
    app.run(debug=True, port=5000)
