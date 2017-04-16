import sys
import re

lineSeparators = r'[:;.?!]'
excludeChars = '\'1234567890,\"`~@#$%^&*()[]{}<>-+=|\\'   # to be excluded from text

def removeChars(s, c):
    for sep in list(c):
        s = s.replace(sep, '')
    return s

if __name__ == '__main__':
    text = ''

    #with open(sys.argv[1], 'r') as infile:
    with open('corpus.txt', 'r') as infile:
        text = infile.read()
    
    # clean up chars we don't want, and split into sentences/phrases (lines)
    text = str.upper(text)
    text = removeChars(text, excludeChars)
    lines = re.split(lineSeparators, text)

    # reformat the text
    output = ''
    for i in range(len(lines)):
        line = lines[i]

        if len(line) > 1:
            words = line.split()
            spacedWords = []
            for word in words:
                if len(word) < 2 and word != 'I' and word != 'a':
                    continue
                else:
                    spacedWords.append(' '.join(list(word)))

            output = output + ' _ '.join(spacedWords)

        else:
            if i > 0:
                output = output + ' _ ' + line
        output += '\n'

    print (output)

