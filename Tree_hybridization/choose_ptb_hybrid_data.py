import argparse
import copy
import random
from lexical_dataset import HierarchicalDataset
from lexical_vocab import LexVocab
from lexical_tree import LexTree
from nltk.tree import Tree

with open('ptb/train_digit.pid', 'r', encoding='utf-8') as fr1:
    trees = [line for line in fr1]

dictionary = open(r"ewt/email/dictionary.txt","r",encoding="utf-8")
dictionary = dictionary.read().split('\n')

f = open(r"ewt/email/data/ptb","w",encoding="utf-8")


data_num = 0
for data in trees:
    tree = Tree.fromstring(data)
    word_lst = tree.leaves()
    count = 0
    for word in word_lst:
        if word in dictionary:
            count += 1
    if  len(word_lst)-count <= 3 and count/len(word_lst) > 0.8:
        data_num += 1
        f.write(data)
print(data_num)