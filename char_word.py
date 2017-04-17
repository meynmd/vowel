

def build_char_word_fst(data):
    start_sent = []
    all_sent = []
    for word in data:
        cur_state = None
        for i in range(len(word)):
            if i ==0:
                #(0 ( 0 A *e*))
                temp_1 = '(s (' + word[i] + ' ' + word[i] + ' *e*' + '))'
                if temp_1 not in start_sent:
                    start_sent += [temp_1]
                cur_state = word[i]
            else:
                if word[i]==' ':
                    continue
                else:
                    next_state = cur_state+word[i]
                    temp_2 ='('+cur_state+' ('+next_state + ' '+ word[i]+' *e*'+' ))'
                    if temp_2 not in all_sent:
                        all_sent+=[ temp_2 ]
                    cur_state=next_state


        if cur_state:
            all_sent += ['( '+cur_state+ ' (e'+' *e* '+cur_state+' ))']
    print('e')
    for temp in start_sent:
        print(temp)
    for temp in all_sent:
        print(temp)









if __name__ == '__main__':

    data = []
    with open('corpus_output.txt','r') as fp:
        for line in fp.readlines():
            line1=line.split('\n')[0]
            temp_data = line1.split('_')
            for word in temp_data:
                if word in data:
                    continue
                else:
                    data+=[word.strip()]

    build_char_word_fst(data)
