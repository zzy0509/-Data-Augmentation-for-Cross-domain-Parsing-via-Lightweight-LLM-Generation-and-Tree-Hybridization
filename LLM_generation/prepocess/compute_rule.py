from lexical_tree import LexTree
from nltk.tree import Tree
import re
import pdb
import json
import random

with open('ptb/train_digit.pid', 'r', encoding='utf-8') as fr1:
    trees = [Tree.fromstring(line) for line in fr1]




def extract_rule_with_headword(tree):
    rule = ''
    headword = re.findall(r'\[.*?\]', tree.label())[0]
    rule += tree.label().split('[')[0]
    rule += '->'
    for i in range(len(tree)):
        if re.findall(r'\[.*?\]', tree[i].label())[0] == headword:
            head_label = tree[i].label().split('[')[0]
        rule += tree[i].label().split('[')[0]
        rule += ' '
    rule = '[' + head_label + ']' + rule

    return rule


def extract_rule(tree):
    rule = ''
    rule += tree.label()
    rule += '->'
    for i in range(len(tree)):
        rule += tree[i].label()
        rule += ' '

    return rule


def compute_rule_with_headword_tree(trees):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == 4):
            phrase = ' '.join(s.leaves())
            # phrase = s.pformat(1e8)
            phrase = re.sub(r'\[.*?\]','',phrase)
            rule_lst = []
            for subtree in s.subtrees(lambda t : t.height() > 2):
                rule_lst.append(extract_rule_with_headword(subtree))
            rule_string = ', '.join(rule_lst)
            dict_count[rule_string] = dict_count.get(rule_string,0) + 1
            if rule_string not in rule_dict.keys():
                rule_dict[rule_string] = [phrase]
            else:
                pre = rule_dict[rule_string]
                if phrase not in pre:
                    new = pre + [phrase]
                    rule_dict[rule_string] = new
    # dict_count = sorted(dict_count.items(),  key=lambda d: d[1], reverse=False)

    return (rule_dict,dict_count)

def compute_rule_with_headword(trees):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == 4):
            phrase = ' '.join(s.leaves())
            rule_lst = []
            for subtree in s.subtrees(lambda t : t.height() > 2):
                rule_lst.append(extract_rule_with_headword(subtree))
            rule_string = ', '.join(rule_lst)
            dict_count[rule_string] = dict_count.get(rule_string,0) + 1
            if rule_string not in rule_dict.keys():
                rule_dict[rule_string] = [phrase]
            else:
                pre = rule_dict[rule_string]
                if phrase not in pre:
                    new = pre + [phrase]
                    rule_dict[rule_string] = new
    # dict_count = sorted(dict_count.items(),  key=lambda d: d[1], reverse=False)

    return (rule_dict,dict_count)


def compute_rule(trees):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == 4):
            phrase = ' '.join(s.leaves())
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
    # dict_count = sorted(dict_count.items(),  key=lambda d: d[1], reverse=False)
    # print(dict_count)
    return (rule_dict,dict_count)

def compute_rule_tree(trees):

    rule_dict = {}
    dict_count = {}
    for tree in trees:
        sentence = tree.leaves()
        for s in tree.subtrees(lambda t : t.height() == 4):
            phrase = ' '.join(s.leaves())
            # phrase = s.pformat(1e8)
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

ptb_rule_dict, ptb_rule_count = compute_rule_with_headword_tree(trees)[0], compute_rule_with_headword_tree(trees)[1]



with open("rule_height_4_tree.json","w", encoding='utf-8') as f: ## 设置'utf-8'编码
    f.write(json.dumps(ptb_rule_dict, ensure_ascii=False))