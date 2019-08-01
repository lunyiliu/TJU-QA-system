# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:14:10 2017

@author: mochp
"""

import pandas as pd

lib = pd.read_excel('input/ming10.16.xlsx',header=None,index=None).fillna(0)

def location(sentense, phrase):
    locationList=[]
    length = len(sentense)
    for i in range(length):
        num = sentense.find(phrase,i,length)
        if num>=0 and (num not in locationList):
            locationList.append(num)
    return locationList

line = 0
num = ['0','1']
lineList = []
for word in lib[1]:
    word = str(word)
    
    line+=1
    word = word.replace(',','，')
    locationList = location(word, '，')
    for i in locationList:
        if word[i-1] not in num:
            lineList.append(line)
            