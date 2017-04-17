def build_word_char_fst(data):
    start_sent = []
    all_sent = []
    for j in range(len(data)):
        word = data[j]
        word1=word.replace(" ", "")

        for i in range(len(word1)):

            if i==0:
                cur_state = word1[i]+'_'+str(j)
                start_sent +=['(s ('+cur_state+' '+word1+' '+word1[i]+'))']

                continue

            if i==len(word1)-1:
                all_sent+= [  '('+cur_state+' (e'+ ' '+ '*e* '+ word1[i]+' ))'   ]
                continue


            next_state=word1[i]+'_'+str(j)
            all_sent += [  '('+cur_state+' ('+next_state + ' '+ '*e* '+ word1[i]+' ))'   ]
            cur_state=next_state
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

    build_word_char_fst(data)
