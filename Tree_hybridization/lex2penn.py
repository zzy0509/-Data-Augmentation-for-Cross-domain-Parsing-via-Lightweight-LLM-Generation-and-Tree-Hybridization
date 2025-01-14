# -*- coding=utf-8 -*-

import argparse

from lexical_tree import LexTree

from nltk.tree import Tree


def lex2penn(src: str, tgt: str):
    with open(src, 'r', encoding='utf-8') as fr:
        trees = [Tree.fromstring(line)[0] for line in fr]
    trees = [LexTree.const2lex(t, i) for i, t in enumerate(trees)]
    with open(tgt, 'w') as fw:
        for tree in trees:
            tree_repr = "(TOP {})\n".format(tree.pformat(1e6))
            fw.write(tree_repr)


def main():
    parser = argparse.ArgumentParser(
            description='Hybridization.'
    )
    parser.add_argument('--input', '-i', type=str,
                        help='path to input file')
    parser.add_argument('--output', '-o', type=str,
                        help='output file')
    args = parser.parse_args()

    lex2penn(args.input, args.output)


if __name__ == '__main__':
    main()