
# delete repeat sentences from a sentence list
def delete_repeat_sentence(input_all, input, output):
    new_sentences = set()
    with open(input_all, 'r') as fr1:
        fr1 = fr1.read().split('\n')
        with open(input, 'r') as fr2:
            fr2 = fr2.read().split('\n')
            with open(output, 'w') as fw:
                for sentence in fr1:
                    print(sentence, sentence in fr2)
                    if sentence not in fr2:
                        new_sentences.add(sentence)
                        fw.write(sentence+'\n')

        
