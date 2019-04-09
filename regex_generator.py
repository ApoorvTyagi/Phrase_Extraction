import pandas as pd
from collections import Counter
import re


def main_regex_generator(path):
    data = pd.read_csv(path, header=0, delimiter="\t", quoting=3)
    list_sent = list(data['sent'])
    list_labels = list(data['label'])

    mega_list_label=[]
    for idx,label in enumerate(list_labels):
        if label=='Not Found':
            pass
        else:
            mega_list_label.append([list_sent[idx], label])
    some_list = []
    for i in mega_list_label:
        name = i[1]
        name = re.sub('[^A-Za-z0-9]+', ' ', name)
        sub = '(\w*)\W*('+name+')\W*(\w*)'
        str1 = i[0]
        for i in re.findall(sub, str1, re.I):
            some_list.append([" ".join([x for x in i if x != ""]), name])
    some_pattern_list = []
    for double_list in some_list:
        if double_list[1] in double_list[0]:
            some_pattern_list.append(double_list[0].replace(double_list[1], " "))
        else:
            pass
    pattern_list1 = ((Counter(some_pattern_list)).most_common())#converts the Counter dictutionary to list of tuples (pattern,freq)
    pattern_list = [tup[0] for tup in pattern_list1]#create a list of patterns
    ###### identifing patterns with two words on the left ######
    some_new_list = []
    for i in mega_list_label:
        name = i[1]
        name = re.sub('[^A-Za-z0-9]+', ' ', name)
        sub = '(\w*)\W*(\w*)\W*('+name+')'
        str1 = i[0]
        for i in re.findall(sub, str1, re.I):
            some_new_list.append([" ".join([x for x in i if x != ""]), name])

    some_pattern_list_new = []
    for double_list in some_new_list:
        if double_list[1] in double_list[0]:
            some_pattern_list_new.append(double_list[0].replace(double_list[1], " "))
        else:
            pass

    pattern_list2 = ((Counter(some_pattern_list_new)).most_common())
    pattern_list_2 = [tup[0] for tup in pattern_list2]
    len_2_words=int((len(pattern_list_2))*.40)



    target = open('regex_matcher.py', 'a')
    target.truncate()
    target.write(
        '''
import re
def main_regex_matcher(path_test):
    master_list=[]
    sent_list=[]
    data = open(path_test,'r')
    for text in data:
        found = 0
        small_master_list=[]
        sent_list.append(text)
    ''')
    target.write('\n')
    target.close()
    for pat in pattern_list:
        boundaries = pat.split()
        if len(boundaries) == 2:
            target = open('regex_matcher.py','a')
            target.write('        m = re.search('+"' "+boundaries[0]+' '+'(.+?)'+' '+boundaries[1]+" '"+', text)')
            target.write('\n')
            target.write('        if m:')
            target.write('\n')
            target.write('            found = m.group(1)')
            target.write('\n')
            target.write('            small_master_list.append(found)')
            target.write('\n')
            target.close()
        else:
            pass
    for pat in pattern_list_2[:len_2_words]:
        boundaries=pat.split()
        if len(boundaries) == 2:
            target = open('regex_matcher.py','a')
            target.write('        m = re.search('+"' "+boundaries[0]+' '+boundaries[1]+' (.*)'+"'"+', text)')
            target.write('\n')
            target.write('        if m:')
            target.write('\n')
            target.write('            found = m.group(1)')
            target.write('\n')
            target.write('            small_master_list.append(found)')
            target.write('\n')
            target.close()
        else:
            pass

    target = open('regex_matcher.py', 'a')
    target.write(
        '''
        if found==0 : # if none of the patterns match give it as Not found
            small_master_list.append('Not Found')
        master_list.append(small_master_list)

    no_no_words=['on','for','to','at','by'] # list of words which if occured in the output will be penalised while giving a score
    final_output=[]
    ############ selecting one from the options
    for options in master_list:
        if len(options)==1:
            final_output.append(options[0])#if only one pattern extracted use it 
        else:
            sent_score_list=[] # else score all the options to select the best one
            for option in options:
                l=option.split()
                score = len(l)
                for word in l:
                    if word in no_no_words:
                        score = score -3 #penalise the no_no_words
                    else:
                        pass
                sent_score_list.append(score)
            m = max(sent_score_list)
            indx=[i for i, j in enumerate(sent_score_list) if j == m] # returns a list of all the index which have max score
            index = indx[-1]#pick the last element as an index 
            final_output.append(options[index])

    tups=zip(sent_list, final_output)
    final_list = [list(l) for l in tups]

    for small_list in final_list:
        target = open("output.txt", "a")
        target.write('\\n')
        target.write(' '.join(small_list[0].split())+'\\t'+small_list[1])
        target.write('\\n')
        target.close()
    return(final_output)
    ''')
    target.write('\n')
    target.close()
