import numpy as np
import math
import json
from scipy.special import expit

def getWordsFromFile(fileName):
    res = set()
    file = open(fileName)

    for line in file:
        try:
            res.add(line.strip())
        except:
            raise Exception('Error creating allowed list set.')
    return res

def loadFrequencies():
    with open("freq_map.json") as fp:
        frequencyDataDict = json.load(fp)
    return frequencyDataDict


def commonWordWeighting():
    
    frequencyDataDict = loadFrequencies()
    
    words = np.array(list(frequencyDataDict.keys()))
    freqs = np.array([frequencyDataDict[w] for w in words])
    argSort = freqs.argsort()
    sortedWords = words[argSort]
    
    xWidth = 10
    c = xWidth * (-0.5 + 3000 / len(words))
    xs = np.linspace(c - xWidth / 2, c + xWidth / 2, len(words))

    weightedFrequencies = dict()
    for word, x in zip(sortedWords, xs):
        weightedFrequencies[word] = expit(x)

    return weightedFrequencies


def getResultantWords(guess, pattern, currentWordSet):
    wordList = currentWordSet
    # Green pass
    greenSet = set()
    for i, c in enumerate(pattern):
        if int(c) == 2:
            if len(greenSet) == 0:
                for word in wordList:
                    if word[i] == guess[i]:
                        greenSet.add(word)
            else:
                tempGreenSet = set()
                for word in greenSet:
                    if word[i] == guess[i]:
                        tempGreenSet.add(word)
                greenSet = tempGreenSet
    if len(greenSet) > 0:
        wordList = greenSet


    # Yellow pass
    yellowSet = set()
    yellowLetterSet = set()
    yellowDict = dict()
    triggerYellow = False
    for i, c in enumerate(pattern):
        if int(c) == 1:
            triggerYellow = True
            yellowLetterSet.add(guess[i])

    if triggerYellow:
        for misplaced in yellowLetterSet:
            yellowDict[misplaced] = guess.count(misplaced)

        for word in wordList:
            passed = True
            for key, value in yellowDict.items():
                if word.count(key) == value:
                    pass
                else:
                    passed = False
            if passed:
                yellowSet.add(word)

        tempYellowSet = set()
        for i, c in enumerate(pattern):
            if int(c) == 1:
                for word in yellowSet:
                    if word[i] == guess[i]:
                        tempYellowSet.add(word)
        

        wordList = yellowSet.difference(tempYellowSet)

    # Grey pass
    triggerGrey = False
    greySet = set()
    for i, c in enumerate(pattern):
        if int(c) == 0:
            triggerGrey = True
            for word in wordList:
                if guess[i] in word:
                    greySet.add(word)
    if triggerGrey:
        wordList = wordList.difference(greySet)

    return wordList


def allPatterns(fileName):
    res = []
    file = open(fileName)

    for line in file:
        try:
            res.append(line.strip())
        except:
            raise Exception('Error creating pattern set.')
    return res

def rankedChoices(currentWordSet, frequencyWeights):
    allPatternList = allPatterns("all_patterns.txt")
    wordEntropies = dict()

    for word in currentWordSet:
        expectedInfo = 0
        for pattern in allPatternList:
            num = float(len(getResultantWords(word, pattern, currentWordSet)))
            
            den =  float(len(currentWordSet))
            if den == 0.0:
                proba = 0
            else:
                proba = num / den

            if proba == 0.0:
                pass
            else:
                info = math.log2(1.0/proba)
                expectedInfo += proba*info
        
        wordEntropies[word] = expectedInfo * frequencyWeights[word]

    sorted_values = sorted(wordEntropies.values(), reverse = True) 
    sortedWordEntropies = dict()
    for i in sorted_values:
        for k in wordEntropies.keys():
            if wordEntropies[k] == i:
                sortedWordEntropies[k] = wordEntropies[k]
                break

    return sortedWordEntropies


frequencyWeights = commonWordWeighting()
myWordList = getWordsFromFile("allowed_words.txt")

while len(myWordList) != 1:
    myGuess = input("Enter guess: ")

    pattern = input("\nEnter pattern that resulted from entered above guess:\n0 for grey\n1 for yellow\n2 for green\n")
    myWordList = getResultantWords(myGuess, pattern, myWordList)
    rankings = rankedChoices(myWordList, frequencyWeights)
    
    print("\nTop 3 reccomended guesses are: \n")
    i = 1
    for item in rankings.items():
        print("{}. {}".format(i, item[0]))
        i += 1
        if i > 3:
            break

    if len(myWordList) == 0:
        print("uh oh no answer...bug exists somewhere")
        break
    elif len(myWordList) == 1:
        print("yay the word is {}.".format(str(myWordList).strip("{'}")))
    else:
        pass

# best opening guess is "rates" 
