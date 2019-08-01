#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'jxliu.nlper@gmail.com'
"""
    标记文件
"""
import yaml
import pickle
import tensorflow as tf
import numpy as np   
import pandas as pd    
from load_data import load_vocs
from model import SequenceLabelingModel
from deal import writetxt
from utils import map_item2id
import re
import os
#NER_ROOT=r'C:\Users\lenovvo\Desktop\吴偶教授\天津大学智能问答\天大美食智能问答\NER模型'
NER_ROOT=os.path.dirname(os.path.abspath( __file__))
#print(NER_ROOT)
# 加载配置文件
with open(NER_ROOT+'\\config.yml','rb') as file_config:
    config = yaml.load(file_config)
config['data_params']['path_result']=os.path.join(NER_ROOT,config['data_params']['path_result'])
config['data_params']['path_test']=os.path.join(NER_ROOT,config['data_params']['path_test'])
config['data_params']['path_train']=os.path.join(NER_ROOT,config['data_params']['path_train'])
config['data_params']['voc_params']['f1']['path']=os.path.join(NER_ROOT,config['data_params']['voc_params']['f1']['path'])
config['data_params']['voc_params']['f2']['path']=os.path.join(NER_ROOT,config['data_params']['voc_params']['f2']['path'])
config['data_params']['voc_params']['label']['path']=os.path.join(NER_ROOT,config['data_params']['voc_params']['label']['path'])
config['model_params']['embed_params']['f1']['path']=os.path.join(NER_ROOT,config['model_params']['embed_params']['f1']['path'])
config['model_params']['embed_params']['f1']['path_pre_train']=os.path.join(NER_ROOT,config['model_params']['embed_params']['f1']['path_pre_train'])
config['model_params']['path_model']=os.path.join(NER_ROOT,config['model_params']['path_model'])
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
    path_model=config['model_params']['path_model'],
    )



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
    while (4 in seq[0][beginnumber:]):
        Food=''
        if 4 in seq[0][beginnumber:] and 5 in seq[0][beginnumber:]:
            place_4=beginnumber+seq[0][beginnumber:].index(4)
            place_5=beginnumber+seq[0][beginnumber:].index(5)+1
            Food=lab[place_4:place_5]
            Food=''.join(Food)
            food=food+Food+','
            beginnumber=beginnumber+place_5
        else:
            place_4=beginnumber+seq[0][beginnumber:].index(4)
            Food=lab[place_4:(place_4+1)]
            Food=''.join(Food)
            food=food+Food+','
            beginnumber=beginnumber+place_4+1
    beginnumber=0
    location=''
    while 10 in seq[0][beginnumber:]:
        Location=''
        if 10 in seq[0][beginnumber:] and 11 in seq[0][beginnumber:]:
            place_10=beginnumber+seq[0][beginnumber:].index(10)
            place_11=beginnumber+seq[0][beginnumber:].index(11)+1
            Location=lab[place_10:place_11]
            Location=''.join(Location)
            location=location+Location+','
            beginnumber=beginnumber+place_11
        else:
            place_10=beginnumber+seq[0][beginnumber:].index(10)
            Location=lab[place_10:(place_10+1)]
            Location=''.join(Location)
            location=location+Location+','
            beginnumber=beginnumber+place_10+1
    beginnumber=0
    store=''
    while (12 in seq[0][beginnumber:]):
        Store=''
        if 12 in seq[0][beginnumber:] and 13 in seq[0][beginnumber:]:
            place_12=beginnumber+seq[0][beginnumber:].index(12)
            place_13=beginnumber+seq[0][beginnumber:].index(13)+1
            Store=lab[place_12:place_13]
            Store=''.join(Store)
            store=store+Store+','
            beginnumber=beginnumber+place_13
        else:
            place_12=beginnumber+seq[0][beginnumber:].index(12)
            Store=lab[place_12:(place_12+1)]
            Store=''.join(Store)
            store=store+Store+','
            beginnumber=beginnumber+place_12+1
    beginnumber=0
    keyword=''
    while 3 in seq[0][beginnumber:]:
        Keyword=''
        if 3 in seq[0][beginnumber:] and 6 in seq[0][beginnumber:]:
            place_3=beginnumber+seq[0][beginnumber:].index(3)
            place_6=beginnumber+seq[0][beginnumber:].index(6)+1
            Keyword=lab[place_3:place_6]
            Keyword=''.join(Keyword)
            keyword=keyword+Keyword+','
            beginnumber=beginnumber+place_6
        else:
            place_3=beginnumber+seq[0][beginnumber:].index(3)
            keyword=lab[place_3:(place_3+1)]
            Keyword=''.join(Keyword)
            keyword=keyword+Keyword+','
            beginnumber=beginnumber+place_3+1
    return food.strip(','),location.strip(','),store.strip(','),keyword.strip(',')

def loadfile(path):
    data=pd.read_excel(path,index=None).fillna('')
    sentence=list(data['sentence'])
    food = list(data['food'])
    taste = list(data['taste'])
    food_n = list(data['food_n'])
    taste_n = list(data['taste_n'])
    return data,sentence,food,taste,food_n,taste_n



def food_taste_extract(string):
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
        return food,taste,food_n,taste_n
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