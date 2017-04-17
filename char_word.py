import sys

def construct_char_word(data_new):
    start_set = set()
    all_set=set()
    for j in range(len(data_new)):
        data=data_new[j]
        count=0
        for i in range(len(data)):
            word = None
            if i == 0:
                next_state = data[i] + '_' + str(i)+'_' + str(j)
                temp_str = '(s ' + '(' + next_state + ' ' + data[i] + ' "<BOS>" ))'
                start_set.add(temp_str)
                # if temp_str not in start_set:
                #     start_set += [temp_str]
                cur_state = next_state
            else:
                next_state = cur_state + data[i] + '_' + str(i) + '_' + str(j)
                if data[i]=='_':
                    word=data.split('_')[count]
                    word = '"'+word+'"'
                    count+=1
                if i==len(data)-1:
                    word = data.split('_')[-1]
                    word = '"'+word+'"'
                    temp_str = '(' + cur_state + ' (' + next_state + ' ' + data[i] + ' ' + word + ' ))'
                    all_set.add(temp_str)
                    # if temp_str not in all_set:
                    #     all_set += [temp_str]
                    cur_state = next_state
                    temp_str = '(' + cur_state + ' ( e *e* *e* ))'
                    all_set.add(temp_str)
                    # if temp_str not in all_set:
                    #     all_set += [temp_str]


                if not word:
                    word='*e*'

                if i!=len(data)-1:
                    temp_str = '(' + cur_state +' ('+next_state+' '+ data[i]+' '+word+' ))'
                    all_set.add(temp_str)

                    # if temp_str not in all_set:
                    #     all_set+=[temp_str]

                    cur_state=next_state












    print('e')
    for temp in start_set:
        print(temp)
    for temp in all_set:
        print(temp)




if __name__ == '__main__':

    data = []
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'corpus_full_formatted_data.txt'
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            line1 = line.split('\n')[0]
            data += [line1.replace(' ', '')]
    print(data)
    construct_char_word(data)
