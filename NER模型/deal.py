import pandas as pd
import numpy as np
import re
import jieba.posseg as pseg
import codecs
from langconv import Converter
import jieba
import jieba.posseg
 

def input1(word): 
    word =re.findall(u"[\u4E00-\u9FA50-9a-zA-Z、,， ]",word)
    word =''.join(word)
    return word  
    
def writetxt(string):
    string=re.findall(u"[\u4E00-\u9FA50-9a-zA-Z、,， ]",str(string))
    string=''.join(string)
    word=[list(string)]
    cixingliebiao=[]
#    flag_1=[]
    flag=[[]]
    lab=input1(string)
    seg = jieba.posseg.cut(string)
    for k in seg:
        cixingliebiao.append((k.word, k.flag))
    for k in range(len(cixingliebiao)):
        list_1=list(cixingliebiao[k][0])
        for j in range(len(list_1)):
            flag[0].append(cixingliebiao[k][1])
    return word,flag,lab
    
    
    
    