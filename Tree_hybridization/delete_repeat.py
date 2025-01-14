import argparse


# delete repeat sentences from a sentence list
def delete_repeat_sentence(input, output):
    new_sentences = set()
    n_repeat = 0
    with open(input, 'r') as fr:
        with open(output, 'w') as fw:
            for sentence in fr:
                if sentence not in new_sentences:
                    new_sentences.add(sentence)
                    fw.write(sentence)
                else:
                    print(sentence)
                    n_repeat += 1
    print('number of repeat sentences: {} / {}'.format(n_repeat, n_repeat + len(new_sentences)))
        

def main():
    parser = argparse.ArgumentParser(
        description='Hybridization.'
    )
    parser.add_argument('--input', '-i', type=str,
                        help='path to input file')
    parser.add_argument('--output', '-o', type=str,
                        help='output file')
    args = parser.parse_args()

    delete_repeat_sentence(args.input, args.output)


if __name__ == '__main__':
    main()