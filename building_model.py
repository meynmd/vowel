


from collections import defaultdict
import numpy as np

import Queue



#A _ H A
#A _ J A
def next_characters_probabilities(cur_state,data,space_done,block):
    str_data = cur_state.split('_')[0]
    if block==0:
        str_data=" ".join(str_data)
        if space_done:
            str_data=str_data+' '
    else:
        if space_done:

            str_data=' '.join(str_data)
            str_data=' '+str_data+' '
        else:
            str_data=' '.join(str_data)
            str_data=' '+str_data


    leng = len(str_data)
    count_dict = defaultdict(int)
    #print 'This is the string data',str_data,len(str_data)
    for temp in data:
        if temp[:leng] == str_data:
            if leng < len(temp):
                ch= temp[leng]
                count_dict[ch]+=1
            else:
                count_dict['*e*']+=1
                # code when string length == cur_state length

    total = sum(count_dict.values())
    prob_dict= {key:float(count_dict[key])/total for key in count_dict }
    #print 'this is the prob',prob_dict
    return prob_dict










def build_wfsa(data_list,wfsa_dict,start_state,sentence_length,block):
    #print '###########################'

    max_len_word=max([len(item) for item in data_list])
    q = Queue.Queue()
    i =0

    first_letters = [data_list[i][0] for i in range(len(data_list))]
    unique_first_letters = list(set(first_letters))
    space = False

    # When there is a space
    if unique_first_letters == [' ']:
        space=True
        first_letters = [data_list[i][1] for i in range(len(data_list))]
        unique_first_letters = list(set(first_letters))


    prob_first_letters = defaultdict(int)
    for temp in first_letters:
        prob_first_letters[temp]+=1

    prob_first_letters={ key:float(prob_first_letters[key])/len(first_letters)  for key in prob_first_letters}

    wfsa_dict[start_state]=defaultdict(tuple)





    for temp in unique_first_letters:
        temp_state = temp + '_' + str(sentence_length) + '_' + str(block)
        wfsa_dict[start_state][temp_state] = (temp,prob_first_letters[temp])

        wfsa_dict[temp_state] = defaultdict(tuple)

        q.put(temp_state)


    space_done= False
    while not q.empty():

        cur_state = q.get()

        prob_next_states=next_characters_probabilities(cur_state,data_list,space_done,block)
        #print 'Prb',prob_next_states.keys()
        if prob_next_states.keys()==[' ']:
            #print 'I ma here'
            space_done = True

            prob_next_states = next_characters_probabilities(cur_state, data_list,space_done,block)



        #This is the case when the sentence ends
        #print prob_next_states
        for key in prob_next_states:
            if '*e*'==key:
                wfsa_dict[cur_state]['e_'+str(sentence_length)+'_'+str(block)] = (key,prob_next_states[key])
                continue
            # Not sure what to write current
            next_state=cur_state.split('_')[0]+ str(key) +'_' + str(sentence_length) + '_' + str(block)
            wfsa_dict[cur_state][next_state] = (key,prob_next_states[key])
            q.put(next_state)


    return wfsa_dict




#(0 (A A))
# 'e_1_0': {'end_fsa': ('*e*', 1.0)},
def construct_wfsa_carmel(wfsa_dict):
    start_data=[]
    all_data=[]
    for key in wfsa_dict:
        for key1 in wfsa_dict[key]:
            #print key,wfsa_dict[key]


            temp_str = '('+str(key)+' ('+str(key1)+' '+str(wfsa_dict[key][key1][0])+' '+str(wfsa_dict[key][key1][0])+' '+str(wfsa_dict[key][key1][1])+'))'
            if str(key)=='start_fsa':
                start_data+=[temp_str]
            else:
                all_data+=[temp_str]

    print 'end_fsa'
    for temp in start_data:
        print temp

    for temp in all_data:
        print temp



















if __name__ == "__main__":
    data=[]
    with open('strings','rb') as fp:
        for line in fp.readlines():
            if '\n' in line:
                data+=[line[:-1]]
            else:
                data+=[line]
    #print data
    new_data = []
    for temp in data:

        # print temp
        if temp[-1]!=' ':
            new_data+=[temp+' ']
        else:
            new_data+=[temp]

    data = new_data
    #data = ['M','MY','MYN']
    data_dict  = defaultdict(list)

    wfsa_dict = defaultdict(dict)

    for temp in data:
        leng=len(temp.split('_'))
        data_dict[leng]+=[temp.split('_')]
    data_dict={key:np.array(data_dict[key])for key in data_dict}
    max_len=max(data_dict.keys())
    min_len=min(data_dict.keys())
    f_state = 0
    for i in range(min_len,max_len+1):
        if i in data_dict:
            data_array=data_dict[i]
            (x,y) = data_array.shape

            for j in range(y):
                #print j
                #print y
                #print list(data_array[:,j])
                start_state = 's_'+str(i)+'_'+str(j)
                wfsa_dict= build_wfsa(list(data_array[:,j]),wfsa_dict,start_state,i,j)
                if j<y-1:
                    final_state=str('e_')+str(i) + '_' + str(j)
                    wfsa_dict[final_state]=defaultdict(tuple)
                    wfsa_dict[final_state]={str('s_')+str(i)+'_'+str(j+1): ('_',1)}

    #Starting states
    wfsa_dict['start_fsa'] = defaultdict(tuple)
    norm=len(data_dict)
    for key in data_dict:
        wfsa_dict['start_fsa']['s_'+str(key)+'_0'] = ('*e*',float(1)/norm)

    #End States

    for key in data_dict:
        wfsa_dict['e_'+str(key)+'_'+str(key-1)]['end_fsa'] = ('*e*',float(1)/norm)




    #print dict(wfsa_dict)
    construct_wfsa_carmel(wfsa_dict)











