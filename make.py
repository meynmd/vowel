'''
MakeWordRecognizer(name, word)

takes the name which will be prepended to all state names,
and the word to recognize

returns (first state, accept state, rules)
'''
def MakeWordRecognizer(name, word):
    rec = ''
    for i in range(len(word)):
        # write the string for this transition rule
        rule = '(' + name + str(i) + \
            ' (' + name + str(i + 1) + \
            ' ' + word[i] + '))\n'

        rec = rec + rule

    return (rec, name + '0', name + str(len(word)))



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



language = ['THE', 'AND']
f = MakeLanguageRecognizer(language)
print(f)
