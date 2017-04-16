import re
import sys
from collections import defaultdict


'''
converts concordance-style dictionary into dictionary from
key => (# of occurrences) to
key => (occurrences / # of keys in dict)
'''
def makeProbDict(dictionary):
    dictType = type(list(dictionary.values())[0])
    probDict = defaultdict(dictType)
    probDict = {}
    ks = dictionary.keys()

    for k in ks:
        probDict[k] = dictionary[k] / len(ks)

    return probDict


'''
bigrams = makeBigrams(corpus)

takes a string consisting of sentences from which to extract bigrams

returns bigram model represented as dictionary of
(string, string) => # of occurrences
'''
def makeBigrams(sentences):
    sentences = [s for s in sentences if s != '']
    bigrams = defaultdict(int)

    # split sentences into words
    for s in sentences:
        s = str.upper(s)
        #s = re.split(r'[@><#$%^&\*+_=}{/)(\",\s]\s*', s)

        s = re.split(r'[,.?!\s]\s*', s)
        #if len(s) < 2:
        #    bigrams[(s, '')] = bigrams[(s, '')] + 1
        #    continue

        # get each pair of consecutive words in each sentence
        for i in range(len(s) - 1):
            w1 = removeChars(s[i].strip(), '!@#$%^&*()-=+{}<>/\\~\"')
            w2 = removeChars(s[i + 1].strip(), '!@#$%^&*()-=+{}<>/\\~\"')
            #if w1 == None or w2 == None:
            #    continue
	    
            if len(w1) == 0 or len(w2) == 0:
                continue	    
            w1 = ' '.join(list(w1))
            w2 = ' '.join(list(w2))
            if not (s[i].isalpha() and s[i+1].isalpha()):
                print(w1, ' ', w2, ' is not alpha', file=sys.stderr)
                continue
            b = (w1, w2)
            bigrams[b] = bigrams[b] + 1

    # record probability of each pair
    bigrams = makeProbDict(bigrams)

    return bigrams



def removeChars(string, seps):
    #print('before: ', string)
    for s in list(seps):
        string = string.replace(s, '')
    return string

def extractSentences(corpus):
    sentences = re.split(r'[@><#$%^&\*-+=}{/)(\".?!:;]', corpus)
    return sentences



def extractWords(corpus):
    corpus = str.upper(corpus)

    # Beazley & Jones, Python Cookbook 3e
    words = re.split(r'[)(.?!:;\s]\s*', corpus)

    words = [' '.join(list(w)) for w in words if w != '']

    return words



def concordance(wordList):
    conc = defaultdict(int)

    for w in wordList:
        conc[w] = conc[w] + 1

    return conc



def makeFsa(wordProbDict, bigramDict):
    fsa = 'F\n\n'
    count = 0
    print('making FSA. Lexicon size: ', len(wordProbDict), file=sys.stderr)
    for word, prob in wordProbDict.items():
        count += 1
        if count % 100 == 0:
            print('.', file=sys.stderr)
        # insert transition from initial state => 
        # state corresponding to this word as start of sentence
        stateName = ''.join(list(word.split()))
        fsa = fsa + '(F (' + stateName + ' ' + word + ' ' + str(prob + 0.05) + '))\n'
        fsa = fsa + '(F (' + stateName + ' ' + word + ' _ '+ ' ' + str(prob + 0.05) + '))\n'
        fsa = fsa + '(' + stateName + ' (F *e* 0.005))\n'

        # insert transitions corresponding to bigrams in dictionary
        bigs = [((w1, w2), p) for ((w1, w2), p) in bigramDict.items() if w1 == word]
        for ((w1, w2), p) in bigs:
            nextStateName = ''.join(list(w2.split()))
            fsa = fsa + '(' + stateName + ' (' + nextStateName + ' ' + w2 + ' ' + str(p + 0.05) + '))\n'
            #fsa = fsa + '(' + stateName + ' (' + nextStateName + ' ' + w2 + ' _ ' + ' ' + str(p) + '))\n'
        fsa = fsa + '\n'

    return fsa



if __name__ == '__main__':
    corpus = ''
    with open(sys.argv[1], 'r') as corpusFile:
        corpus = corpusFile.read()
        #for line in corpusFile.readlines():
        #    line = line.strip()
        #    print(line)
        #    corpus += line
    #corpus = '.'.join(corpus)	
    
    #print(corpus)
    
    corpus = removeChars(corpus, '!@$%^&*()-+1234567890<>{}[]|;:,.?!/~\"')

    vocab = extractWords(corpus)

    bigrams = makeBigrams(extractSentences(corpus))

    conc = concordance(vocab)
    wordProb = makeProbDict(conc)

    fsa = makeFsa(wordProb, bigrams)
    
    print (fsa)
