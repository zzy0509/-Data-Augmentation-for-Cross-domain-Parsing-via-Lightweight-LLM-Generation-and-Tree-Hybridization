import json
from nltk.tree import Tree

with open("label.json","r", encoding='utf-8'  ) as f_label:
    label_dict = json.load(f_label)

with open("generate_phrase.json","r", encoding='utf-8') as f:
    phrase_dict = json.load(f)


new_dict = {}
c = 0
for rule in phrase_dict.keys():
    if phrase_dict[rule] != []:
        label_lst = []
        correct = []
        print(rule)
        print(rule.split(':')[1])
        example = Tree.fromstring(rule.split(':')[1])
        for s in example.subtrees(lambda t: t.height() == 2):
            label_lst.append(s.label())
        for phrase in phrase_dict[rule]:
            word_lst = phrase.split()
            if len(label_lst) != len(word_lst):
                continue
            count = 0
            flag = True
            for i in range(len(word_lst)):
                if (label_lst[i] == 'DT' and word_lst[i] not in label_dict['DT']) and (label_lst[i] == 'DT' and word_lst[i].lower() not in label_dict['DT']):
                    flag = False
                elif (label_lst[i] == 'IN' and word_lst[i] not in label_dict['IN']) and (label_lst[i] == 'IN' and word_lst[i].lower() not in label_dict['IN']):
                    flag = False
                elif (label_lst[i] == 'PRP' and word_lst[i] not in label_dict['PRP']) and (label_lst[i] == 'PRP' and word_lst[i].lower() not in label_dict['PRP']):
                    flag = False
                elif (label_lst[i] == 'TO' and word_lst[i] not in label_dict['TO']) and (label_lst[i] == 'TO' and word_lst[i].lower() not in label_dict['TO']):
                    flag = False
                if word_lst[i] in label_dict[label_lst[i]] or word_lst[i].lower() in label_dict[label_lst[i]] or word_lst[i].capitalize() in label_dict[label_lst[i]]:
                    count += 1
            if flag == True and count/len(word_lst) > 0.5:
                correct.append(phrase)
                c += 1
        if correct != []:
            new_dict[rule] = correct
print(c)

with open("correct.json","w", encoding='utf-8') as f1: ## 设置'utf-8'编码
    f1.write(json.dumps(new_dict, ensure_ascii=False))  