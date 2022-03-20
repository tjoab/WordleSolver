# Required imports
import numpy as np
import math
import json
from scipy.special import expit

# Reads in all possible 5 letter words and
# returns them in a set
def getWordsFromFile(fileName):
    res = set()

    file = open(fileName)
    for line in file:
        try:
            res.add(line.strip())
        except:
            raise Exception('Error creating word list.')
    return res


# Reads in all possible 5^3 Wordle patterns, previously encoded 
# as '0' for grey, '1' for yellow and '2' for green. Returns
# them in a list.
def allPatterns(fileName):
    res = []
    file = open(fileName)

    for line in file:
        try:
            res.append(line.strip())
        except:
            raise Exception('Error creating pattern list.')
    return res


# Load up 5 letter word frequency data 
# from the Google Ngram viewer
def loadFrequencies():
    # Ngram viewer data sits in "freq_map.json" as a dictionary
    with open("freq_map.json") as fp:
        frequencyDataDict = json.load(fp)
    return frequencyDataDict


# Creates and returns a dictionary of word-weight pairs, where the 
# weights consider 5 letter word frequency data
def commonWordWeighting():
    # Google Ngram word frequency data 
    frequencyDataDict = loadFrequencies()
    
    # Sort the words
    words = np.array(list(frequencyDataDict.keys()))
    freqs = np.array([frequencyDataDict[w] for w in words])
    argSort = freqs.argsort()
    sortedWords = words[argSort]
    
    # We want to "almost" binarize our frequencies using the sigmoid
    # function. The "x=0" point is chosen arbitrarily to be at the
    # 3000th most common word from the frequency data. This point was
    # chosen from visual inspection of the data beforehand.  
    xWidth = 10
    c = xWidth * (-0.5 + 3000 / len(words))
    xs = np.linspace(c - xWidth / 2, c + xWidth / 2, len(words))

    # Pass the frequencies through the sigmoid, and create a new 
    # dictionary of these weights
    weightedFrequencies = dict()
    for word, x in zip(sortedWords, xs):
        weightedFrequencies[word] = expit(x)
    return weightedFrequencies


# Given a current guess, the Wordle pattern associated with that guess, 
# and the current set of next possible guesses, this function further
# refines the set of next possible guesses based on the Wordle pattern
# passed. 
def getResultantWords(guess, pattern, currentWordSet):
    # Set word list to the entire set of possibel guesses
    wordList = currentWordSet
    
    # Green pass. Reduces the potential set the fastest, and usually
    # by the greatest amount... so it is done first. 
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
    # Update the word list if the green pass reduces it.
    if len(greenSet) > 0:
        wordList = greenSet


    # Yellow pass. Tricky... needed to consider multiple yellows simultaneously, 
    # and multiple of the same letter appearing yellow. 
    yellowSet = set()
    yellowLetterSet = set()
    yellowDict = dict()
    triggerYellow = False

    for i, c in enumerate(pattern):
        if int(c) == 1:
            triggerYellow = True
            # Creates a set of all yellow letters in the pattern if they exist
            yellowLetterSet.add(guess[i])

    # We only want to run this section, if a yellow letter is present
    if triggerYellow:
        # For each misplaced letter, we create a dictionary of misplaced letter
        # and the number of times they appear in the word. This handles multiple
        # letter appearing yellow.
        for misplaced in yellowLetterSet:
            yellowDict[misplaced] = guess.count(misplaced)

        for word in wordList:
            passed = True
            # Make sure for each each word in the current word list has the correct
            # number of misplaced letters. We add these to a set... which will become 
            # our new word list. BUT we did not consider the where these letters are 
            # appearing yet... only that these words have the correct number of letters
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
                # Here we find all the words from our yellow word set that do not 
                # follow the rules of wordle. Namely that a yellow letter cannot apear
                # in that specific position anymore. We create a set of these words.
                for word in yellowSet:
                    if word[i] == guess[i]:
                        tempYellowSet.add(word)
        #We set the new word list to be the difference between these sets
        wordList = yellowSet.difference(tempYellowSet)


    # Grey pass. 
    triggerGrey = False
    greySet = set()

    # Find all words in the word list that contain any grey letters, if said
    # grey letters appear in the pattern. Create a set of these words.
    for i, c in enumerate(pattern):
        if int(c) == 0:
            triggerGrey = True
            for word in wordList:
                if guess[i] in word:
                    greySet.add(word)
    # We only run this section, if a grey letter is present
    if triggerGrey:
        # The final word list is the difference of these sets
        wordList = wordList.difference(greySet)

    # Return the set of next possible guesses
    return wordList


# Out of the the word set passed, and the dictionary of word frequencies, we can
# rank each of the words in the passed word set. 
def rankedChoices(currentWordSet, frequencyWeights):
    # Load in the all possible 3^5 Wordle patterns
    allPatternList = allPatterns("all_patterns.txt")

    # The way we will rank each word is by using entropy.
    wordEntropies = dict()
    # For each word... we find the probability of the subsequent word 
    # list for every possible Wordle pattern creating a distribution
    for word in currentWordSet:
        # E[I] = entropy = sum( p(pattern) * I(pattern) ) where I(pattern) = log_2(1/p(pattern))
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

        # After we calculate the entropy for each word... we use the word frequencies from
        # the Google Ngram viewer to tweak the rankings to favour more common words.
        wordEntropies[word] = expectedInfo * frequencyWeights[word]

    # Sort the dictionary of rankings from largest amount of bits to the smallest 
    sorted_values = sorted(wordEntropies.values(), reverse = True) 
    sortedWordEntropies = dict()
    for i in sorted_values:
        for k in wordEntropies.keys():
            if wordEntropies[k] == i:
                sortedWordEntropies[k] = wordEntropies[k]
                break

    # Return sorted dictionary of rankings based on 
    # greatest information aquired (entropy in bits)
    return sortedWordEntropies


def main():
    frequencyWeights = commonWordWeighting()
    myWordList = getWordsFromFile("allowed_words.txt")

    while len(myWordList) != 1:
        myGuess = input("\nEnter guess: ")
        pattern = input("\nLEGEND\nGrey: 0\nYellow: 1\nGreen: 2\n\nEnter pattern that resulted from entered above guess: ")
        
        myWordList = getResultantWords(myGuess, pattern, myWordList)
        rankings = rankedChoices(myWordList, frequencyWeights)
        
        print("\nTop 3 reccomended guesses are: \n")
        i = 1
        for item in rankings.items():
            print("{}. {}    {:.3f} Bits".format(i, item[0], item[1]))
            i += 1
            if i > 3:
                break

        if len(myWordList) == 0:
            print("\nUh oh. No answer...bug exists somewhere:(\n")
            break
        elif len(myWordList) == 1:
            print("\nThe answer must be {} :D\n".format(str(myWordList).strip("{'}")))
        else:
            pass

# Note: By running commonWordWeighting() with the full set of 5 letter English words, 
# we find that the best opening guess is "rates"
if __name__ == '__main__':
    main()
