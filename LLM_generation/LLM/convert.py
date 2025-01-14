from lexical_tree import LexTree
from nltk.tree import Tree
import re

with open('data_all.pid', 'r', encoding='utf-8') as fr1:
    trees = [line for line in fr1]

f = open(r"data_all_digit.pid","w",encoding="utf-8")


def convert(string):
    print(string)
    t1 = Tree.fromstring(string)
    sentence = t1.leaves()
    for i in range(len(sentence)):
        sentence[i] = sentence[i].lower()
    for s in t1.subtrees():
        l = s.label().split('[')[0]
        headword = s.label().split('[')[1][:-1].lower()
        replacement = '[' + str(sentence.index(headword)+1) + ']'
        s.set_label(l+replacement)

    return t1.pformat(1e7)

for tree in trees:
    f.write(convert(tree)+'\n')

