import sys

def makeTransitions(word, name):
    output = ''
    count = 0

    output = '(F (' + name + '_' + '0 *e*))\n'
    currentState = name + '_' + '0'

    for letter in word:
        count += 1
        if letter == ' ' or letter == '\n':
            continue

        if count < len(word):
            nextState = name + '_' + str(count)
            output = output + '(' + currentState + ' (' + nextState + ' ' + letter + '))\n'
            currentState = nextState
        else:
            output = output + '(' + currentState + ' (F ' + letter + '))\n'

    return output


if __name__ == '__main__':
    txt = ''
    with open('vocab.small', 'r') as infile:
        txt = infile.read()
    
    words = txt.split('\n')
    fsa = 'F\n\n'
    count = 0
    for word in words:
        count += 1
        if count % 100 == 0:
            print('.', end='', file=sys.stderr)	    
        word = word.strip()
        fsa = fsa + makeTransitions(word, str(count)) + '\n'

    print(fsa)
