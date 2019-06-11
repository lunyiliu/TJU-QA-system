#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'jxliu.nlper@gmail.com'
"""
    标记文件
"""
import yaml
import pickle
import csv
import tensorflow as tf
import numpy as np   
import pandas as pd    
from load_data import load_vocs
from model import SequenceLabelingModel
from deal import writetxt
from utils import map_item2id
import re


# 加载配置文件
with open('./config.yml','rb') as file_config:
    config = yaml.load(file_config)

feature_names = config['model_params']['feature_names']

# 初始化embedding shape, dropouts, 预训练的embedding也在这里初始化)
feature_weight_shape_dict, feature_weight_dropout_dict, \
    feature_init_weight_dict = dict(), dict(), dict()
for feature_name in feature_names:
    feature_weight_shape_dict[feature_name] = \
        config['model_params']['embed_params'][feature_name]['shape']
    feature_weight_dropout_dict[feature_name] = \
        config['model_params']['embed_params'][feature_name]['dropout_rate']
    path_pre_train = config['model_params']['embed_params'][feature_name]['path']
    if path_pre_train:
        with open(path_pre_train, 'rb') as file_r:
            feature_init_weight_dict[feature_name] = pickle.load(file_r)

# 加载vocs
path_vocs = []
for feature_name in feature_names:
    path_vocs.append(config['data_params']['voc_params'][feature_name]['path'])
path_vocs.append(config['data_params']['voc_params']['label']['path'])
vocs = load_vocs(path_vocs)


# 加载模型
model = SequenceLabelingModel(
    sequence_length=config['model_params']['sequence_length'],
    nb_classes=config['model_params']['nb_classes'],
    nb_hidden=config['model_params']['bilstm_params']['num_units'],
    feature_weight_shape_dict=feature_weight_shape_dict,
    feature_init_weight_dict=feature_init_weight_dict,
    feature_weight_dropout_dict=feature_weight_dropout_dict,
    dropout_rate=config['model_params']['dropout_rate'],
    nb_epoch=config['model_params']['nb_epoch'], feature_names=feature_names,
    batch_size=config['model_params']['batch_size'],
    train_max_patience=config['model_params']['max_patience'],
    use_crf=config['model_params']['use_crf'],
    l2_rate=config['model_params']['l2_rate'],
    rnn_unit=config['model_params']['rnn_unit'],
    learning_rate=config['model_params']['learning_rate'],
    path_model=config['model_params']['path_model'])



saver = tf.train.Saver()
saver.restore(model.sess, config['model_params']['path_model'])


def init_data(word,flag,feature_names, vocs, max_len, model='train', sep=' '):
    sentence_count = len(word)
    one_instance_items = [word,flag]
    data_dict = dict()
    for feature_name in feature_names:
        data_dict[feature_name] = np.zeros(
            (sentence_count, max_len), dtype='int32')
      
    for index in range(sentence_count): 
        one_instance_items = [word[index],flag[index],[]]
        
        for i in range(len(feature_names)):
            data_dict[feature_names[i]][index, :] = map_item2id(
                one_instance_items[i], vocs[i], max_len)
      
    return data_dict

def predict(string):
#    chioce = []
    word,flag,lab = writetxt(string)
    # 加载数据 path=config['data_params']['path_test'],
    if len(lab[0]) == 0:
        return 'ok;None'

    data_dict = init_data(word,
                          flag,
                          feature_names=feature_names, 
                          sep='\t',
                          vocs=vocs, 
                          max_len=config['model_params']['sequence_length'],
                          model='test')
    
    
    seq = model.predict(data_dict)
