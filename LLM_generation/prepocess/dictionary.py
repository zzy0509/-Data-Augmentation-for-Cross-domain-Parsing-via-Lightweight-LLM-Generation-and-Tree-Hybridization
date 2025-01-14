import re
from nltk.tree import Tree
# 从同源数据集中选取合适频率的单词作为词典
f_review = open(r"literature.txt","r",encoding="utf-8")
dictionary = open(r"dictionary.txt","w",encoding="utf-8")
data = f_review.read().split('\n')
data = list(set(data))
dict = {}
c = 0
pat= '[a-zA-Z]+'
for sentence in data:
    c += 1
    lst = re.findall(pat,sentence)
    for i in lst:
        i = i.lower()
        dict[i] = dict.get(i,0) + 1
dic_lst = []
for i in dict.keys():
    if 500 <= dict[i]:
        dictionary.write(i + '\n')
        dic_lst.append(i)
