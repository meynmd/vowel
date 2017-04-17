# def build_word_char_fst(data):
#     start_sent = []
#     all_sent = []
#     for j in range(len(data)):
#         word = data[j]
#         word1=word.replace(" ", "")
#
#         for i in range(len(word1)):
#             check=0
#             if i==0:
#                 cur_state = word1[i]+'_'+str(j)+'_'+str(i)
#                 start_sent +=['(s ('+cur_state+' '+word1+' '+word1[i]+'))']
#                 check =1
#                 continue
#
#             if i==len(word1)-1:
#                 all_sent+= [  '('+cur_state+' (e'+ ' '+ '*e* '+ word1[i]+' ))'   ]
#                 check=1
#                 continue
#
#             if check==0:
#                 next_state=word1[i]+'_'+str(j)+'_'+str(i)
#                 all_sent += [  '('+cur_state+' ('+next_state + ' '+ '*e* '+ word1[i]+' ))'   ]
#                 cur_state=next_state
#     print('e')
#     for temp in start_sent:
#         print(temp)
#     for temp in all_sent:
#         print(temp)


import sys
import math

def construct_word_character(data_new):
    print('Constructing word-char FSM. Data size: ' + str(len(data_new)), file=sys.stderr)
    
    start = '(s (<BOS> "<BOS>" *e*))'
    end = '(<EOS> (e *e* *e*))'
    start_set=set()
    all_set = set()

    start_set.add(start)
    
    loopcount = 0
    for data in data_new:
        loopcount += 1
        if loopcount % 10 == 0:
            print(str(loopcount / len(data_new) * 100.) + ' percent', file=sys.stderr)
        for i in range(len(data)):
            if i==0:
                current_state='<BOS>'
                nex_state = data+'_'+str(i)
                input_str = '"'+data+'"'
                output_str = data[i]
                temp_str= '(' + current_state + ' (' + nex_state + ' ' + input_str + ' ' + output_str +' ))'

                all_set.add(temp_str)
                # if temp_str not in all_set:
                #     all_set+=[temp_str]

                current_state=nex_state
                continue

            if i==len(data)-1:
                nex_state = data+'__'
                input_str = '*e*'
                output_str = data[i]
                temp_str = '(' + current_state + ' (' + nex_state + ' ' + input_str + ' ' + output_str + ' ))'
                all_set.add(temp_str)
         	#if temp_str not in all_set:
                #   all_set+=[temp_str]
                current_state = nex_state

                nex_state = '<BOS>'
                input_str = '*e*'
                output_str = '_'
                temp_str = '(' + current_state + ' (' + nex_state + ' ' + input_str + ' ' + output_str + ' ))'
                all_set.add(temp_str)
                # if temp_str not in all_set:
                #     all_set+=[temp_str]


                nex_state = '<EOS>'
                input_str = '"<EOS>"'
                output_str = '*e*'
                temp_str = '(' + current_state + ' (' + nex_state + ' ' + input_str + ' ' + output_str + ' ))'
                all_set.add(temp_str)
                # if temp_str not in all_set:
                #     all_set+=[temp_str]





                current_state = nex_state

            if i!=0 and i!=len(data)-1:
                nex_state = data + '_' + str(i)
                input_str = '*e*'
                output_str = data[i]
                temp_str = '(' + current_state + ' (' + nex_state + ' ' + input_str + ' ' + output_str + ' ))'
                all_set.add(temp_str)

                # if temp_str not in all_set:
                #     all_set += [temp_str]

                current_state = nex_state

    print('e')
    for temp in start_set:
        print(temp)
    for temp in all_set:
        print(temp)










if __name__ == '__main__':
    data = []
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = 'corpus_full_formatted_data.txt'
    with open(fname, 'r') as fp:
        for line in fp.readlines():
            line1=line.split('\n')[0]
            temp_data = line1.split('_')
            for word in temp_data:
                if word in data:
                    continue
                else:
                    data+=[word.replace(' ','')]

    construct_word_character(data)



