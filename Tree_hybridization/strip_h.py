# -*- coding=utf-8 -*-

import argparse


def strip(input, output):
    with open(input, 'r') as fr:
        with open(output, 'w') as fw:
            for line in fr:
                fw.write(line.split('\t')[1])


def main():
    parser = argparse.ArgumentParser(
        description='Hybridization.'
    )
    parser.add_argument('--input', '-i', type=str,
                        help='path to input file')
    parser.add_argument('--output', '-o', type=str,
                        help='output file')
    args = parser.parse_args()

    strip(args.input, args.output)


if __name__ == '__main__':
    main()