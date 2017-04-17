import sys
import math
from collections import defaultdict

def counting_bigrams(data):
    onePercent = math.floor(len(data) / 100.)
    loopCount = 0
    count_dict = {}
    for temp in data:
        loopCount += 1
        if loopCount % 10 == 0:
            print(str(loopCount / len(data) * 100.) + ' %', file=sys.stderr)    
        i=0
        j=len(temp)-1
        while i+1<=j:
            if temp[i] not in count_dict:
                count_dict[temp[i]]={}

            if temp[i+1] not in count_dict[temp[i]]:
                count_dict[temp[i]][temp[i+1]]=0
            count_dict[temp[i]][temp[i+1]]+=1
            i=i+1
    return count_dict




def construct_wfst(count_dict,unique_words):
    start_set=[]
    all_set = []
    
    print('Constructing WFST.', file=sys.stderr)
    count = 0

    onePercent = math.floor(len(unique_words) / 100.)
    for cur_state in unique_words:
        count += 1
        if count % 10 == 0:
            print(str(count / len(unique_words) * 100.) + ' %', file=sys.stderr)    
        if cur_state in count_dict:
           # print('I am here')
            #print(cur_state)
            total=sum([count_dict[cur_state][key] for key in count_dict[cur_state]])
            for next_state in count_dict[cur_state]:
                #print(next_state)
                if cur_state=='<BOS>':
                    #print(count_dict[cur_state])
                    #print(total)
                    prob = count_dict[cur_state][next_state]/total
                    temp_str='('+cur_state+' ('+next_state+' '+'"'+cur_state+'" '+'"<BOS>" '+str(round(prob,4))+'))'
                    if temp_str not in start_set:
                        start_set+=[ temp_str ]
                else:
                    try:
                        prob = count_dict[cur_state][next_state]/total
                    except:
                        print('I am here')

                    if next_state=='<EOS>':
                        temp_str='(' + cur_state + ' (' + next_state + ' "' + cur_state + '" "' + cur_state + '" ' + str(prob) + '))'
                        if temp_str not in all_set:
                            all_set += [temp_str ]
                        cur_state_1 = next_state
                        temp_str= '(' + cur_state_1 + ' (e' +   ' *e*' +  ' "' + cur_state_1 + '" ' + str('1') + '))'
                        if temp_str not in all_set:
                            all_set+=[temp_str]
                    else:
                        temp_str='(' + cur_state + ' (' + next_state + ' "' + cur_state + '" "' + cur_state + '" ' + str(prob) + '))'
                        all_set += [temp_str]

    print('e')
    for temp in start_set:
        print(temp)
    for temp in all_set:
        print(temp)





if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'corpus.txt'
    data = []
    with open(filename,'r') as fp:
        for line in fp.readlines():
            line1=line.split('\n')[0]
            temp_data = line1.split('_')
            temp_data=[word.replace(' ','') for word in temp_data]
            data+=[['<BOS>']+temp_data+['<EOS>']]

    print('counting unique words.', file=sys.stderr)
    unique_words=[]
    for temp in data:
        for i in range(len(temp)):
            if temp[i] not in data:
                unique_words+=[temp[i]]


    print('Computing bigrams. There are ' + str(len(unique_words)) + ' unique words.', file=sys.stderr)

    #print(len(unique_words))
    #print(data)
    count_dict=counting_bigrams(data)
    #print(count_dict)
    construct_wfst(count_dict,unique_words)








