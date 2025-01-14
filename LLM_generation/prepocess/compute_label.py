from lexical_tree import LexTree
from nltk.tree import Tree
import json

dictionary = open(r"dictionary.txt","r",encoding="utf-8")
dictionary = dictionary.read().split('\n')

with open('ptb/train_digit.pid', 'r', encoding='utf-8') as fr1:
    trees = [Tree.fromstring(line) for line in fr1]



word_dict = {}
for tree in trees:
    sentence = tree.leaves()
    for s in tree.subtrees(lambda t : t.height() == 2):
        word = s[0]
        if word.istitle():
            word = word.lower()
        if word in dictionary:
            label = s.label().split('[')[0]
            if word not in word_dict.keys():
                word_dict[word] = {}
                word_dict[word][label] = 1
            else:
                word_dict[word][label] = word_dict[word].get(label,0) + 1

# 保留主要词性
for word in word_dict.keys():
    label_dict = word_dict[word]
    if len(label_dict) == 1:
        continue
    new_label_dict = {}
    JJ = VB = NN = 0
    for l in label_dict.keys():
        if l[:2] == 'JJ':
            JJ += label_dict[l]
        elif l[:2] == 'VB':
            VB += label_dict[l]
        if l[:2] == 'NN':
            NN += label_dict[l]
    if JJ > VB and JJ > NN:
        for l in label_dict.keys():
            if l[:2] != 'NN' and l[:2] != 'VB':
                new_label_dict[l] = label_dict[l]
    elif VB > JJ and VB > NN:
        for l in label_dict.keys():
            if l[:2] != 'NN' and l[:2] != 'JJ':
                new_label_dict[l] = label_dict[l]
    elif NN > JJ and NN > VB:
        for l in label_dict.keys():
            if l[:2] != 'NN' and l[:2] != 'VB':
                new_label_dict[l] = label_dict[l]
    if new_label_dict != {}:
        word_dict[word] = new_label_dict
    
        
label_dict = {}
for word in word_dict.keys():
    for label in word_dict[word].keys():
        if label not in label_dict.keys():
            label_dict[label] = [word]
        else:
            pre_word_lst = label_dict[label]
            if word not in pre_word_lst:
                new_word_lst = pre_word_lst + [word]
                label_dict[label] = new_word_lst

for word in word_dict.keys():
    for label in word_dict[word].keys():
        if label not in label_dict.keys():
            label_dict[label] = [word]
        else:
            pre_word_lst = label_dict[label]
            if word not in pre_word_lst:
                new_word_lst = pre_word_lst + [word]
                label_dict[label] = new_word_lst


with open("label.json","w", encoding='utf-8') as f: ## 设置'utf-8'编码
    f.write(json.dumps(label_dict, ensure_ascii=False))  