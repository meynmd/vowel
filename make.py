from collections import defaultdict

def split_string(split_str,fsa_dict):
    cur_state = 's0'
    cons_str = None

    for i in range(len(split_str)):
        if split_str[i] in fsa_dict[cur_state]:
            cur_state = fsa_dict[cur_state][split_str[i]]
            continue
        else:
            cons_str = split_str[i:]
            break

    return cons_str,cur_state



def construct_fsa(cons_str,cur_state,fsa_dict,cur_final_state=0):
    state_count=cur_final_state
    for i in range(len(cons_str)):

        if cur_state not in fsa_dict:
            fsa_dict[cur_state] = defaultdict(str)

        if cons_str[i] == ' ':
            fsa_dict[cur_state][cons_str[i]] = cur_state
            continue

        new_state = str(state_count + 1)
        if cons_str[i] not in fsa_dict[cur_state]:
            fsa_dict[cur_state][cons_str[i]] = new_state
        cur_state = new_state
        state_count+=1
    if new_state  not in fsa_dict:
        fsa_dict[new_state]=defaultdict(str)
        fsa_dict[new_state]['eplison'] = 'f_state'
    else:
        fsa_dict[new_state]['eplison'] = 'f_state'
    return fsa_dict,int(new_state)



def check_fsa(cur_str,fsa_dict):
    cur_state = 's0'
    #accepted = True

    for ch in cur_str:
        if ch in fsa_dict[cur_state]:
            cur_state=fsa_dict[cur_state][ch]
            continue
        else:
            break
            accepted=False

    if 'eplison' in fsa_dict[cur_state]:
        accepted = True
    else:
        accepted = False


    return accepted




def convert_fsa_carmel(fsa_dict):

    #fsa_dict={'1': {'A': '2', ' ': '1'}, '3':  {'eplison': 'f_state'}, '2':  {'eplison': 'f_state', 'B': '3', ' ': '2'}, 's0': {'A': '1'},'f_state': {'_': 's0'}}



    print 'f_state'

    for key1 in fsa_dict['s0']:
        if key1=='eplison':
            key1_d = '*e*'
        else:
            key1_d = key1

        print '(', 's0', '(', fsa_dict['s0'][key1], key1_d, '))'


    for key in fsa_dict:
        if key=='s0':
            continue



        for key1 in fsa_dict[key]:
            # if key=='s0':
            #     key_d = '0'
            # else:
            #     key_d = key

            if key1=='eplison':
                key1_d = '*e*'
            else:
                key1_d = key1


            print '(',key,'(',fsa_dict[key][key1],key1_d,'))'


















if __name__ == "__main__":
    data=[]
    with open('vocab','rb') as fp:
        for line in fp.readlines():
            if '\n' in line:
                data+=[line[:-1]]
            else:
                data+=[line]


    fsa_dict = defaultdict(dict)
    fsa_dict['s0']=defaultdict(str)

    f_state=0
    for item in data:
        end_str,end_state=split_string(item,fsa_dict)
        if end_str!=None:
            fsa_dict,f_state=construct_fsa(end_str,end_state,fsa_dict,f_state)

    fsa_dict['f_state']['_'] = 's0'
    convert_fsa_carmel(fsa_dict)










