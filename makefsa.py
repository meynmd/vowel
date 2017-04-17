import re
import sys
import unicodedata
from collections import defaultdict


MIN_PROB = 0.005
stateNames = {}

'''
converts concordance-style dictionary into dictionary from
key => (# of occurrences) to
key => (occurrences / # of keys in dict)
'''
def makeProbDict(dictionary):
    probDict = defaultdict(float)
    ks = dictionary.keys()

    for k in ks:
        probDict[k] = dictionary[k] / len(ks)

    return probDict



'''
bigrams = makeBigrams(sentences)

takes a string consisting of sentences from which to extract bigrams

returns bigram model represented as dictionary of
(string, string) => # of occurrences
'''
def makeBigrams(sentences):
    print('Constructing bigrams.', file=sys.stderr)

    sentences = [s for s in sentences if s != '']
    bigrams = defaultdict(defaultdict)

    for s in sentences:
        s = cleanupString(s)
        s = str.upper(s)
        s = re.split(r'[,\s]\s*', s)
        s = [w for w in s if w != '']
        if len(s) < 2:
            continue

        # get each pair of consecutive words in each sentence
        for i in range(len(s) - 1):
            w1 = ' '.join(list(s[i]))
            w2 = ' '.join(list(s[i + 1]))
            if bigrams.get(w1) == None:
                bigrams[w1] = defaultdict(int)
            bigrams[w1][w2] = bigrams[w1][w2] + 1

    # record probability of each pair
    for k in bigrams.keys():
        bigrams[k] = makeProbDict(bigrams[k])

    return bigrams



def concordance(wordList):
    print('Building concordance. Lexicon size: ' + str(len(wordList)), file=sys.stderr)
    conc = defaultdict(int)

    for w in wordList:
        conc[w] = conc[w] + 1

    return conc



def makeFsa(wordProbDict, bigramDict):
    fsa = 'F\n\n'
    print('Building FSA.', end='', file=sys.stderr)
    baseProb = str(MIN_PROB / len(wordProbDict.keys()))
    count = 0

    wpd = wordProbDict.items()
    for word, prob in wpd:
        count += 1
        if count % 1000 == 0:
            print('.', end='', file=sys.stderr)

        stateName = ''.join(list(word.split()))
        stateNames[word] = stateName

        # insert transition from initial state => 
        # state corresponding to this word as start of sentence
        if prob == 0:
            fsa = fsa + '(F (' + stateName + '*e* 0.005))\n'
        else:
            fsa = fsa + '(F (' + stateName + '*e* ' + str(prob) + '))\n'

        # insert transitions from this state => other states
        fsa = fsa + '(' + stateName + ' (F *e* 0.005))\n'

        nextWordProbs = bigramDict.get(word)
        if nextWordProbs != None:
            nwp = nextWordProbs.items()
            for nw, p in nwp:
                nextStateName = ''.join(list(nw.split()))
                fsa = fsa + '(' + stateName + ' (' + nextStateName + ' \"' + nw + '\" ' + \
                    str(p - MIN_PROB / len(nwp)) + '))\n'

        fsa = fsa + '\n'

    #print('\nAdding extra transitions.', end='', file = sys.stderr)
    #count = 0
    #for word, prob in wpd:
    #    count += 1
    #    if count % 1000 == 0:
    #        print('.', end='', file=sys.stderr)
    #    for otherWord, junk in wpd:
    #        if word == otherWord:
    #            continue
    #        fsa = fsa + '(' + stateName + ' (' + stateNames[otherWord] + \
    #            ' \"' + otherWord + '\" ' + baseProb + '))\n'

    return fsa



def removeChars(s, c):
    for sep in list(c):
        s = s.replace(sep, ' ')
    return s



def cleanupString(s):
    badchars = []
    for c in s:
        if ord(c) > 127:
            badchars.append(c)
    for c in badchars:
        s.replace(c, '')

    return s



def extractSentences(corpus):
    sentences = re.split(r'[,.?!:;]', corpus)
    return sentences



def extractWords(corpus):
    corpus = str.upper(corpus)

    # Beazley & Jones, Python Cookbook 3e
    words = re.split(r'[,.?!:;\s]\s*', corpus)

    words = [' '.join(list(w)) for w in words if w != '']

    return words



if __name__ == '__main__':
    corpus = ''
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'corpus.txt'
	
    with open(filename) as infile:
        corpus = infile.read()

    if len(sys.argv) > 2:
        if sys.argv[2] == '-f':
            corpus = removeChars(corpus, ' ')
            corpus = corpus.replace('_', ' ')


    outfile = open('wsj.fsa', 'w')

    corpus = removeChars(corpus, '~`@#$%^&*()-+=:;\"[]{}|/\\1234567890')

    vocab = extractWords(corpus)

    bigrams = makeBigrams(extractSentences(corpus))

    conc = concordance(vocab)
    wordProb = makeProbDict(conc)

    fsa = makeFsa(wordProb, bigrams)
    
    print (fsa)
    outfile.write(fsa)


