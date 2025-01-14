import re
import random
import openai
from nltk.tree import Tree
from retrying import retry
import json


def replace(prompt):
    while True:
        try:
            message = [{'role':'user','content':prompt}]
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages = message,
                max_tokens=2000,
                temperature=0.8,
                stop=None)
            generated_text = response.choices[0].message.content
            break
        except:
            pass

    return generated_text

with open("/prepocess/ewt/reviews/label.json","r", encoding='utf-8' ) as f_label:
    label_dict = json.load(f_label)

with open("/prepocess/ewt/reviews/rule_height_5.json","r", encoding='utf-8'  ) as f_rule:
    rule_dict = json.load(f_rule)


def extract_rule(tree):
    rule = ''
    rule += tree.label()
    rule += '->'
    for i in range(len(tree)):
        rule += tree[i].label()
        rule += ' '

    return rule


def compute_rule(tree):

    rule_lst = []
    for subtree in tree.subtrees(lambda t : t.height() > 2):
        rule_lst.append(extract_rule(subtree))
    rule_string = ', '.join(rule_lst)

    return rule_string



def generate_CoT(tree):

    label_to_phrase={'ADJP': 'adjective phrase', 'ADVP': 'adverb phrase', 'CONJP': 'conjunction phrase', 
                     'FRAG': 'fragment phrase', 'INTJ': 'interjection',
                    'NAC': 'non-constituent', 'NP': 'noun phrase', "NX": "head noun phrase",
                    'PP': 'prepositional phrase', 'PRN': 'parenthetical.', 'PRT': 'particle',
                    'QP': 'quantifier phrase', 'RRC': 'reduced relative clause','UCP': 'unlike coordinated phrase', 
                    'VP': 'verb phrase','WHADJP': 'wh-adjective phrase', 'WHADVP': 'wh-adverb phrase',
                    'WHNP': 'wh-noun phrase','WHPP': 'wh-prepositional phrase', 'X': 'unknown phrase',
                    'S': 'simple clause', "SBAR": "subordinating clause", "SBARQ": "wh-subordinating clause",
                    "SINV": "inverted clause", "SQ": "interrogative clause", "NNS": "plural noun", 
                    "IN": "preposition", "JJ": "adjective", "NN": "singular noun", "VBD": "past tense verb", 
                    "PRP$": "possessive pronoun", "DT": "determiner", "TO": "infinitive verb phrase",
                    "NNP": "proper noun", "NNPS": "plural proper noun", "VB": "base form verb", 
                    "POS":"possessive noun", "VBG": "present participle verb", "QP": "quantifier phrase",
                    "$": "united states dollar", "CD": "Cardinal Number","RB": "adverb", "RBR":"comparative adverb",
                    "CC":"coordinating conjunction", "JJR":"comparative adjective", "PRP":"presonal pronoun", 
                    "MD":"modal verb", "WDT":"wh-determiner", ",":",",".":".","``":"``","''":"th ''",
                    "FW":"foreign word","VBZ":"third preson singular present tense verb", "WP":"wh-pronoun",
                    "RP":"particle",":":":","VBP":"verb base form present tense","VBN":"past participle verb",
                    "PDT":"pre-determiner","JJS":"superlative adjective","RBS":"superlative adverb",
                    "EX":"existential sentence", "WRB":"wh-adverb","-LRB-":"(","-RRB-":")","#":"#",
                    "SYM":"symbol", "UH":"interjection"}

    cot = ''
    while len(tree) == 1:
        tree = tree[0]

    
    for s in tree.subtrees(lambda t : t.height() > 3):
        for i in range(len(s)):
            if len(s[i]) == 1 and s[i].height()>2:
                s[i] = s[i][0]


    new_rule = compute_rule(tree)
    for s in tree.subtrees(lambda t : t.height() > 2):
        lst = []
        string = ''
        for i in range(len(s)):
            lst.append(label_to_phrase[s[i].label()]+ ' "' + ' '.join(s[i].leaves()) + '" ')
        string = 'and '.join(lst)
        string += 'combine and get ' + label_to_phrase[s.label()] + ' "' + ' '.join(s.leaves()) + '" ' + '\n'
        cot = string + cot
    
    return (new_rule, cot)

f_generate = {}
for rule in rule_dict.keys():

    present_rule = rule+':'+rule_dict[rule][0]
    generate_phrase = []

    word_lst = []
    for tree in rule_dict[rule]:
        t = Tree.fromstring(tree)
        word_lst += t.leaves()

    for time in range(20):
        prompt = 'As a language assistant, you excel at selecting appropriate word from the vocabulary and creating phrases based on the grammar rules.\nPlease strictly observe the constraints. 1. The words in the phrase do not need to be exclusively from the vocabulary, but they must follow the given grammar rules and make sense logically. 2. The phrase does not have to be a complete sentence. 3. The generated phrase must be different from the example. 4. The parts of speech of the words in the vocabulary are consistent, so you can only use one word from the vocabulary.\nGrammar rules : '
        number = len(rule_dict[rule])
        if number > 5:
            subtree_lst = random.choices(rule_dict[rule], k = 5)
        else:
            subtree_lst = rule_dict[rule]
        example_lst = []
        for i in subtree_lst:
            example_lst.append(' '.join(Tree.fromstring(i).leaves()))
        cot_tree = Tree.fromstring(random.choice(rule_dict[rule]))
        cot_phrase = cot_tree.leaves()
        label_lst  = []
        label = ''
        label_max_number = 0
        for word in cot_tree.subtrees(lambda t : t.height() == 2):
            if word.label()[:2] == 'VB':
                label = word.label()
                break
            elif word.label()[:2] == 'JJ':
                label = word.label()
                break
            else:
                if word.label() in label_dict:
                    if len(label_dict[word.label()]) > label_max_number:
                        label_max_number = len(label_dict[word.label()])
                        label = word.label()
        vocabulary = random.choices(label_dict[label], k=3)
        if not generate_CoT(cot_tree) :
            continue
        new_rule, cot = generate_CoT(cot_tree)
        prompt += new_rule + '\n'
        prompt += 'Vocabulary: ' + str(vocabulary) 
        prompt += '. The part of speech of all words in the vocabulary are ' + label + '.\n'
        prompt += 'The step of constructing a phrase based on the grammar rules "' + new_rule + '" is the following:\n'
        prompt += cot
        prompt += 'Examples: ' + ', '.join(example_lst) + '\n'
        phrase_length = len(example_lst[0].split())
        prompt += 'Based on the above information, generate a phase of ' + str(phrase_length) + ' words.'
        generate = replace(prompt)
        use = 0
        for i in range(3):
            if vocabulary[i] in generate:
                use += 1
        if use >= 2:
            continue
        generate_phrase.append(generate)
    f_generate[present_rule] = generate_phrase


with open("/generate/ewt/reviews/height_5/generate_phrase.json","w", encoding='utf-8') as f: 
    f.write(json.dumps(f_generate, ensure_ascii=False))    

    