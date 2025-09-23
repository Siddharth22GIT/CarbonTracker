from flask import Flask


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Behind it ALL"

@app.route("/about")
def About():
    return "Here at BIA I do all kind of stuff basically pulling out hidden loopholes in the system to sniffing around random stuff which really matters in our daily lives. If you wanna join me in my journey then follow me @behinditallofficial and I am on youtube as well so make sure you subscribe the channel too to get the taste of my ongoing discoveries"
















