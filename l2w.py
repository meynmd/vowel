def makeTransitions(word, name):
    output = ''
    count = 0

    output = '(F (' + name + '_' + '0 *e* *e*))\n'
    currentState = name + '_' + '0'
    word = word.replace(' ', '')
    
    for letter in word:
        count += 1
        if letter == ' ' or letter == '\n':
            continue

        if count < len(word):
            nextState = name + '_' + str(count)
            output = output + '(' + currentState + ' (' + nextState + ' ' + letter + ' *e*))\n'
            currentState = nextState
        else:
            output = output + '(' + currentState + ' (F ' + letter + ' \"' + word + '\"))\n'

    return output


if __name__ == '__main__':
    txt = ''
    with open('corpus_output.txt', 'r') as infile:
        txt = infile.read()
    
    words = txt.split('\n')
    fst = ''
    count = 0
    for word in words:
        count += 1
        word = word.strip()
        fst = fst + makeTransitions(word, str(count)) + '\n'

    print(fst)
