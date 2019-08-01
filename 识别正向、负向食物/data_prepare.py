import pandas as pd
import numpy as np
import csv
import jieba
import jieba.posseg
import re
from gensim.corpora.dictionary import Dictionary
from gensim.models import Word2Vec
import codecs

path1='data/input/traindata_7500.xlsx'
path2='data/input/embeddingdata.xlsx'

def loadfile(path):
    data=pd.read_excel(path,index=None).fillna('')
    sentence=list(data['sentence'])
    food = list(data['food'])
    taste = list(data['taste'])
    food_n = list(data['food_n'])
    taste_n = list(data['taste_n'])
    return data,sentence,food,taste,food_n,taste_n

def data_clean(sentence):
    for i in range(len(sentence)):
        sentence[i]=re.findall(u"[\u4E00-\u9FA50-9a-zA-Z、]",sentence[i])
        sentence[i]=''.join(sentence[i])
    return sentence

def embeddingdata(path):
    data=pd.read_excel(path,index=None).fillna('')
    sentence=list(data['sentence'])
    embeddingdata=[]
    for i in range(len(sentence)):
        embeddingdata.append(list(sentence[i]))
    return embeddingdata

def data_POS(sentence):
    POS=[]
    word=[]
    for i in range(len(sentence)):
        cixingliebiao=[]
        list_2=[]
        seg = jieba.posseg.cut(sentence[i])
        for k in seg:
            cixingliebiao.append((k.word, k.flag))
        for h in range(len(cixingliebiao)):
            list_1=list(cixingliebiao[h][0])
            for j in range(len(list_1)):
                list_2.append(cixingliebiao[h][1])
        POS.append(list_2)
        word.append(list(sentence[i]))
    return POS,word

