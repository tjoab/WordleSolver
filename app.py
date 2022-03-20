from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    current_app,
)
from wordle import *
import time
import json
# Import cache
from common import cache

app = Flask(__name__)
cache.init_app(app=app, config={"CACHE_TYPE": "filesystem",'CACHE_DIR': '/tmp'})

cache.set("frequencyWeights", commonWordWeighting())
cache.set("myWordList", getWordsFromFile("allowed_words.txt"))


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        cache.set("uGuess", request.form['userGuess'])
        cache.set("uPattern", request.form['userPattern'])
        
    return render_template("wordle.html")


@app.route('/restart', methods=['POST'])
def restart():
    if request.method == "POST":
        cache.set("myWordList", getWordsFromFile("allowed_words.txt"))
    return 'restarted'


@app.route('/getpythondata')
def get_python_data():
    time.sleep(1)

    if len(cache.get("myWordList")) != 1:
        myWordList = cache.get("myWordList")
        
        updatedWordList = getResultantWords(cache.get("uGuess").lower(), cache.get("uPattern"), myWordList)

        cache.set("myWordList", updatedWordList)

        rankings = rankedChoices(cache.get("myWordList"), cache.get("frequencyWeights"))

        topGuesses = {}
        i = 1
        for word, bits in rankings.items():
            topGuesses[i] = [word, bits]
            i = i + 1
            if i > 3:
                break            
        print(topGuesses)
    return json.dumps(topGuesses)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
