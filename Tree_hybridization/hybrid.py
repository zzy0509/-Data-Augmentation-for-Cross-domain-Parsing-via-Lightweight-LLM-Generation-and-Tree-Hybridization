import argparse
import copy
import random
from lexical_dataset import HierarchicalDataset
from lexical_vocab import LexVocab
from lexical_tree import LexTree
from nltk.tree import Tree
import re
import json

phrase_use = {}


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



class HybridizationV3(object):

    def __init__(self, dataset, vocab) -> None:
        self.dataset = dataset
        self.vocab = vocab
        self.n_inits = {k: len(v) for k, v in self.dataset.dataset.items()}
        # self.raw_dataset = copy.deepcopy(self.dataset)

    def add(self, tree: Tree, level) -> bool:
        # fail to add
        if not self.vocab.add(tree):
            return False
        self.dataset.add(tree, level)
        return True
        

    def get_alternatives(self, tree: Tree, level: int):
        alternatives = []
        label = tree.label_repr()
        alt_lst = self.vocab[label]
        lst = alt_lst
        headword = re.findall(r'\[.*?\]', label)[0][1:-1]
        if headword.islower() == False and headword != headword.lower():
            new_label = re.sub(headword,headword.lower(),label)
            new_alt_lst = self.vocab[new_label]
            if len(new_alt_lst) > len(alt_lst):
                lst = new_alt_lst
        for alt in lst:
            # can't be replaced
            if not alt.replaceable():
                # print(alt)
                continue
            # Rule 3: can't replace a subtree with the same representation
            if tree.equal(alt):
                continue
            if HierarchicalDataset.hierarchy_split(alt.size()) >= level:
                continue
            alternatives.append(alt)
        return alternatives


    def substitute_random_deep(self, tree, level):

        new_t = tree.copy()

        for i, child in enumerate(tree): 
            if not child.replaceable():
                continue
            alternatives = self.get_alternatives(child, level)
            raw_alters = [alter for alter in alternatives if alter.hybrid_level() == 0]
            hybrid_alters = [alter for alter in alternatives if alter.hybrid_level() != 0]
            if not raw_alters and not hybrid_alters:
                continue
            elif raw_alters and not hybrid_alters:
                alters = raw_alters
            elif not raw_alters and hybrid_alters:
                alters = hybrid_alters
            else:
                if random.random() < 0.5:
                    alters = raw_alters 
                else:
                    alters = hybrid_alters 
            lst = []
            for subtree in alters:
                lst.append(' '.join(subtree.leaves()))
            alter = alters[0]
            if phrase_use[' '.join(alter.leaves())] >= 3:
                continue
            phrase_use[' '.join(alter.leaves())] = phrase_use.get(' '.join(alter.leaves()),0) + 1
            new_t.update(i, alter)
        if new_t != tree and self.add(new_t, level):
            return 1
        return 0

    def substitute(self, tree, level, mode=None):
        if mode == 'random':
            n = self.substitute_random(tree, level)
        elif mode == 'random_deep':
            n = self.substitute_random_deep(tree, level)
        elif mode == 'brute':
            n = self.substitute_brute(tree, level)
        else:
            raise ValueError
        return n

    def hybrid(self, mode=None):
        print('hybrid start !')
        n = 0
        self.dataset.count_sizes()
        self.vocab.count_sizes()
        # from small size to large size
        for level in HierarchicalDataset.hierarchy()[1:]:
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('handle level {} !'.format(level))
            trees = copy.copy(self.dataset[level])
            for tree in trees:
                # print(tree)
                n += self.substitute(tree, level, mode)
        self.dataset.count_sizes()
        self.vocab.count_sizes()
        # print('{} new examples generated !'.format(n))
        print('hybrid end !')
    
    def process(self, tree):
        count = 0
        for s in tree.subtrees(lambda t : t.height() == 2):
            # print(s)
            if count == 0:
                if s[0].islower():
                    s[0] = s[0].capitalize()
            else:
                if s[0].istitle():
                    s[0] = s[0].lower()
            count += 1
        return tree
        


    def output(self, dest: str) -> None:
        with open(dest, 'w') as fw:
            hybrid_dict = dict()
            total_h = 0
            n = 0
            for level in HierarchicalDataset.hierarchy():
                for tree in self.dataset[level]:
                    if not tree.top():
                        continue
                    n += 1
                    h = tree.hybrid_level()
                    if hybrid_dict.get(h, None) is None:
                        hybrid_dict[h] = 0
                    hybrid_dict[h] += 1
                    total_h += h
                    tree_repr = "{}\t{}\n".format(h, tree.one_line())
                    print(n, ' '.join(tree.leaves()))
                    fw.write(tree_repr)
            print('hybrid rate: {} / {} = {}'.format(total_h, n, total_h / n))
            print('number of hybrid level 1 is {} / {} = {}'.format(hybrid_dict[1], n, hybrid_dict[1] / n))


def main():

    parser = argparse.ArgumentParser(
        description='Hybridization.'
    )
    parser.add_argument('--mode', choices=['random', 'brute', 'random_deep'],
                        help='use which mode to augment data')
    parser.add_argument('--input', type=str,
                        help='path to input file')
    parser.add_argument('--add', type=str,
                        help='path to add file')
    parser.add_argument('--output', type=str,
                        help='output file')
    args = parser.parse_args()

    lex_file = args.input
    vocab_file = args.add
    dataset = HierarchicalDataset.build(lex_file)
    vocab = LexVocab(vocab_file)
    processor = HybridizationV3(dataset, vocab)
    processor.hybrid(mode=args.mode)
    processor.output(args.output)



if __name__ == "__main__":
    main()

