from flask import Flask, render_template,redirect,request, session, url_for
from bs4 import BeautifulSoup
import requests as rq
app = Flask(__name__)
app.secret_key = "sadfljkf"

@app.route("/")
@app.route("/index/")
def home():
    return render_template("index.html")



def getProjects():
    url = "https://github.com/kamVelo?tab=repositories"
    soup = BeautifulSoup(rq.get(url).content, "html.parser")
    list = soup.find("div", {"id": "user-repositories-list"}).findChildren("ul", recursive=False)[0]
    repos = list.findChildren("li", recursive=False)
    repo_dicts = []
    for repo in repos:
        repo_dict = {}
        info_block = repo.find("div", {"class": "col-10"})
        title = \
        info_block.findChildren("div", recursive=False)[0].findChildren("h3", recursive=False)[0].findChildren("a",
                                                                                                               recursive=False)[
            0].text.strip()
        try:
            desc = info_block.findChildren("div", recursive=False)[1].findChildren("p", recursive=False)[0].text.strip()

        except:
            desc = None
        try:
            language = \
            info_block.findChildren("div", recursive=False)[2].findChildren("span", recursive=False)[0].findChildren(
                "span", recursive=False)[1].text.strip()
        except:
            language = None
        try:
            updated = info_block.findChildren("div", recursive=False)[2].findChildren("relative-time", recursive=False)[
                0].text.strip()
        except:
            updated = None

        repo_dict["title"] = title
        repo_dict["desc"] = desc
        repo_dict["lang"] = language
        repo_dict["updated"] = updated
        repo_dicts.append(repo_dict)
    return repo_dicts
if __name__ == "__main__":
    app.run(debug=True, port=5000)