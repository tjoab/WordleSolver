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

app = Flask(__name__)

global userGuess, userPattern, frequencyWeights, myWordList
userGuess = None
userPattern = None
frequencyWeights = None
myWordList = None

frequencyWeights = commonWordWeighting()
myWordList = getWordsFromFile("allowed_words.txt")


@app.route('/', methods=['GET', 'POST'])
def index():
    global userGuess, userPattern

    if request.method == "POST":
        userGuess = request.form['userGuess']
        userPattern = request.form['userPattern']
        
    return render_template("wordle.html")


@app.route('/restart', methods=['POST'])
def restart():
    global myWordList
    if request.method == "POST":
        myWordList = getWordsFromFile("allowed_words.txt")
    return 'restarted'


@app.route('/getpythondata')
def get_python_data():
    time.sleep(1)
    global userGuess, userPattern, frequencyWeights, myWordList

    if len(myWordList) != 1:
        myWordList = getResultantWords(userGuess.lower(), userPattern, myWordList)
        

        rankings = rankedChoices(myWordList, frequencyWeights)

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
    app.run()