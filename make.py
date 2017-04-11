import sys

'''
MakeWordRecognizer(name, word)

takes the name which will be prepended to all state names,
and the word to recognize

returns (first state, accept state, rules)
'''
def MakeWordRecognizer(name, word):
    rec = ''
    count = 0
    for c in word:
        if c == ' ' or c == '\n':
	    continue

        count += 1

        # write the string for this transition rule
        rule = '(' + name + str(count) + \
            ' (' + name + str(count + 1) + \
            ' ' + c + '))\n'

        rec = rec + rule

    return (rec, name + '1', name + str(count + 1))



'''
MakeLanguageRecognizer(words)

takes words, a list of words in the language to be recognized

returns a FSA for that list of words
'''
def MakeLanguageRecognizer(words):
    fsa = 'F\n'
    fsa = fsa + '(S (S _))\n'
    count = 0
    for word in words:
        #print 'processing word ' + word + '...'
        count += 1
        wr = MakeWordRecognizer(str(count) + '_', word)
        wordRec = wr[0]
        initState = wr[1]
        finalState = wr[2]
        fsa = fsa + '(S (' + initState + ' *e*))\n'
        fsa = fsa + wordRec
        fsa = fsa + '(' + finalState + ' (S *e*))\n'
    
    fsa = fsa + '(S (F *e*))\n'
    return fsa

lines = sys.stdin.readlines()
language = MakeLanguageRecognizer(lines)
print(language)
