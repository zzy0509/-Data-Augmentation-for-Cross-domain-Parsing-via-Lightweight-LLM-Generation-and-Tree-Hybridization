import argparse
import copy
import random
import re
from lexical_dataset import HierarchicalDataset
from lexical_vocab import LexVocab
from lexical_tree import LexTree
from nltk.tree import Tree

with open('ptb/train.pid', 'r', encoding='utf-8') as train:
    train_trees = [Tree.fromstring(line) for line in train]


with open('review/data_all.pid', 'r', encoding='utf-8') as fr1:
    trees = [line for line in fr1]


f = open(r"review/data_all_rule.pid","w",encoding="utf-8")


def extract_rule(tree):
    rule = ''
    rule += tree.label()
    rule += '->'
    for i in range(len(tree)):
        rule += tree[i].label()
        rule += ' '

    return rule


def compute_rule(trees,h):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == h):
            phrase = ' '.join(s.leaves())
            rule_lst = []
            for subtree in s.subtrees(lambda t : t.height() > 2):
                rule_lst.append(extract_rule(subtree))
            rule_string = ', '.join(rule_lst)
            dict_count[rule_string] = dict_count.get(rule_string,0) + 1
            if rule_string not in rule_dict.keys():
                rule_dict[rule_string] = [phrase]
            else:
                pre = rule_dict[rule_string]
                if phrase not in pre:
                    new = pre + [phrase]
                    rule_dict[rule_string] = new
    return (rule_dict,dict_count)


def compute_rule_tree(trees,h):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == h):
            # phrase = ' '.join(s.leaves())
            phrase = s.pformat(1e8)
            rule_lst = []
            for subtree in s.subtrees(lambda t : t.height() > 2):
                rule_lst.append(extract_rule(subtree))
            rule_string = ', '.join(rule_lst)
            # print(rule_string)
            dict_count[rule_string] = dict_count.get(rule_string,0) + 1
            if rule_string not in rule_dict.keys():
                rule_dict[rule_string] = [phrase]
            else:
                pre = rule_dict[rule_string]
                if phrase not in pre:
                    new = pre + [phrase]
                    rule_dict[rule_string] = new

    return (rule_dict,dict_count)

height = 0
ptb_rule_count_3 = compute_rule_tree(train_trees,3)[1]
ptb_rule_count_4 = compute_rule_tree(train_trees,4)[1]
ptb_rule_count_5 = compute_rule_tree(train_trees,5)[1]
ptb_rule_count_6 = compute_rule_tree(train_trees,6)[1]


def compute(tree, height):
    total_num = 0
    count = 0
    if height == 3:
        dic = ptb_rule_count_3
    elif height == 4:
        dic = ptb_rule_count_4
    elif height == 5:
        dic = ptb_rule_count_5
    elif height == 6:
        dic = ptb_rule_count_6
    for s in tree.subtrees(lambda t : t.height() == height):
        total_num += 1
        rule_lst = []
        for subtree in s.subtrees(lambda t : t.height() > 2):
            rule_lst.append(extract_rule(subtree))
        rule_string = ', '.join(rule_lst)
        if rule_string in dic:
            count += dic[rule_string]

    return count/total_num



data_num = 0
c = 0
for data in trees:
    flag = True
    data = re.sub(r'\[.*?\]', '',data)
    tree = Tree.fromstring(data)
    score = 0
    for h in range(3, min(tree.height()+1,5)):
        
        if h == 3 and compute(tree,h) < 50:
            c += 1
            flag = False
        elif h == 4 and compute(tree,h) <= 1:
            flag = False
    if flag:
        data_num += 1
        f.write(tree.pformat(1e6)+'\n')
    
print(data_num)