#    print(seq)
#    return viterbi_sequences
    beginnumber=0
    food=''
    while (2 in seq[0][beginnumber:]):
        Food=''
        if 2 in seq[0][beginnumber:] and 3 in seq[0][beginnumber:]:
            place_2=beginnumber+seq[0][beginnumber:].index(2)
            place_3=beginnumber+seq[0][beginnumber:].index(3)+1
            Food=lab[place_2:place_3]
            Food=''.join(Food)
            food=food+Food+','
            beginnumber=beginnumber+place_3
        else:
            place_2=beginnumber+seq[0][beginnumber:].index(2)
            Food=lab[place_2:(place_2+1)]
            Food=''.join(Food)
            food=food+Food+','
            beginnumber=beginnumber+place_2+1
    beginnumber=0
    taste=''
    while 9 in seq[0][beginnumber:]:
        Taste=''
        if 9 in seq[0][beginnumber:] and 10 in seq[0][beginnumber:]:
            place_9=beginnumber+seq[0][beginnumber:].index(9)
            place_10=beginnumber+seq[0][beginnumber:].index(10)+1
            Taste=lab[place_9:place_10]
            Taste=''.join(Taste)
            taste=taste+Taste+','
            beginnumber=beginnumber+place_10
        else:
            place_9=beginnumber+seq[0][beginnumber:].index(9)
            Taste=lab[place_9:(place_9+1)]
            Taste=''.join(Taste)
            taste=taste+Taste+','
            beginnumber=beginnumber+place_9+1
    beginnumber=0
    food_n=''
    while (5 in seq[0][beginnumber:]):
        Food_n=''
        if 5 in seq[0][beginnumber:] and 6 in seq[0][beginnumber:]:
            place_5=beginnumber+seq[0][beginnumber:].index(5)
            place_6=beginnumber+seq[0][beginnumber:].index(6)+1
            Food_n=lab[place_5:place_6]
            Food_n=''.join(Food_n)
            food_n=food_n+Food_n+','
            beginnumber=beginnumber+place_6
        else:
            place_5=beginnumber+seq[0][beginnumber:].index(5)
            Food_n=lab[place_5:(place_5+1)]
            Food_n=''.join(Food_n)
            food_n=food_n+Food_n+','
            beginnumber=beginnumber+place_5+1
    beginnumber=0
    taste_n=''
    while 7 in seq[0][beginnumber:]:
        Taste_n=''
        if 7 in seq[0][beginnumber:] and 11 in seq[0][beginnumber:]:
            place_7=beginnumber+seq[0][beginnumber:].index(7)
            place_11=beginnumber+seq[0][beginnumber:].index(11)+1
            Taste_n=lab[place_7:place_11]
            Taste_n=''.join(Taste_n)
            taste_n=taste_n+Taste_n+','
            beginnumber=beginnumber+place_11
        else:
            place_7=beginnumber+seq[0][beginnumber:].index(7)
            Taste_n=lab[place_7:(place_7+1)]
            Taste_n=''.join(Taste_n)
            taste_n=taste_n+Taste_n+','
            beginnumber=beginnumber+place_7+1
    return food,taste,food_n,taste_n

def loadfile(path):
    data=pd.read_excel(path,index=None).fillna('')
    sentence=list(data['sentence'])
    food = list(data['food'])
    taste = list(data['taste'])
    food_n = list(data['food_n'])
    taste_n = list(data['taste_n'])
    return data,sentence,food,taste,food_n,taste_n


