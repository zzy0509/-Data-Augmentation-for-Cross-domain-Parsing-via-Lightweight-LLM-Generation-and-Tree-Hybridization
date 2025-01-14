# -*- coding=utf-8 -*-

from collections import Counter
from typing import Union

from lexical_tree import LexTree

from nltk.tree import Tree

import re


class LexVocab(object):

    def __init__(self, data):
        self.vocab = dict()
        self.unique = set()
        self.initialize(data)

    # def __init__(self, data,data1):
    #     self.vocab = dict()
    #     self.unique = set()
    #     self.initialize(data,data1)

    def __getitem__(self, key):
        if isinstance(key, str):
            return self.vocab.get(key, [])
        else:
            raise TypeError

    def __contains__(self, tree: Tree) -> bool:
        if not isinstance(tree, Tree):
            raise TypeError
        if tree.flatten().pformat(1e6) in self.unique:
            return True
        return False

    def add(self, tree: Tree):
        flat_repr = tree.flatten().pformat(1e6)
        if flat_repr in self.unique:
            # fail to add
            return False
        self.unique.add(flat_repr)
        label = tree.label_repr()
        headword = re.findall(r'\[.*?\]', label)[0][1:-1]
        # if headword.islower() == False:
        #     print(label,headword.lower())
        if self.vocab.get(label, None) is None:
            self.vocab[label] = []
        self.vocab[label].append(tree)
        if headword.islower() == False and headword != headword.lower():
            new_label = re.sub(headword,headword.lower(),label)
            # print(label,headword.lower())
            if self.vocab.get(new_label, None) is None:
                self.vocab[new_label] = []
            self.vocab[new_label].append(tree)
        return True

    def initialize(self, src1: Union[str, list]):
        # read lexical trees
        if isinstance(src1, str):
            with open(src1, 'r', encoding='utf-8') as fr1:
                trees = [Tree.fromstring(line) for line in fr1]
            # with open(src2, 'r', encoding='utf-8') as fr2:
            #     trees2 = [Tree.fromstring(line) for line in fr2]
            #     trees = trees1 + trees2
                trees = [LexTree.const2lex(t, i) for i, t in enumerate(trees)]
        elif isinstance(src1, list):
            trees = src1
        else:
            raise TypeError
        for tree in trees:
            # self.add(tree)
            subtrees = LexTree.get_subtrees(tree)
            for subtree in subtrees:
                if not subtree.replaceable():
                    continue
                self.add(subtree)


    def count_sizes(self):
        print('-------------------------------------')
        print('lexical vocabulary size statistic:')
        print('vocab len: {}'.format(len(self.vocab)))
        counter = Counter({label: len(set([t.pformat(1000) for t in trees])) for label, trees in self.vocab.items()})
        print('total elements: {}'.format(sum(counter.values())))
        print('top 10 common elements:')
        for k, freq in counter.most_common(10):
            print('{} : {}'.format(k, freq))

    def count_frequencies(self):
        """count all sub-trees"""
        print('-------------------------------------')
        print('lexical vocabulary frequency statistic:')
        print('vocab len: {}'.format(len(self.vocab)))
        counter = Counter({label: len(set([t.pformat(1e6) for t in trees])) for label, trees in self.vocab.items()})
        total = len(counter)
        for n in [2, 5, 10]:
            i = 0
            for k, freq in counter.most_common():
                if freq >= n:
                    i += 1
            print('>= {} : {} / {} = {}'.format(n, i, total, i/total))

    
