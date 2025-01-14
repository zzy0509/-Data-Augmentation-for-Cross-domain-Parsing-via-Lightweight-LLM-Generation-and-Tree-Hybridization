# -*- coding=utf-8 -*-

import argparse
from nltk.tree import Tree


def remove(input, output, n, mode='hybrid'):
    n_total = 0
    n_long = 0
    with open(input, 'r') as fr:
        with open(output, 'w') as fw:
            for line in fr:
                n_total += 1
                if mode == 'hybrid':
                    tree_repr = line.split('\t')[1].strip()
                elif mode == 'base':
                    tree_repr = line.strip()
                tree = Tree.fromstring(tree_repr)
                if len(tree.leaves()) > n:
                    n_long += 1
                    continue
                fw.write(line)
    print('number of long sentences > {} : {} / {}'.format(n, n_long, n_total)) 


def main():
    parser = argparse.ArgumentParser(
        description='Hybridization.'
    )
    parser.add_argument('--input', '-i', type=str,
                        help='path to input file')
    parser.add_argument('--output', '-o', type=str,
                        help='output file')
    parser.add_argument('--num', '-n', type=int,
                        help='number of examples to sample')
    parser.add_argument('--mode', type=str, default='hybrid',
                        help='whether to use hybrid or base representation')
    args = parser.parse_args()

    remove(args.input, args.output, args.num, args.mode)
    
if __name__ == '__main__':
    main()