def data_label(sentence,food,taste,food_n,taste_n,POS,word):
    Pos_word=[]
    for i in range(len(food)):
        food[i]=str(food[i])
        taste[i]=str(taste[i])
        food_n[i]=str(food_n[i])
        taste_n[i]=str(taste_n[i])
        food[i]=food[i].split(' ')
        taste[i]=taste[i].split(' ')
        food_n[i]=food_n[i].split(' ')
        taste_n[i]=taste_n[i].split(' ')
        food[i].sort(key=lambda x: -len(x))
        taste[i].sort(key=lambda x: -len(x))
        food_n[i].sort(key=lambda x: -len(x))
        taste_n[i].sort(key=lambda x: -len(x))
    Food_place=[]
    Taste_place=[]
    Food_n_place=[]
    Taste_n_place=[]
    for i in range(len(sentence)):
        food_place=[]
        taste_place=[]
        food_n_place=[]
        taste_n_place=[]
        for j in range(len(food[i])):
            if food[i][j]=='':
                place=[]
                food_place.append(place)
            else:
                place=[m.start() for m in re.finditer(str(food[i][j]),sentence[i])]
                food_place.append(place)
        Food_place.append(food_place)
        for j in range(len(taste[i])):
            if taste[i][j]=='':
                place=[]
                taste_place.append(place)
            else:
                place=[m.start() for m in re.finditer(str(taste[i][j]), sentence[i])]
                taste_place.append(place)
        Taste_place.append(taste_place)
        for j in range(len(food_n[i])):
            if food_n[i][j]=='':
                place=[]
                food_n_place.append(place)
            else:
                place=[m.start() for m in re.finditer(str(food_n[i][j]),sentence[i])]
                food_n_place.append(place)
        Food_n_place.append(food_n_place)
        for j in range(len(taste_n[i])):
            if taste_n[i][j]=='':
                place=[]
                taste_n_place.append(place)
            else:
                place=[m.start() for m in re.finditer(str(taste_n[i][j]), sentence[i])]
                taste_n_place.append(place)
        Taste_n_place.append(taste_n_place)
    for i in range(len(POS)):
        pos_word=[]
        for j in range(len(POS[i])):
            pw=word[i][j]+'\t'+POS[i][j]
            pos_word.append(pw)
        Pos_word.append(pos_word)
    for i in range(len(Food_place)):
        for j in range(len(Food_place[i])):
            for h in range(len(Food_place[i][j])):
                print(i,j,h,Food_place[i][j][h])
                if '\n' in Pos_word[i][Food_place[i][j][h]]:
                    continue
                else:
                    for k in range(len(food[i][j])):
                        if k==0:
                           Pos_word[i][Food_place[i][j][h]]=Pos_word[i][Food_place[i][j][h]]+'\t'+'fs'+'\n'
                           continue
                        elif k==len(food[i][j])-1:
                            Pos_word[i][Food_place[i][j][h]+k]=Pos_word[i][Food_place[i][j][h]+k]+'\t'+'fe'+'\n'
                        else:
                            Pos_word[i][Food_place[i][j][h]+k]=Pos_word[i][Food_place[i][j][h]+k]+'\t'+'fm'+'\n'
    for i in range(len(Taste_place)):
        for j in range(len(Taste_place[i])):
            for h in range(len(Taste_place[i][j])):
                if '\n' in Pos_word[i][Taste_place[i][j][h]]:
                    continue
                else:
                    for k in range(len(taste[i][j])):
                        if k==0:
                           Pos_word[i][Taste_place[i][j][h]]=Pos_word[i][Taste_place[i][j][h]]+'\t'+'ts'+'\n'
                           continue
                        elif k==len(taste[i][j])-1:
                            Pos_word[i][Taste_place[i][j][h]+k]=Pos_word[i][Taste_place[i][j][h]+k]+'\t'+'te'+'\n'
                        else:
                            Pos_word[i][Taste_place[i][j][h]+k]=Pos_word[i][Taste_place[i][j][h]+k]+'\t'+'tm'+'\n'
    for i in range(len(Food_n_place)):
        for j in range(len(Food_n_place[i])):
            for h in range(len(Food_n_place[i][j])):
                print(i,j,h,Food_n_place[i][j][h])
                if '\n' in Pos_word[i][Food_n_place[i][j][h]]:
                    continue
                else:
                    for k in range(len(food_n[i][j])):
                        if k==0:
                           Pos_word[i][Food_n_place[i][j][h]]=Pos_word[i][Food_n_place[i][j][h]]+'\t'+'fns'+'\n'
                           continue
                        elif k==len(food_n[i][j])-1:
                            Pos_word[i][Food_n_place[i][j][h]+k]=Pos_word[i][Food_n_place[i][j][h]+k]+'\t'+'fne'+'\n'
                        else:
                            Pos_word[i][Food_n_place[i][j][h]+k]=Pos_word[i][Food_n_place[i][j][h]+k]+'\t'+'fnm'+'\n'
    for i in range(len(Taste_n_place)):
        for j in range(len(Taste_n_place[i])):
            for h in range(len(Taste_n_place[i][j])):
                if '\n' in Pos_word[i][Taste_n_place[i][j][h]]:
                    continue
                else:
                    for k in range(len(taste_n[i][j])):
                        if k==0:
                           Pos_word[i][Taste_n_place[i][j][h]]=Pos_word[i][Taste_n_place[i][j][h]]+'\t'+'tns'+'\n'
                           continue
                        elif k==len(taste_n[i][j])-1:
                            Pos_word[i][Taste_n_place[i][j][h]+k]=Pos_word[i][Taste_n_place[i][j][h]+k]+'\t'+'tne'+'\n'
                        else:
                            Pos_word[i][Taste_n_place[i][j][h]+k]=Pos_word[i][Taste_n_place[i][j][h]+k]+'\t'+'tnm'+'\n'
    for i in range(len(Pos_word)):
        for j in range(len(Pos_word[i])):
            if '\n' in Pos_word[i][j]:
                continue
            else:
                Pos_word[i][j]=Pos_word[i][j]+'\t'+'o'+'\n'
    for i in range(len(Pos_word)):
        Pos_word[i]=''.join(Pos_word[i])
    Pos_word='\n'.join(Pos_word)
    f=codecs.open("data/sample_train.txt","w",encoding='utf-8')
    f.write(''.join(Pos_word))
    f.close()
    return

def embedding_sentences(sentences):
    w2vModel = Word2Vec(sentences, size = 64, window = 5, min_count = 1)
    w2vModel.save('Model/Word2vec_model.pkl')
    gensim_dict = Dictionary()
    gensim_dict.doc2bow(w2vModel.wv.vocab.keys(),allow_update=True)
    w2indx = {v: k for k, v in gensim_dict.items()}
    w2vec = {word: w2vModel[word] for word in w2indx.keys()}    
    return w2vec

if __name__ == '__main__':
    data,sentence,food,taste,food_n,taste_n=loadfile(path1)
    embeddingdata=embeddingdata(path2)
    sentence=data_clean(sentence)
    POS,word=data_POS(sentence)
    data_label(sentence,food,taste,food_n,taste_n,POS,word)
    embedding_sentences(embeddingdata)