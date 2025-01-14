from lexical_tree import LexTree
from nltk.tree import Tree
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

def sentence_confidence(sentence, model_name='gpt2'):
    # 加载模型和分词器
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    
    # 对句子进行编码，添加终止符
    inputs = tokenizer.encode(sentence, return_tensors='pt')
    
    # 用模型计算loss，这里不需要实际的标签，我们只是想获取对数似然
    with torch.no_grad():
        outputs = model(inputs, labels=inputs)
    loss = outputs.loss
    
    # 对数似然是负的，因此我们取它的相反数来表示置信度
    log_likelihood = -loss.item()
    
    return log_likelihood