#data,sentence,food,taste,food_n,taste_n=loadfile("data/input/testdata_7500.xlsx")
#
#food_number=0
#taste_number=0
#food_n_number=0
#taste_n_number=0
#
#food_call=0
#taste_call=0
#food_n_call=0
#taste_n_call=0
#
#food_call_1=0
#taste_call_1=0
#food_n_call_1=0
#taste_n_call_1=0
#
#foodresult=[]
#tasteresult=[]
#food_nresult=[]
#taste_nresult=[]
#
#false=[]
#
#for i in range(len(sentence)):
#    r=''
#    food_2,taste_2,food_n_2,taste_n_2=predict(sentence[i])
#    print(food_2,taste_2,food_n_2,taste_n_2)
#    foodresult.append(food_2.replace('&',''))
#    tasteresult.append(taste_2.replace('&',''))
#    food_nresult.append(food_n_2.replace('&',''))
#    taste_nresult.append(taste_n_2.replace('&',''))
#    food_2=food_2.replace('&','')
#    taste_2=taste_2.replace('&','')
#    food_n_2=food_n_2.replace('&','')
#    taste_n_2=taste_n_2.replace('&','')
#    if str(food[i])=='':
#        if food[i]==food_2:
#            food_number=food_number+1
#        else:
#            r=r+'food'+' '
#    else:
#        food_call=food_call+1
#        food[i]=str(food[i])
#        food[i]=food[i].replace(' ','').replace('.0','')
#        if food[i] in food_2:
#            food_number=food_number+1
#            food_call_1=food_call_1+1
#        else:
#            r=r+'food'+' '
#    if str(taste[i])=='':
#        if taste[i]==taste_2:
#            taste_number=taste_number+1
#        else:
#            r=r+'taste'+' '
#    else:
#        taste_call=taste_call+1
#        taste[i]=str(taste[i])
#        taste[i]=taste[i].replace(' ','').replace('.0','')
#        if taste[i] in taste_2:
#            taste_number=taste_number+1
#            taste_call_1=taste_call_1+1
#        else:
#            r=r+'taste'+' '
#    if str(food_n[i])=='':
#        if food_n[i]==food_n_2:
#            food_n_number=food_n_number+1
#        else:
#            r=r+'food_n'+' '
#    else:
#        food_n_call=food_n_call+1
#        food_n[i]=str(food_n[i])
#        food_n[i]=food_n[i].replace(' ','').replace('.0','')
#        if food_n[i] in food_n_2:
#            food_n_number=food_n_number+1
#            food_n_call_1=food_n_call_1+1
#        else:
#            r=r+'food_n'+' '
#    if str(taste_n[i])=='':
#        if taste_n[i]==taste_n_2:
#            taste_n_number=taste_n_number+1
#        else:
#            r=r+'taste_n'+' '
#    else:
#        taste_n_call=taste_n_call+1
#        taste_n[i]=str(taste_n[i])
#        taste_n[i]=taste_n[i].replace(' ','').replace('.0','')
#        if taste_n[i] in taste_n_2:
#            taste_n_number=taste_n_number+1
#            taste_n_call_1=taste_n_call_1+1
#        else:
#            r=r+'taste_n'+' ' 
#    false.append(r)
##准确率            
#food_accuracy=food_number/len(food)
#taste_accuracy=taste_number/len(taste)
#food_n_accuracy=food_n_number/len(food)
#taste_n_accuracy=taste_n_number/len(taste)
#accuracy=(food_accuracy+taste_accuracy+food_n_accuracy+taste_n_accuracy)/4
##召回率
#food_recall=food_call_1/food_call
#taste_recall=taste_call_1/taste_call
#food_n_recall=food_n_call_1/food_n_call
#taste_n_recall=taste_n_call_1/taste_n_call
#recall=(food_call_1+taste_call_1+food_n_call_1+taste_n_call_1)/(food_call+taste_call+food_n_call+taste_n_call)
#print('测试集容量',len(sentence))
#print('food正确数：',food_number,'\n','taste正确数：',taste_number,'\n','food_n正确数：',food_n_number,'\n','taste_n正确数：',taste_n_number)
#print('food正确率：',food_accuracy,'\n','taste正确率：',taste_accuracy,'\n','food_n正确率：',food_n_accuracy,'\n','taste_n正确率：',taste_n_accuracy)
#print('总正确率：',accuracy)
#print('food召回率：',food_recall,'\n','taste召回率：',taste_recall,'\n','taste_n召回率：',taste_n_recall,'\n','food_n召回率：',food_n_recall)
#print('总召回率：',recall)
#
#result=pd.DataFrame(data,columns=['sentence'])
#result['food']=food
#result['taste']=taste
#result['food_n']=food_n
#result['taste_n']=taste_n
#result['machine_food']=foodresult
#result['machine_taste']=tasteresult
#result['machine_food_n']=food_nresult
#result['machine_taste_n']=taste_nresult
#result['false']=false
#result.to_excel("data/input/result7500.xlsx")

def foodtaste_extract(string):
    string=string.replace(' ',',').replace('.',',').replace('。',',').replace('，',',').replace('！',',').replace('!',',').replace('?',',').replace('？',',')
    string=re.findall(u"[\u4E00-\u9FA50-9a-zA-Z,]",str(string))
    string=''.join(string)
    string_l=string.split(',')
    food=''
    taste=''
    food_n=''
    taste_n=''
    for i in range(len(string_l)):
        if string_l[i]=='':
            continue
        else:
            food_l,taste_l,food_n_l,taste_n_l=predict(string_l[i])
            food=(food+food_l+',')[:-1]
            taste=(taste+taste_l+',')[:-1]
            food_n=(food_n+food_n_l+',')[:-1]
            taste_n=(taste_n+taste_n_l+',')[:-1]
#    others,deny = predict(string)
    ALL = food+taste+food_n+taste_n
#    print(ALL)
    if ALL== '':
#        print ('none')
        return 'none'
    else:
#        print('food:',food,'\n','taste:',taste,'\n','food_n',food_n,'\n','taste:',taste_n)
        if len(food)>0:
            food=food[:-1]
        if len(taste)>0:
            taste=taste[:-1]
        if len(food_n)>0:
            food_n=food_n[:-1]
        if len(taste_n)>0:
            taste_n=taste_n[:-1]
        return food,taste,food_n,taste_n